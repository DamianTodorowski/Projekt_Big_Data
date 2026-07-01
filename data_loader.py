# -*- coding: utf-8 -*-
import os
import requests
import pandas as pd
import numpy as np
import streamlit as st

# Słownik z mapowaniem kodów sezonów na czytelne etykiety i URL
SEASONS = {
    "2021/22": "2122",
    "2022/23": "2223",
    "2023/24": "2324",
    "2024/25": "2425",
    "2025/26": "2526"
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def get_season_url(season_code):
    """Generuje URL do pliku CSV na football-data.co.uk"""
    return f"https://www.football-data.co.uk/mmz4281/{season_code}/E0.csv"

def parse_date_robustly(date_str):
    """
    Konwertuje datę tekstową na obiekt datetime przy użyciu różnych formatów.
    Czasami w plikach CSV rok jest zapisany 2-cyfrowo (%y) a czasami 4-cyfrowo (%Y).
    """
    if pd.isna(date_str) or not isinstance(date_str, str):
        return pd.NaT
    date_str = date_str.strip()
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d", "%y-%m-%d"):
        try:
            return pd.to_datetime(date_str, format=fmt)
        except (ValueError, TypeError):
            continue
    try:
        return pd.to_datetime(date_str)
    except Exception:
        return pd.NaT

@st.cache_data(show_spinner="Pobieranie i przetwarzanie danych...")
def load_season_data(season_name):
    """
    Pobiera i przetwarza dane dla wybranego sezonu.
    Najpierw szuka w lokalnym katalogu 'data', a jeśli plik nie istnieje,
    pobiera go z internetu i zapisuje lokalnie jako backup.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    season_code = SEASONS[season_name]
    local_file = os.path.join(DATA_DIR, f"E0_{season_code}.csv")
    
    df = None
    
    # 1. Próba załadowania z pliku lokalnego
    if os.path.exists(local_file):
        try:
            df = pd.read_csv(local_file)
        except Exception as e:
            # W razie błędu pliku lokalnego, spróbujemy pobrać na nowo
            df = None

    # 2. Jeśli brak pliku lokalnego lub błąd, pobieramy z sieci
    if df is None:
        url = get_season_url(season_code)
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                with open(local_file, "wb") as f:
                    f.write(response.content)
                df = pd.read_csv(local_file)
            else:
                # W przypadku problemów z siecią (np. 404 lub brak połączenia) 
                # podniesiemy wyjątek, który obsłużymy w UI
                raise ConnectionError(f"Nie udało się pobrać danych ze źródła. Kod statusu: {response.status_code}")
        except Exception as e:
            # Jeśli brak pliku lokalnego i brak sieci, rzucamy błąd
            raise RuntimeError(f"Błąd podczas pozyskiwania danych: {str(e)}")

    # 3. Krok czyszczenia i transformacji danych
    # Filtrujemy puste wiersze (czasem na końcu CSV są puste wiersze)
    df = df.dropna(subset=["HomeTeam", "AwayTeam", "Date"])
    
    # Oczyszczanie białych znaków z nazw zespołów i sędziów
    df["HomeTeam"] = df["HomeTeam"].astype(str).str.strip()
    df["AwayTeam"] = df["AwayTeam"].astype(str).str.strip()
    if "Referee" in df.columns:
        df["Referee"] = df["Referee"].astype(str).str.strip()
    
    # Czyszczenie daty
    df["Date_Parsed"] = df["Date"].apply(parse_date_robustly)
    df = df.dropna(subset=["Date_Parsed"])
    df = df.sort_values(by="Date_Parsed").reset_index(drop=True)
    
    # Rzutowanie typów numerycznych na poprawne
    numeric_cols = [
        "FTHG", "FTAG", "HTHG", "HTAG", "HS", "AS", "HST", "AST", 
        "HF", "AF", "HC", "AC", "HY", "AY", "HR", "AR"
    ]
    for col in numeric_cols:
        if col in df.columns:
            # Uzupełnienie ewentualnych braków zerami i konwersja na int
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Tworzenie kolumn pochodnych
    df["TotalGoals"] = df["FTHG"] + df["FTAG"]
    df["TotalShots"] = df["HS"] + df["AS"]
    df["TotalFouls"] = df["HF"] + df["AF"]
    df["TotalYellowCards"] = df["HY"] + df["AY"]
    df["TotalRedCards"] = df["HR"] + df["AR"]
    df["TotalCards"] = df["TotalYellowCards"] + df["TotalRedCards"]
    
    # Rozstrzygnięcie meczu w języku polskim
    def get_result_full(row):
        if row["FTR"] == "H":
            return "Wygrana Gospodarza"
        elif row["FTR"] == "A":
            return "Wygrana Gościa"
        else:
            return "Remis"
            
    df["FTR_Full"] = df.apply(get_result_full, axis=1)
    
    # Dodanie punktów meczowych
    df["Points_Home"] = df["FTR"].apply(lambda x: 3 if x == "H" else (1 if x == "D" else 0))
    df["Points_Away"] = df["FTR"].apply(lambda x: 3 if x == "A" else (1 if x == "D" else 0))
    
    # Dodanie kolumny z nazwą sezonu
    df["Season"] = season_name
    
    return df

@st.cache_data
def load_all_seasons_data():
    """Wczytuje i łączy dane ze wszystkich sezonów w jeden DataFrame"""
    dfs = []
    errors = []
    for s_name in SEASONS.keys():
        try:
            df_season = load_season_data(s_name)
            dfs.append(df_season)
        except Exception as e:
            errors.append(f"{s_name}: {str(e)}")
            
    if not dfs:
        raise RuntimeError(f"Nie udało się załadować danych dla żadnego sezonu. Szczegóły błędów: {'; '.join(errors)}")
        
    return pd.concat(dfs, ignore_index=True)

def generate_league_table(df):
    """
    Generuje tabelę ligową na podstawie podanego DataFrame meczów.
    Zwraca DataFrame zawierający: Miejsce, Zespół, Mecze, Zwycięstwa, Remisy, Porażki, Bramki+, Bramki-, Bilans, Punkty, Formę.
    """
    teams = pd.concat([df["HomeTeam"], df["AwayTeam"]]).unique()
    table_data = []
    
    for team in sorted(teams):
        # Mecze u siebie
        home_matches = df[df["HomeTeam"] == team]
        # Mecze na wyjeździe
        away_matches = df[df["AwayTeam"] == team]
        
        matches_played = len(home_matches) + len(away_matches)
        if matches_played == 0:
            continue
            
        wins = len(home_matches[home_matches["FTR"] == "H"]) + len(away_matches[away_matches["FTR"] == "A"])
        draws = len(home_matches[home_matches["FTR"] == "D"]) + len(away_matches[away_matches["FTR"] == "D"])
        losses = len(home_matches[home_matches["FTR"] == "A"]) + len(away_matches[away_matches["FTR"] == "H"])
        
        goals_scored = home_matches["FTHG"].sum() + away_matches["FTAG"].sum()
        goals_conceded = home_matches["FTAG"].sum() + away_matches["FTHG"].sum()
        goal_diff = goals_scored - goals_conceded
        
        points = wins * 3 + draws * 1
        
        # Pobieranie formy (5 ostatnich meczów chronologicznie)
        team_matches = df[(df["HomeTeam"] == team) | (df["AwayTeam"] == team)].sort_values(by="Date_Parsed")
        last_5 = team_matches.tail(5)
        
        form_list = []
        for idx, row in last_5.iterrows():
            is_home = row["HomeTeam"] == team
            res = row["FTR"]
            if res == "D":
                form_list.append("R")
            elif (res == "H" and is_home) or (res == "A" and not is_home):
                form_list.append("Z")
            else:
                form_list.append("P")
        
        # Odwracamy, by najnowszy mecz był po prawej stronie, lub reprezentujemy jako string
        form_str = " ".join(form_list)
        
        # Statystyki domowe/wyjazdowe
        home_wins = len(home_matches[home_matches["FTR"] == "H"])
        home_draws = len(home_matches[home_matches["FTR"] == "D"])
        home_losses = len(home_matches[home_matches["FTR"] == "A"])
        home_points = home_wins * 3 + home_draws
        
        away_wins = len(away_matches[away_matches["FTR"] == "A"])
        away_draws = len(away_matches[away_matches["FTR"] == "D"])
        away_losses = len(away_matches[away_matches["FTR"] == "H"])
        away_points = away_wins * 3 + away_draws
        
        table_data.append({
            "Klub": team,
            "Mecze": matches_played,
            "Zwycięstwa": wins,
            "Remisy": draws,
            "Porażki": losses,
            "Bramki Zdobyte": goals_scored,
            "Bramki Stracone": goals_conceded,
            "Bilans Bramek": goal_diff,
            "Punkty": points,
            "Forma (5 ostatnich)": form_str,
            "Pkt Domowe": home_points,
            "Pkt Wyjazdowe": away_points,
            "Zwycięstwa Dom": home_wins,
            "Remisy Dom": home_draws,
            "Porażki Dom": home_losses,
            "Zwycięstwa Wyjazd": away_wins,
            "Remisy Wyjazd": away_draws,
            "Porażki Wyjazd": away_losses
        })
        
    table_df = pd.DataFrame(table_data)
    # Sortowanie: 1. Punkty, 2. Bilans bramek, 3. Bramki zdobyte, 4. Nazwa klubu
    table_df = table_df.sort_values(
        by=["Punkty", "Bilans Bramek", "Bramki Zdobyte", "Klub"], 
        ascending=[False, False, False, True]
    ).reset_index(drop=True)
    
    # Dodanie kolumny z pozycją
    table_df.index = table_df.index + 1
    table_df.index.name = "Pozycja"
    
    return table_df.reset_index()
