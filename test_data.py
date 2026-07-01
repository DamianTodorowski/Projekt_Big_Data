# -*- coding: utf-8 -*-
import sys
from data_loader import load_season_data, generate_league_table
from stadiums import STADIUMS_DB
from predictor import predict_match_outcome

def run_tests():
    print("=== Rozpoczęcie testów logicznych ===")
    
    # 1. Test wczytania sezonu
    season = "2023/24"
    print(f"\n1. Test wczytania sezonu {season}...")
    try:
        df = load_season_data(season)
        print(f"Sukces! Wczytano {len(df)} wierszy.")
        print("Kolumny w DataFrame:", df.columns.tolist()[:10], "... i inne.")
        
        # Sprawdzenie braków
        null_count = df[["HomeTeam", "AwayTeam", "Date_Parsed", "FTHG", "FTAG"]].isnull().sum().sum()
        print(f"Liczba wartości null w kluczowych kolumnach: {null_count}")
        assert null_count == 0, "Błąd: Wykryto wartości null w kluczowych kolumnach!"
    except Exception as e:
        print(f"BŁĄD wczytywania danych: {str(e)}")
        sys.exit(1)
        
    # 2. Sprawdzenie spójności bazy stadionów
    print("\n2. Sprawdzenie spójności bazy stadionów...")
    teams_in_data = set(df["HomeTeam"].unique())
    missing_teams = []
    for team in teams_in_data:
        if team not in STADIUMS_DB:
            missing_teams.append(team)
            
    if missing_teams:
        print(f"Ostrzeżenie: Brakujące drużyny w bazie stadionów: {missing_teams}")
    else:
        print("Sukces! Wszystkie drużyny z sezonu 2023/24 istnieją w bazie stadionów.")

    # 3. Test generowania tabeli ligowej
    print("\n3. Test generowania tabeli ligowej...")
    table = generate_league_table(df)
    print("Sukces! Wygenerowano tabelę ligową.")
    print("Top 5 drużyn:")
    print(table[["Pozycja", "Klub", "Mecze", "Punkty", "Bramki Zdobyte", "Forma (5 ostatnich)"]].head(5))
    
    # Sprawdzenie czy suma punktów jest sensowna
    assert len(table) == 20, f"Błąd: Liczba drużyn w tabeli to {len(table)}, a powinna być 20!"
    print(f"Liczba zespołów w tabeli: {len(table)} (OK)")

    # 4. Test silnika predykcji Poissona
    print("\n4. Test silnika predykcji Poissona...")
    home = "Arsenal"
    away = "Chelsea"
    prediction = predict_match_outcome(df, home, away)
    print(f"Mecz: {home} vs {away}")
    print(f"Oczekiwane gole gospodarza: {prediction['expected_home_goals']}")
    print(f"Oczekiwane gole gościa: {prediction['expected_away_goals']}")
    print(f"Prawdopodobieństwo wygranej gospodarza: {prediction['home_win_prob']}%")
    print(f"Prawdopodobieństwo remisu: {prediction['draw_prob']}%")
    print(f"Prawdopodobieństwo wygranej gościa: {prediction['away_win_prob']}%")
    print(f"Najbardziej prawdopodobny wynik: {prediction['most_likely_score'][0]}:{prediction['most_likely_score'][1]} (szansa: {prediction['most_likely_prob']}%)")
    
    total_prob = prediction['home_win_prob'] + prediction['draw_prob'] + prediction['away_win_prob']
    print(f"Suma prawdopodobieństw: {total_prob}%")
    assert abs(total_prob - 100.0) < 1.0, "Błąd: Suma prawdopodobieństw znacznie różni się od 100%!"
    print("Sukces! Test predykcji zakończony pomyślnie.")
    
    print("\n=== Wszystkie testy zakończone SUKCESEM! ===")

if __name__ == "__main__":
    run_tests()
