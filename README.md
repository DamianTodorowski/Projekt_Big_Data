# ⚽ Premier League Analytics Dashboard

Interaktywna aplikacja analityczna (dashboard) napisana w języku Python z użyciem biblioteki **Streamlit** oraz **Plotly**. Aplikacja prezentuje szczegółowe statystyki, tabele, rozkład sędziowski, analizy korelacji oraz moduł symulacyjny dla angielskiej Premier League z ostatnich 5 sezonów (od 2021/22 do 2025/26).

##  Działająca wersja (Deployment)
Aplikacja została wdrożona na platformie Streamlit Community Cloud i jest dostępna pod poniższym adresem:
 **[https://premierleaguedash.streamlit.app](https://premierleaguedash.streamlit.app)**

---

## 📊 Główne Funkcjonalności i Cechy
Projekt w pełni spełnia (i rozszerza) wymagania techniczne pracy zaliczeniowej:

1. **Prawdziwe źródło danych**: Statystyki meczów pobierane są automatycznie ze znanego portalu [football-data.co.uk](https://www.football-data.co.uk/).
2. **Czyszczenie i transformacja danych**:
   - Obsługa formatów dat i ujednolicenie (dwa formaty zapisu roku).
   - Usuwanie pustych wierszy i wartości anomalnych.
   - Kolumny pochodne (łączna liczba strzałów, fauli, kartek, punkty, polskie opisy wyników).
   - Cache'owanie danych z użyciem `@st.cache_data` z automatycznym zapisem pobranych plików w lokalnym folderze `data/` w celu optymalizacji wydajności i działania offline.
3. **Różnorodność wizualizacji (9 wykresów, 7 różnych typów)**:
   - **Wykres Liniowy (Line Chart)**: skumulowany dorobek punktowy zespołów w trakcie sezonu.
   - **Wykres Słupkowy (Bar Chart)**: bilans bramek zdobytych i straconych u siebie i na wyjeździe.
   - **Wykresy Punktowe (Scatter Plot)**:
     - Styl arbitrów (średnia liczba fauli vs średnia kartek).
     - Korelacje statystyk meczowych (np. strzały celne vs bramki) wraz z wyznaczoną **linią trendu OLS** oraz współczynnikiem korelacji Pearsona.
   - **Wykres Pudełkowy (Box Plot)**: rozkład żółtych kartek u poszczególnych sędziów.
   - **Wykres Kołowy (Donut Chart)**: procentowy rozkład wyników meczów (Home/Draw/Away).
   - **Histogram**: rozkład całkowitej liczby bramek w meczu.
   - **Mapa Ciepła (Heatmap)**: rozkład prawdopodobieństw dokładnego wyniku meczu w symulatorze.
   - **Wykres Geograficzny (Scatter Mapbox)**: interaktywna mapa stadionów z rozmiarem odpowiadającym pojemności i kolorem odzwierciedlającym punkty zdobycz domową.
4. **Interaktywność (6 widgetów filtrujących)**:
   - Wybór sezonu (`selectbox`).
   - Wybór wielu drużyn do porównania postępów (`multiselect`).
   - Wybór klubu do profilu szczegółowego (`selectbox`).
   - Filtr minimalnej liczby meczów dla sędziów (`slider`).
   - Wybór zmiennych osi X i Y w analizie korelacji (`selectbox`).
   - Wybór gospodarza i gościa w kalkulatorze wyników (`selectbox`).
5. **Kalkulator Wyników oparty na Rozkładzie Poissona**: Matematyczna symulacja szans meczowych za pomocą rozkładu prawdopodobieństwa na podstawie siły ofensywnej/defensywnej zespołów.

---

## 🛠️ Jak uruchomić projekt lokalnie

### Wymagania
Upewnij się, że masz zainstalowanego Pythona (zalecana wersja 3.9 lub nowsza).

### Krok 1: Sklonuj repozytorium
```bash
git clone https://github.com/twoj-profil/nazwa-repozytorium.git
cd nazwa-repozytorium
```

### Krok 2: Zainstaluj zależności
Możesz zainstalować wymagane pakiety za pomocą pip:
```bash
pip install -r requirements.txt
```
*(Wymagane biblioteki: `streamlit`, `pandas`, `plotly`, `requests`, `numpy`)*

### Krok 3: Uruchom aplikację Streamlit
```bash
streamlit run app.py
```
Aplikacja powinna automatycznie otworzyć się w Twojej przeglądarce pod adresem `http://localhost:8501`.

---

## 📂 Struktura plików w projekcie
```text
├── .streamlit/
│   └── config.toml      # Konfiguracja ciemnego motywu wizualnego
├── data/                # Lokalny cache plików CSV (pobrane automatycznie)
├── app.py               # Główny plik aplikacji i interfejsu Streamlit
├── data_loader.py       # Pobieranie, oczyszczanie i transformacja danych, generowanie tabeli
├── predictor.py         # Logika symulacji Poissona (siła zespołów, macierz prawdopodobieństw)
├── stadiums.py          # Baza współrzędnych i pojemności stadionów Premier League
├── requirements.txt     # Plik zależności bibliotek Pythona
├── test_data.py         # Skrypt testów jednostkowych/logicznych
└── README.md            # Opis projektu (ten plik)
```
