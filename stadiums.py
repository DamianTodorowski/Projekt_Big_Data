# -*- coding: utf-8 -*-

# Słownik zawierający dane o stadionach zespołów Premier League
# Współrzędne geograficzne pozwalają na dokładne umieszczenie na mapie (Plotly Mapbox)
STADIUMS_DB = {
    "Arsenal": {
        "stadium": "Emirates Stadium",
        "city": "Londyn",
        "capacity": 60704,
        "lat": 51.5549,
        "lon": -0.1084
    },
    "Aston Villa": {
        "stadium": "Villa Park",
        "city": "Birmingham",
        "capacity": 42682,
        "lat": 52.5091,
        "lon": -1.8848
    },
    "Brentford": {
        "stadium": "Gtech Community Stadium",
        "city": "Londyn",
        "capacity": 17250,
        "lat": 51.4908,
        "lon": -0.3031
    },
    "Brighton": {
        "stadium": "Amex Stadium",
        "city": "Brighton",
        "capacity": 31876,
        "lat": 50.8618,
        "lon": -0.0837
    },
    "Brighton & Hove Albion": {
        "stadium": "Amex Stadium",
        "city": "Brighton",
        "capacity": 31876,
        "lat": 50.8618,
        "lon": -0.0837
    },
    "Burnley": {
        "stadium": "Turf Moor",
        "city": "Burnley",
        "capacity": 21944,
        "lat": 53.7890,
        "lon": -2.2302
    },
    "Chelsea": {
        "stadium": "Stamford Bridge",
        "city": "Londyn",
        "capacity": 40341,
        "lat": 51.4817,
        "lon": -0.1910
    },
    "Crystal Palace": {
        "stadium": "Selhurst Park",
        "city": "Londyn",
        "capacity": 25486,
        "lat": 51.3983,
        "lon": -0.0854
    },
    "Everton": {
        "stadium": "Goodison Park",
        "city": "Liverpool",
        "capacity": 39572,
        "lat": 53.4388,
        "lon": -2.9664
    },
    "Fulham": {
        "stadium": "Craven Cottage",
        "city": "Londyn",
        "capacity": 29600,
        "lat": 51.4750,
        "lon": -0.2217
    },
    "Leeds": {
        "stadium": "Elland Road",
        "city": "Leeds",
        "capacity": 37792,
        "lat": 53.7778,
        "lon": -1.5731
    },
    "Leeds United": {
        "stadium": "Elland Road",
        "city": "Leeds",
        "capacity": 37792,
        "lat": 53.7778,
        "lon": -1.5731
    },
    "Leicester": {
        "stadium": "King Power Stadium",
        "city": "Leicester",
        "capacity": 32261,
        "lat": 52.6203,
        "lon": -1.1422
    },
    "Leicester City": {
        "stadium": "King Power Stadium",
        "city": "Leicester",
        "capacity": 32261,
        "lat": 52.6203,
        "lon": -1.1422
    },
    "Liverpool": {
        "stadium": "Anfield",
        "city": "Liverpool",
        "capacity": 61276,
        "lat": 53.4308,
        "lon": -2.9608
    },
    "Man City": {
        "stadium": "Etihad Stadium",
        "city": "Manchester",
        "capacity": 53400,
        "lat": 53.4831,
        "lon": -2.2002
    },
    "Manchester City": {
        "stadium": "Etihad Stadium",
        "city": "Manchester",
        "capacity": 53400,
        "lat": 53.4831,
        "lon": -2.2002
    },
    "Man United": {
        "stadium": "Old Trafford",
        "city": "Manchester",
        "capacity": 74310,
        "lat": 53.4631,
        "lon": -2.2913
    },
    "Manchester United": {
        "stadium": "Old Trafford",
        "city": "Manchester",
        "capacity": 74310,
        "lat": 53.4631,
        "lon": -2.2913
    },
    "Newcastle": {
        "stadium": "St James' Park",
        "city": "Newcastle",
        "capacity": 52305,
        "lat": 54.9756,
        "lon": -1.6217
    },
    "Newcastle United": {
        "stadium": "St James' Park",
        "city": "Newcastle",
        "capacity": 52305,
        "lat": 54.9756,
        "lon": -1.6217
    },
    "Norwich": {
        "stadium": "Carrow Road",
        "city": "Norwich",
        "capacity": 27244,
        "lat": 52.6225,
        "lon": 1.3094
    },
    "Southampton": {
        "stadium": "St Mary's Stadium",
        "city": "Southampton",
        "capacity": 32384,
        "lat": 50.9058,
        "lon": -1.3911
    },
    "Tottenham": {
        "stadium": "Tottenham Hotspur Stadium",
        "city": "Londyn",
        "capacity": 62850,
        "lat": 51.6044,
        "lon": -0.0664
    },
    "Tottenham Hotspur": {
        "stadium": "Tottenham Hotspur Stadium",
        "city": "Londyn",
        "capacity": 62850,
        "lat": 51.6044,
        "lon": -0.0664
    },
    "Watford": {
        "stadium": "Vicarage Road",
        "city": "Watford",
        "capacity": 22200,
        "lat": 51.6499,
        "lon": -0.4015
    },
    "West Ham": {
        "stadium": "London Stadium",
        "city": "Londyn",
        "capacity": 62500,
        "lat": 51.5386,
        "lon": -0.0164
    },
    "West Ham United": {
        "stadium": "London Stadium",
        "city": "Londyn",
        "capacity": 62500,
        "lat": 51.5386,
        "lon": -0.0164
    },
    "Wolves": {
        "stadium": "Molineux Stadium",
        "city": "Wolverhampton",
        "capacity": 32050,
        "lat": 52.5902,
        "lon": -2.1304
    },
    "Wolverhampton Wanderers": {
        "stadium": "Molineux Stadium",
        "city": "Wolverhampton",
        "capacity": 32050,
        "lat": 52.5902,
        "lon": -2.1304
    },
    "Bournemouth": {
        "stadium": "Vitality Stadium",
        "city": "Bournemouth",
        "capacity": 11364,
        "lat": 50.7352,
        "lon": -1.8383
    },
    "AFC Bournemouth": {
        "stadium": "Vitality Stadium",
        "city": "Bournemouth",
        "capacity": 11364,
        "lat": 50.7352,
        "lon": -1.8383
    },
    "Nott'm Forest": {
        "stadium": "City Ground",
        "city": "Nottingham",
        "capacity": 30445,
        "lat": 52.9400,
        "lon": -1.1328
    },
    "Nottingham Forest": {
        "stadium": "City Ground",
        "city": "Nottingham",
        "capacity": 30445,
        "lat": 52.9400,
        "lon": -1.1328
    },
    "Luton": {
        "stadium": "Kenilworth Road",
        "city": "Luton",
        "capacity": 12000,
        "lat": 51.8841,
        "lon": -0.4317
    },
    "Luton Town": {
        "stadium": "Kenilworth Road",
        "city": "Luton",
        "capacity": 12000,
        "lat": 51.8841,
        "lon": -0.4317
    },
    "Sheffield United": {
        "stadium": "Bramall Lane",
        "city": "Sheffield",
        "capacity": 32050,
        "lat": 53.3703,
        "lon": -1.4708
    },
    "Ipswich": {
        "stadium": "Portman Road",
        "city": "Ipswich",
        "capacity": 29673,
        "lat": 52.0551,
        "lon": 1.1448
    },
    "Ipswich Town": {
        "stadium": "Portman Road",
        "city": "Ipswich",
        "capacity": 29673,
        "lat": 52.0551,
        "lon": 1.1448
    },
    "Sunderland": {
        "stadium": "Stadium of Light",
        "city": "Sunderland",
        "capacity": 49000,
        "lat": 54.9144,
        "lon": -1.3883
    }
}

def get_stadium_info(team_name):
    """
    Zwraca słownik z danymi stadionu dla podanej drużyny.
    Jeśli drużyna nie zostanie znaleziona, zwraca domyślne dane (np. Londyn/Neutral).
    """
    return STADIUMS_DB.get(team_name, {
        "stadium": "Nieznany Stadion",
        "city": "Nieznane Miasto",
        "capacity": 15000,
        "lat": 52.5,
        "lon": -1.5
    })
