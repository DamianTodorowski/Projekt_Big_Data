# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Importy własnych modułów
from data_loader import load_season_data, generate_league_table, SEASONS
from stadiums import get_stadium_info, STADIUMS_DB
from predictor import predict_match_outcome

# Ustawienia strony
st.set_page_config(
    page_title="Premier League Analytics Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Wstrzyknięcie stylów CSS dla podniesienia estetyki UI (efekt "premium")
def apply_custom_css():
    st.markdown("""
    <style>
    /* Gradientowy tytuł aplikacji */
    .title-gradient {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ff87 0%, #0284c7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 12px rgba(0, 255, 135, 0.15);
    }
    
    .subtitle {
        font-size: 1.15rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    
    /* Premium KPI Cards z szklanym efektem */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        flex: 1;
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 4px solid #00ff87;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #00ff87;
        background: rgba(30, 41, 59, 0.95);
    }
    
    .kpi-value {
        font-size: 2.25rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.25rem;
    }
    
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Formatowanie odznak formy (Zwycięstwo, Remis, Porażka) */
    .form-badge {
        display: inline-block;
        width: 26px;
        height: 26px;
        line-height: 26px;
        border-radius: 50%;
        text-align: center;
        font-weight: 800;
        font-size: 0.8rem;
        margin-right: 4px;
        color: #ffffff;
    }
    .form-z { background-color: #10b981; } /* Zwycięstwo - zielony */
    .form-r { background-color: #64748b; } /* Remis - szary */
    .form-p { background-color: #ef4444; } /* Porażka - czerwony */

    /* Kontener komentarzy analitycznych */
    .commentary-box {
        background-color: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #0284c7;
        padding: 1rem 1.25rem;
        border-radius: 4px 12px 12px 4px;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        font-style: italic;
        color: #cbd5e1;
    }
    
    /* Formatowanie sekcji sędziego i profilu */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        border-bottom: 2px solid #334155;
        padding-bottom: 0.5rem;
        margin-bottom: 1.25rem;
        color: #f1f5f9;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# --- SIDEBAR (PANEL BOCZNY) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚽ PL Analytics Hub</h2>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg", width=150)
    st.markdown("---")
    
    # 1. Widget wyboru sezonu (Globalny)
    selected_season = st.selectbox(
        "Wybierz Sezon",
        options=list(SEASONS.keys()),
        index=len(SEASONS) - 1 # Domyślnie ostatni dostępny sezon (2025/26)
    )
    
    st.markdown("---")
    st.markdown("### O projekcie")
    st.markdown(
        "Aplikacja analityczna integrująca pełny przepływ pracy z danymi Premier League. "
        "Wykorzystuje historyczne statystyki meczowe w celu identyfikacji wzorców, analizy sędziów "
        "oraz modelowania predykcyjnego (Poisson)."
    )
    
    st.markdown("---")
    st.markdown("**Dane:** [football-data.co.uk](https://www.football-data.co.uk/)")
    st.markdown("**Autor:** Damian Todorowski")

# Wczytanie danych dla wybranego sezonu
try:
    df_matches = load_season_data(selected_season)
except Exception as e:
    st.error(f"Nie udało się załadować danych dla sezonu {selected_season}: {str(e)}")
    st.stop()

# --- GŁÓWNY PANEL ---
st.markdown("<h1 class='title-gradient'>Premier League Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown(
    f"<div class='subtitle'>Kompleksowe analizy, wizualizacje i predykcje dla sezonu <b>{selected_season}</b></div>", 
    unsafe_allow_html=True
)

# Obliczanie metryk dla kart KPI
total_matches = len(df_matches)
total_goals = df_matches["TotalGoals"].sum()
avg_goals_match = df_matches["TotalGoals"].mean()
home_wins_pct = (len(df_matches[df_matches["FTR"] == "H"]) / total_matches) * 100
avg_cards_match = df_matches["TotalCards"].mean()

# Wyświetlanie kart KPI
st.markdown(f"""
<div class='kpi-container'>
    <div class='kpi-card'>
        <div class='kpi-value'>{total_matches}</div>
        <div class='kpi-label'>Mecze w sezonie</div>
    </div>
    <div class='kpi-card'>
        <div class='kpi-value'>{total_goals}</div>
        <div class='kpi-label'>Suma bramek</div>
    </div>
    <div class='kpi-card' style='border-top-color: #0284c7;'>
        <div class='kpi-value'>{avg_goals_match:.2f}</div>
        <div class='kpi-label'>Średnia goli / mecz</div>
    </div>
    <div class='kpi-card' style='border-top-color: #f59e0b;'>
        <div class='kpi-value'>{home_wins_pct:.1f}%</div>
        <div class='kpi-label'>Zwycięstwa gospodarzy</div>
    </div>
    <div class='kpi-card' style='border-top-color: #ef4444;'>
        <div class='kpi-value'>{avg_cards_match:.2f}</div>
        <div class='kpi-label'>Średnia kartek / mecz</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tworzenie zakładek
tab_table, tab_team, tab_ref, tab_stats, tab_pred, tab_map = st.tabs([
    "📈 Tabela & Wyścig", 
    "🛡️ Profil Drużyny", 
    "⚖️ Analiza Sędziowska", 
    "📊 Statystyki & Korelacje", 
    "🔮 Symulator Poissona", 
    "🗺️ Mapa Stadionów"
])

# ==============================================================================
# TAB 1: TABELA LIGOWA & POSTĘPY SEZONU
# ==============================================================================
with tab_table:
    st.markdown("<div class='section-header'>Tabela Ligowa Premier League</div>", unsafe_allow_html=True)
    
    # Generowanie i wyświetlanie tabeli ligowej
    league_table = generate_league_table(df_matches)
    
    # Prezentujemy tabelę w elegancki sposób
    st.dataframe(
        league_table[[
            "Pozycja", "Klub", "Mecze", "Punkty", "Zwycięstwa", "Remisy", "Porażki", 
            "Bramki Zdobyte", "Bramki Stracone", "Bilans Bramek", "Forma (5 ostatnich)"
        ]],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("<div class='section-header'>Wyścig po Mistrzostwo i Utrzymanie (Skumulowane Punkty)</div>", unsafe_allow_html=True)
    st.markdown("Wybierz zespoły, aby prześledzić jak zmieniał się ich dorobek punktowy kolejka po kolejce.")
    
    # 2. Widget multiselect (Wyszukiwanie i wybór zespołów do wykresu liniowego)
    all_teams = sorted(league_table["Klub"].unique())
    # Domyślnie zaznaczamy czołówkę z tabeli
    default_selected = all_teams[:4] if len(all_teams) >= 4 else all_teams
    selected_teams = st.multiselect("Zespoły do analizy:", options=all_teams, default=default_selected)
    
    if selected_teams:
        # Obliczanie skumulowanych punktów mecz po meczu
        df_sorted = df_matches.sort_values(by="Date_Parsed")
        cumulative_data = []
        
        for team in selected_teams:
            team_matches = df_sorted[(df_sorted["HomeTeam"] == team) | (df_sorted["AwayTeam"] == team)].copy()
            # Punkty za każdy mecz
            points = []
            for idx, row in team_matches.iterrows():
                is_home = row["HomeTeam"] == team
                res = row["FTR"]
                if res == "D":
                    points.append(1)
                elif (res == "H" and is_home) or (res == "A" and not is_home):
                    points.append(3)
                else:
                    points.append(0)
            
            # Skumulowana suma
            cum_points = np.cumsum(points)
            # Dodajemy punkt 0 na początku sezonu
            cum_points = np.insert(cum_points, 0, 0)
            
            for match_num, pts in enumerate(cum_points):
                cumulative_data.append({
                    "Klub": team,
                    "Kolejka": match_num,
                    "Punkty": int(pts)
                })
                
        df_cum = pd.DataFrame(cumulative_data)
        
        # Wykres 1: LINIOWY (Line Chart)
        fig_line = px.line(
            df_cum,
            x="Kolejka",
            y="Punkty",
            color="Klub",
            title="Skumulowany dorobek punktowy w trakcie sezonu",
            labels={"Kolejka": "Rozegrane mecze", "Punkty": "Punkty skumulowane"},
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig_line.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        fig_line.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
        fig_line.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
        
        st.plotly_chart(fig_line, use_container_width=True)
        
        st.markdown("""
        <div class='commentary-box'>
            <b>Komentarz analityczny:</b> Wykres liniowy przedstawia tempo zdobywania punktów przez wybrane drużyny. 
            Strome odcinki linii oznaczają serie zwycięstw, natomiast spłaszczenia obrazują kryzysy formy lub serie porażek. 
            Pozwala to zaobserwować kluczowe momenty zwrotne w walce o mistrzostwo lub utrzymanie.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Proszę wybrać co najmniej jedną drużynę do wyświetlenia wykresu postępu.")

# ==============================================================================
# TAB 2: PROFIL I ANALIZA DRUŻYNY
# ==============================================================================
with tab_team:
    st.markdown("<div class='section-header'>Szczegółowa Analiza Drużyny</div>", unsafe_allow_html=True)
    
    # 3. Widget selectbox (Wybór zespołu do profilu)
    profile_team = st.selectbox("Wybierz klub:", options=all_teams)
    
    # Pobieranie danych o stadionie
    stadium_info = get_stadium_info(profile_team)
    
    # Wyciąganie statystyk zespołu z tabeli ligowej
    team_stats = league_table[league_table["Klub"] == profile_team].iloc[0]
    
    # Statystyki z meczów
    team_home_matches = df_matches[df_matches["HomeTeam"] == profile_team]
    team_away_matches = df_matches[df_matches["AwayTeam"] == profile_team]
    
    col_info, col_charts = st.columns([1, 2])
    
    with col_info:
        st.markdown(f"### 🛡️ {profile_team}")
        st.markdown(f"**Stadion:** {stadium_info['stadium']}")
        st.markdown(f"**Miasto:** {stadium_info['city']}")
        st.markdown(f"**Pojemność:** {stadium_info['capacity']:,} miejsc")
        st.markdown("---")
        
        # Lokalne KPI dla profilu
        st.metric("Pozycja w tabeli", f"{team_stats['Pozycja']}.")
        
        # Bilans dom/wyjazd
        st.write(f"**Punkty zdobyte u siebie:** {team_stats['Pkt Domowe']} pkt "
                 f"(Bilans: {team_stats['Zwycięstwa Dom']}-{team_stats['Remisy Dom']}-{team_stats['Porażki Dom']})")
        st.write(f"**Punkty zdobyte na wyjeździe:** {team_stats['Pkt Wyjazdowe']} pkt "
                 f"(Bilans: {team_stats['Zwycięstwa Wyjazd']}-{team_stats['Remisy Wyjazd']}-{team_stats['Porażki Wyjazd']})")
        
        # Forma w postaci kółeczek
        st.markdown("**Forma (od najstarszego do najnowszego):**")
        form_letters = team_stats["Forma (5 ostatnich)"].split()
        badge_html = ""
        for letter in form_letters:
            cls = "form-z" if letter == "Z" else ("form-r" if letter == "R" else "form-p")
            badge_html += f"<span class='form-badge {cls}'>{letter}</span>"
        st.markdown(badge_html, unsafe_allow_html=True)
        
    with col_charts:
        # Przygotowanie danych do wykresu bramkowego
        g_scored_home = team_home_matches["FTHG"].sum()
        g_conceded_home = team_home_matches["FTAG"].sum()
        g_scored_away = team_away_matches["FTAG"].sum()
        g_conceded_away = team_away_matches["FTHG"].sum()
        
        categories = ["Mecze Domowe", "Mecze Wyjazdowe"]
        
        # Wykres 2: SŁUPKOWY (Bar Chart) - Bramki zdobyte i stracone (Dom vs Wyjazd)
        fig_bar_goals = go.Figure(data=[
            go.Bar(name="Bramki Zdobyte", x=categories, y=[g_scored_home, g_scored_away], marker_color="#10b981"),
            go.Bar(name="Bramki Stracone", x=categories, y=[g_conceded_home, g_conceded_away], marker_color="#ef4444")
        ])
        fig_bar_goals.update_layout(
            title=f"Bilans bramkowy zespołu {profile_team} (Dom vs Wyjazd)",
            barmode="group",
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_bar_goals, use_container_width=True)
        
    # Ostatnie mecze zespołu w tabelce
    st.markdown("#### Ostatnie mecze w wybranym sezonie")
    team_all_matches = df_matches[
        (df_matches["HomeTeam"] == profile_team) | (df_matches["AwayTeam"] == profile_team)
    ].sort_values(by="Date_Parsed", ascending=False)
    
    # Formacik tabeli ostatnich meczów
    def format_match_row(row):
        is_home = row["HomeTeam"] == profile_team
        opponent = row["AwayTeam"] if is_home else row["HomeTeam"]
        place = "Dom" if is_home else "Wyjazd"
        score = f"{row['FTHG']}:{row['FTAG']}"
        
        # Wynik dla profilowanej drużyny
        res = row["FTR"]
        if res == "D":
            outcome = "Remis"
        elif (res == "H" and is_home) or (res == "A" and not is_home):
            outcome = "Wygrana"
        else:
            outcome = "Porażka"
            
        return {
            "Data": row["Date_Parsed"].strftime("%Y-%m-%d"),
            "Gdzie": place,
            "Przeciwnik": opponent,
            "Wynik": score,
            "Rezultat": outcome,
            "Strzały (nasze-rywala)": f"{row['HS'] if is_home else row['AS']}-{row['AS'] if is_home else row['HS']}",
            "Kartki (nasze-rywala)": f"{row['HY'] + row['HR'] if is_home else row['AY'] + row['AR']}-{row['AY'] + row['AR'] if is_home else row['HY'] + row['HR']}",
            "Sędzia": row["Referee"]
        }
        
    formatted_matches = [format_match_row(r) for idx, r in team_all_matches.iterrows()]
    st.dataframe(pd.DataFrame(formatted_matches), use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 3: ANALIZA SĘDZIOWSKA
# ==============================================================================
with tab_ref:
    st.markdown("<div class='section-header'>Analiza Stylu Sędziowania</div>", unsafe_allow_html=True)
    st.markdown(
        "Sprawdź, którzy arbitrzy są najbardziej rygorystyczni, a którzy pozwalają na twardszą grę. "
        "Możesz odfiltrować sędziów z małą liczbą meczów."
    )
    
    # 4. Widget slider (Filtrowanie minimalnej liczby meczów dla sędziów)
    min_ref_matches = st.slider(
        "Minimalna liczba sędziowanych meczów w sezonie:",
        min_value=1,
        max_value=30,
        value=5
    )
    
    # Agregacja statystyk sędziowskich
    ref_stats = df_matches.groupby("Referee").agg(
        Mecze=("Date", "count"),
        Faule_Mecz=("TotalFouls", "mean"),
        Zolte_Mecz=("TotalYellowCards", "mean"),
        Czerwone_Suma=("TotalRedCards", "sum")
    ).reset_index()
    
    # Filtrowanie po sliderze
    ref_stats_filtered = ref_stats[ref_stats["Mecze"] >= min_ref_matches]
    
    if len(ref_stats_filtered) > 0:
        col_ref_scatter, col_ref_box = st.columns(2)
        
        with col_ref_scatter:
            # Wykres 3: PUNKTOWY (Scatter Plot) - Średnie faule vs średnie żółte kartki
            fig_ref_scatter = px.scatter(
                ref_stats_filtered,
                x="Faule_Mecz",
                y="Zolte_Mecz",
                size="Mecze",
                hover_name="Referee",
                text="Referee",
                title="Styl arbitrów: Średnia liczba fauli vs średnia żółtych kartek",
                labels={"Faule_Mecz": "Średnia liczba fauli w meczu", "Zolte_Mecz": "Średnia żółtych kartek w meczu"},
                template="plotly_dark",
                color="Zolte_Mecz",
                color_continuous_scale="OrRd"
            )
            fig_ref_scatter.update_traces(textposition="top center")
            fig_ref_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            fig_ref_scatter.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
            fig_ref_scatter.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
            st.plotly_chart(fig_ref_scatter, use_container_width=True)
            
        with col_ref_box:
            # Wykres 4: PUDEŁKOWY (Box Plot) - Rozkład kartek pokazanych przez sędziów w poszczególnych meczach
            # Filtrujemy tylko mecze sędziowane przez wybranych w filtrze sędziów
            active_refs = ref_stats_filtered["Referee"].unique()
            df_active_ref_matches = df_matches[df_matches["Referee"].isin(active_refs)]
            
            fig_ref_box = px.box(
                df_active_ref_matches,
                x="Referee",
                y="TotalYellowCards",
                title="Rozkład żółtych kartek w meczach dla poszczególnych sędziów",
                labels={"Referee": "Sędzia", "TotalYellowCards": "Liczba żółtych kartek w meczu"},
                template="plotly_dark",
                color="Referee",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_ref_box.update_layout(
                showlegend=False, 
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)"
            )
            fig_ref_box.update_xaxes(tickangle=45, showgrid=True, gridwidth=1, gridcolor="#334155")
            fig_ref_box.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
            st.plotly_chart(fig_ref_box, use_container_width=True)
            
        st.markdown("""
        <div class='commentary-box'>
            <b>Komentarz analityczny:</b> Wykres punktowy pozwala zidentyfikować sędziów o różnej charakterystyce:
            lewy dolny róg to sędziowie liberalni (mało fauli, mało kartek), prawy górny róg to sędziowie restrykcyjni 
            (często przerywają grę i chętnie sięgają do kieszeni). Wykres pudełkowy (Box Plot) pokazuje wariancję zachowań 
            danego sędziego – rozpiętość "pudełka" wskazuje, czy sędzia zawsze trzyma się stałego limitu kartek, czy też 
            jego decyzje zależą mocno od temperatury konkretnego meczu.
        </div>
        """, unsafe_allow_html=True)
        
        # Wyświetlenie tabeli z sędziami
        st.markdown("#### Tabela Szczegółowa Sędziów")
        st.dataframe(
            ref_stats_filtered.rename(columns={
                "Referee": "Sędzia",
                "Mecze": "Liczba meczów",
                "Faule_Mecz": "Średnia fauli/mecz",
                "Zolte_Mecz": "Średnia żółtych kartek/mecz",
                "Czerwone_Suma": "Suma czerwonych kartek"
            }).round(2),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("Brak sędziów spełniających kryteria minimalnej liczby meczów.")

# ==============================================================================
# TAB 4: STATYSTYKI I KORELACJE
# ==============================================================================
with tab_stats:
    st.markdown("<div class='section-header'>Analiza Statystyczna i Badanie Korelacji</div>", unsafe_allow_html=True)
    
    col_controls, col_plots = st.columns([1, 3])
    
    with col_controls:
        st.markdown("### Wybór Zmiennych")
        st.markdown("Zbadaj relację między różnymi wskaźnikami meczowymi w całym sezonie.")
        
        # Mapowanie czytelnych nazw na kolumny techniczne
        metrics_dict = {
            "Gole Gospodarza": "FTHG",
            "Gole Gościa": "FTAG",
            "Suma Goli w meczu": "TotalGoals",
            "Strzały Gospodarza": "HS",
            "Strzały Gościa": "AS",
            "Suma Strzałów w meczu": "TotalShots",
            "Strzały Celne Gospodarza": "HST",
            "Strzały Celne Gościa": "AST",
            "Faule Gospodarza": "HF",
            "Faule Gościa": "AF",
            "Suma Fauli w meczu": "TotalFouls",
            "Rzuty Rożne Gospodarza": "HC",
            "Rzuty Rożne Gościa": "AC",
            "Żółte Kartki Gospodarza": "HY",
            "Żółte Kartki Gościa": "AY",
            "Czerwone Kartki Gospodarza": "HR",
            "Czerwone Kartki Gościa": "AR"
        }
        
        # 5. Widgety selectbox do dynamicznej korelacji X i Y
        x_label = st.selectbox("Wybierz oś X (niezależna):", options=list(metrics_dict.keys()), index=5) # Suma Strzałów
        y_label = st.selectbox("Wybierz oś Y (zależna):", options=list(metrics_dict.keys()), index=2) # Suma Goli
        
        x_col = metrics_dict[x_label]
        y_col = metrics_dict[y_label]
        
    with col_plots:
        # Wykres 5: PUNKTOWY (Scatter Plot) z linią trendu (korelacja zmiennych)
        fig_scatter_stats = px.scatter(
            df_matches,
            x=x_col,
            y=y_col,
            trendline="ols",
            trendline_color_override="#00ff87",
            title=f"Korelacja: {x_label} vs {y_label}",
            labels={x_col: x_label, y_col: y_label},
            template="plotly_dark",
            opacity=0.6,
            hover_data=["HomeTeam", "AwayTeam", "FTR"]
        )
        fig_scatter_stats.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        fig_scatter_stats.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
        fig_scatter_stats.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
        
        st.plotly_chart(fig_scatter_stats, use_container_width=True)
        
        # Obliczanie współczynnika korelacji Pearsona
        corr_val = df_matches[x_col].corr(df_matches[y_col])
        st.write(f"**Współczynnik korelacji liniowej Pearsona ($r$):** `{corr_val:.3f}`")
        if abs(corr_val) > 0.7:
            st.info("Korelacja silna. Zmienne wykazują bardzo silny związek liniowy.")
        elif abs(corr_val) > 0.4:
            st.info("Korelacja umiarkowana. Zauważalna jest tendencja wzrostowa/spadkowa.")
        else:
            st.info("Korelacja słaba. Czynniki te nie są bezpośrednio skorelowane liniowo.")
            
    st.markdown("---")
    
    col_pie, col_hist = st.columns(2)
    
    with col_pie:
        # Wykres 6: KOŁOWY / DONUT (Pie/Donut Chart) - Rozkład rezultatów
        res_counts = df_matches["FTR_Full"].value_counts().reset_index()
        res_counts.columns = ["Rezultat", "Liczba"]
        
        fig_donut = px.pie(
            res_counts,
            names="Rezultat",
            values="Liczba",
            hole=0.4,
            title="Rozkład wyników meczów (Atut własnego boiska)",
            color="Rezultat",
            color_discrete_map={
                "Wygrana Gospodarza": "#10b981",
                "Remis": "#64748b",
                "Wygrana Gościa": "#ef4444"
            },
            template="plotly_dark"
        )
        fig_donut.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_hist:
        # Wykres 7: HISTOGRAM - Rozkład liczby goli w meczu
        fig_hist = px.histogram(
            df_matches,
            x="TotalGoals",
            nbins=10,
            title="Rozkład całkowitej liczby bramek w meczu",
            labels={"TotalGoals": "Liczba goli w meczu", "count": "Liczba spotkań"},
            template="plotly_dark",
            color_discrete_sequence=["#0284c7"]
        )
        fig_hist.update_layout(
            bargap=0.1, 
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title_text="Liczba spotkań"
        )
        fig_hist.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#334155", dtick=1)
        fig_hist.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
        st.plotly_chart(fig_hist, use_container_width=True)

# ==============================================================================
# TAB 5: SYMULATOR WYNIKÓW (POISSON MODEL)
# ==============================================================================
with tab_pred:
    st.markdown("<div class='section-header'>Predyktor Wyników na bazie Rozkładu Poissona</div>", unsafe_allow_html=True)
    st.markdown(
        "Model matematyczny analizuje siłę ofensywną i defensywną obu zespołów w bieżącym sezonie, "
        "wyznacza oczekiwaną liczbę goli (lambda) i oblicza prawdopodobieństwa dokładnych wyników."
    )
    
    col_sel1, col_sel2 = st.columns(2)
    
    with col_sel1:
        # 6. Widget selectbox (Gospodarz predictor)
        pred_home = st.selectbox("Gospodarz meczu:", options=all_teams, index=0)
    with col_sel2:
        # 6. Widget selectbox (Gość predictor)
        # Próbujemy domyślnie wybrać inną drużynę
        default_away_idx = 1 if len(all_teams) > 1 else 0
        pred_away = st.selectbox("Gość meczu:", options=all_teams, index=default_away_idx)
        
    if pred_home == pred_away:
        st.warning("Gospodarz i gość muszą być różnymi zespołami!")
    else:
        # Obliczenie prognozy
        pred_results = predict_match_outcome(df_matches, pred_home, pred_away)
        
        col_pred_stats, col_pred_heatmap = st.columns([2, 3])
        
        with col_pred_stats:
            st.markdown(f"### Analiza Szans: {pred_home} vs {pred_away}")
            st.write(f"**Oczekiwana liczba goli gospodarza ($\lambda_{{dom}}$):** `{pred_results['expected_home_goals']}`")
            st.write(f"**Oczekiwana liczba goli gościa ($\lambda_{{wyjazd}}$):** `{pred_results['expected_away_goals']}`")
            st.write("---")
            
            # Paski prawdopodobieństw (1 X 2)
            st.markdown("#### Prawdopodobieństwa rezultatów (1X2):")
            
            prob_home = pred_results["home_win_prob"]
            prob_draw = pred_results["draw_prob"]
            prob_away = pred_results["away_win_prob"]
            
            st.write(f"🟢 **Wygrana {pred_home}:** {prob_home}%")
            st.progress(prob_home / 100)
            
            st.write(f"⚪ **Remis:** {prob_draw}%")
            st.progress(prob_draw / 100)
            
            st.write(f"🔴 **Wygrana {pred_away}:** {prob_away}%")
            st.progress(prob_away / 100)
            
            st.write("---")
            most_likely_h, most_likely_a = pred_results["most_likely_score"]
            st.markdown(
                f"<div style='background-color: rgba(0, 255, 135, 0.1); border: 1px solid #00ff87; padding: 1rem; border-radius: 8px; text-align: center;'>"
                f"🎯 <b>Najbardziej prawdopodobny wynik:</b> <span style='font-size: 1.5rem; font-weight: 800; color: #00ff87;'>"
                f"{most_likely_h} : {most_likely_a}</span><br/>"
                f"(Prawdopodobieństwo: <b>{pred_results['most_likely_prob']}%</b>)"
                f"</div>",
                unsafe_allow_html=True
            )
            
        with col_pred_heatmap:
            # Wykres 8: MAPA CIEPŁA (Heatmap) - Prawdopodobieństwa dokładnych rezultatów
            matrix = pred_results["score_matrix"]
            max_goals_range = list(range(matrix.shape[0]))
            
            # Konwersja na procenty dla tooltipu
            matrix_pct = np.round(matrix * 100, 2)
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=matrix_pct,
                x=[f"{g} goli gościa" for g in max_goals_range],
                y=[f"{g} goli gosp." for g in max_goals_range],
                colorscale="Viridis",
                text=matrix_pct,
                texttemplate="%{text}%",
                hoverongaps=False
            ))
            
            fig_heatmap.update_layout(
                title=f"Macierz prawdopodobieństwa wyniku ({pred_home} - {pred_away})",
                xaxis_title="Gole drużyny gości",
                yaxis_title="Gole drużyny gospodarzy",
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
        st.markdown("""
        <div class='commentary-box'>
            <b>Komentarz matematyczny:</b> Symulacja opiera się na założeniu niezależności liczby strzelonych goli 
            przez oba zespoły. Siła ataku i obrony wyznaczana jest na podstawie rozegranych meczów w bieżącym sezonie. 
            Rozkład Poissona doskonale modeluje rozkład rzadkich zdarzeń (jakimi są bramki w meczu piłkarskim) i jest 
            powszechnie wykorzystywany przez firmy bukmacherskie oraz analityków sportowych do szacowania szans meczowych.
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 6: INTERAKTYWNA MAPA STADIONÓW
# ==============================================================================
with tab_map:
    st.markdown("<div class='section-header'>Mapa Geograficzna Stadionów Premier League</div>", unsafe_allow_html=True)
    st.markdown(
        "Lokalizacja stadionów wszystkich zespołów uczestniczących w wybranym sezonie. "
        "Rozmiar koła reprezentuje pojemność stadionu."
    )
    
    # Tworzenie zbioru danych dla mapy na podstawie drużyn wybranego sezonu
    active_teams = set(df_matches["HomeTeam"].unique()).union(set(df_matches["AwayTeam"].unique()))
    
    map_data = []
    for team in active_teams:
        info = get_stadium_info(team)
        
        # Obliczenie średniej liczby punktów zdobytych u siebie przez daną drużynę
        home_games = df_matches[df_matches["HomeTeam"] == team]
        avg_home_goals = home_games["FTHG"].mean() if len(home_games) > 0 else 0
        total_home_pts = home_games["Points_Home"].sum()
        
        map_data.append({
            "Klub": team,
            "Stadion": info["stadium"],
            "Miasto": info["city"],
            "Pojemność": info["capacity"],
            "Latitude": info["lat"],
            "Longitude": info["lon"],
            "Śr. gole gospodarza": round(avg_home_goals, 2),
            "Suma pkt domowych": int(total_home_pts)
        })
        
    df_map = pd.DataFrame(map_data)
    
    # Wykres 9: MAPA GEOGRAFICZNA (Scatter Mapbox)
    fig_map = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="Pojemność",
        color="Suma pkt domowych",
        color_continuous_scale="Viridis",
        hover_name="Klub",
        hover_data={
            "Stadion": True,
            "Miasto": True,
            "Pojemność": ":,",
            "Śr. gole gospodarza": True,
            "Suma pkt domowych": True,
            "Latitude": False,
            "Longitude": False
        },
        zoom=5.3,
        height=650,
        title="Rozmieszczenie stadionów Premier League i punkty zdobyte u siebie",
        template="plotly_dark"
    )
    
    # Użycie darmowego stylu OpenStreetMap
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("""
    <div class='commentary-box'>
        <b>Komentarz geograficzny:</b> Mapa przedstawia rozkład terytorialny klubów Premier League. 
        Można zaobserwować wyraźne zagęszczenie klubów w aglomeracji londyńskiej oraz w pasie północno-zachodnim 
        (Liverpool, Manchester). Rozmiar punktu jest proporcjonalny do pojemności stadionu, natomiast kolor 
        odzwierciedla sumaryczny dorobek punktowy wywalczony przed własną publicznością w tym sezonie.
    </div>
    """, unsafe_allow_html=True)
