# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd

def poisson_probability(lmbda, k):
    """
    Oblicza prawdopodobieństwo otrzymania dokładnie k zdarzeń
    przy średniej częstości lmbda na jednostkę czasu/przestrzeni.
    """
    if lmbda <= 0:
        return 1.0 if k == 0 else 0.0
    try:
        return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)
    except OverflowError:
        return 0.0

def predict_match_outcome(df_matches, home_team, away_team, max_goals=6):
    """
    Prognozuje wynik meczu piłkarskiego przy użyciu modelu rozkładu Poissona.
    
    Parametry:
    - df_matches: DataFrame zawierający historię meczów wybranego sezonu.
    - home_team: Nazwa drużyny gospodarzy.
    - away_team: Nazwa drużyny gości.
    - max_goals: Maksymalna liczba bramek dla każdego zespołu analizowana w macierzy (domyślnie 6).
    
    Zwraca słownik z wynikami analizy:
    - expected_home_goals: oczekiwana liczba bramek gospodarza
    - expected_away_goals: oczekiwana liczba bramek gościa
    - home_win_prob: prawdopodobieństwo wygranej gospodarza
    - draw_prob: prawdopodobieństwo remisu
    - away_win_prob: prawdopodobieństwo wygranej gościa
    - most_likely_score: krotka (gole_gosp, gole_gosci)
    - score_matrix: macierz (numpy array) prawdopodobieństw wyników
    """
    # 1. Średnie ligowe
    avg_home_goals_league = df_matches["FTHG"].mean()
    avg_away_goals_league = df_matches["FTAG"].mean()
    
    # 2. Statystyki domowe gospodarza
    home_matches_ht = df_matches[df_matches["HomeTeam"] == home_team]
    if len(home_matches_ht) > 0:
        home_goals_scored_avg = home_matches_ht["FTHG"].mean()
        home_goals_conceded_avg = home_matches_ht["FTAG"].mean()
    else:
        # Fallback na średnie ligowe
        home_goals_scored_avg = avg_home_goals_league
        home_goals_conceded_avg = avg_away_goals_league
        
    # 3. Statystyki wyjazdowe gościa
    away_matches_at = df_matches[df_matches["AwayTeam"] == away_team]
    if len(away_matches_at) > 0:
        away_goals_scored_avg = away_matches_at["FTAG"].mean()
        away_goals_conceded_avg = away_matches_at["FTHG"].mean()
    else:
        # Fallback na średnie ligowe
        away_goals_scored_avg = avg_away_goals_league
        away_goals_conceded_avg = avg_home_goals_league

    # 4. Obliczanie sił ataku i obrony
    # Siła ataku gospodarza = gole strzelone u siebie / średnia ligowa goli strzelonych u siebie
    home_attack = home_goals_scored_avg / avg_home_goals_league if avg_home_goals_league > 0 else 1.0
    # Siła obrony gościa = gole stracone na wyjeździe / średnia ligowa goli straconych na wyjeździe (czyli strzelonych u siebie)
    away_defense = away_goals_conceded_avg / avg_home_goals_league if avg_home_goals_league > 0 else 1.0
    
    # Siła ataku gościa = gole strzelone na wyjeździe / średnia ligowa goli strzelonych na wyjeździe
    away_attack = away_goals_scored_avg / avg_away_goals_league if avg_away_goals_league > 0 else 1.0
    # Siła obrony gospodarza = gole stracone u siebie / średnia ligowa goli straconych u siebie (czyli strzelonych na wyjeździe)
    home_defense = home_goals_conceded_avg / avg_away_goals_league if avg_away_goals_league > 0 else 1.0
    
    # 5. Oczekiwana liczba bramek
    expected_home_goals = home_attack * away_defense * avg_home_goals_league
    expected_away_goals = away_attack * home_defense * avg_away_goals_league
    
    # 6. Budowanie macierzy prawdopodobieństw
    score_matrix = np.zeros((max_goals, max_goals))
    for h in range(max_goals):
        for a in range(max_goals):
            prob_h = poisson_probability(expected_home_goals, h)
            prob_a = poisson_probability(expected_away_goals, a)
            score_matrix[h, a] = prob_h * prob_a
            
    # 7. Obliczanie prawdopodobieństw 1X2
    home_win_prob = 0.0
    draw_prob = 0.0
    away_win_prob = 0.0
    
    for h in range(max_goals):
        for a in range(max_goals):
            prob = score_matrix[h, a]
            if h > a:
                home_win_prob += prob
            elif h == a:
                draw_prob += prob
            else:
                away_win_prob += prob
                
    # Skalowanie do sumy 100% (ponieważ ucinamy macierz do max_goals bramek)
    total_prob = home_win_prob + draw_prob + away_win_prob
    if total_prob > 0:
        home_win_prob /= total_prob
        draw_prob /= total_prob
        away_win_prob /= total_prob
        score_matrix = score_matrix / total_prob

    # 8. Najbardziej prawdopodobny wynik (indeksy o największym prawdopodobieństwie)
    flat_idx = np.argmax(score_matrix)
    most_likely_h, most_likely_a = np.unravel_index(flat_idx, score_matrix.shape)
    
    return {
        "expected_home_goals": round(expected_home_goals, 2),
        "expected_away_goals": round(expected_away_goals, 2),
        "home_win_prob": round(home_win_prob * 100, 1),
        "draw_prob": round(draw_prob * 100, 1),
        "away_win_prob": round(away_win_prob * 100, 1),
        "most_likely_score": (most_likely_h, most_likely_a),
        "most_likely_prob": round(score_matrix[most_likely_h, most_likely_a] * 100, 1),
        "score_matrix": score_matrix
    }
