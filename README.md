# Metric TSP: Exact Held-Karp vs 1.5-Approximation Christofides Benchmark

> **Analiza teoretyczna i badania empiryczne złożoności algorytmów dla problemu komiwojażera**  
> **Przedmiot:** Techniki Algorytmiczne  
> **Uczelnia:** Wojskowa Akademia Techniczna (WAT), Wydział Cybernetyki  
> **Autorzy:** Stanisław Gołębiewski, Dominik Matusiak  

---

## 📌 Opis Problemu

Projekt stanowi studium problemu komiwojażera (**Traveling Salesperson Problem – TSP**) w wariancie symetrycznym i metrycznym (odległości euklidesowe na płaszczyźnie 2D spełniające nierówność trójkąta).

Zaimplementowano i porównano dwa fundamentalne paradygmaty rozwiązywania problemów NP-trudnych:
1. **Algorytm dokładny (Exact):** Programowanie dynamiczne **Held-Karp** z maskami bitowymi.
2. **Algorytm aproksymacyjny (Heuristic):** Heurystyka bazująca na idei **Christofidesa** z zachłannym skojarzeniem wierzchołków o nieparzystym stopniu w Minimalnym Drzewie Rozpinającym (MST).

Oprócz samej implementacji przeprowadzono kalibrację stałych sprzętowych oraz formalne porównanie złożoności teoretycznej z wynikami pomiarów czasu procesora (`perf_counter`) i alokacji pamięci operacyjnej (`tracemalloc`).

---

## 🔬 Zastosowane Algorytmy

### 1. Algorytm Held-Karp (Programowanie Dynamiczne)
- **Mechanizm:** Zamiast przeszukiwania przestrzeni permutacji brute-force ($O(n!)$), algorytm dzieli zadanie na podproblemy: wyznaczenie najkrótszej ścieżki odwiedzającej dany podzbiór wierzchołków $S$ kończącej się w wierzchołku $j$.
- **Implementacja:** 
  - Maski bitowe (bit integers) do bezkonfliktowej, szybkiej reprezentacji zbiorów odwiedzonych miast.
  - Słownik stanów dynamicznych `dp[(mask, j)] = min_cost`.
  - Rekonstrukcja optymalnej trasy za pomocą słownika rodziców `parent[(mask, j)]`.
- **Złożoność:**
  - Czasowa: $O(n^2 \cdot 2^n)$
  - Pamięciowa: $O(n \cdot 2^n)$
  - Dokładność: **100% (rozwiązanie optymalne)**

### 2. Algorytm Heurystyczny (Zbliżony do Christofidesa)
- **Kroki algorytmu:**
  1. Wyznaczenie Minimalnego Drzewa Rozpinającego (**MST**) algorytmem Prima.
  2. Identyfikacja podzbioru wierzchołków o stopniu nieparzystym $V_{odd}$.
  3. Zachłanne skojarzenie par wierzchołków (**Greedy Matching**) o minimalnych wagach krawędzi i włączenie ich do multigrafu.
  4. Wyznaczenie cyklu Eulera w powstałym multigrafie parzystym.
  5. Konwersja do cyklu Hamiltona poprzez skróty (**shortcutting** – omijanie wierzchołków już odwiedzonych).
- **Złożoność:**
  - Czasowa: $O(n^3)$ (lub $O(n^2)$ z optymalizacjami)
  - Pamięciowa: $O(n^2)$
  - Gwarancja teoretyczna: błąd względny $\le 50\%$ względem optimum.

---

## 📊 Wyniki Badań Empirycznych

Pomiary wykonane dla instancji testowych o rozmiarach $n \in [10, 14]$ miast (kalibracja stałych sprzętowych dla punktu odniesienia $n=10$):

### 1. Czas Wykonania (Held-Karp vs Christofides)
| $n$ | Czas Held-Karp [s] | Teoria HK [s] | Współczynnik | Czas Christofides [s] | Teoria CHR [s] | Współczynnik |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10** | 0.0134 | 0.0134 | 1.00 | 0.00025 | 0.00025 | 1.00 |
| **11** | 0.0253 | 0.0323 | 0.78 | 0.00022 | 0.00033 | 0.66 |
| **12** | 0.0664 | 0.0770 | 0.86 | 0.00027 | 0.00043 | 0.64 |
| **13** | 0.1534 | 0.1806 | 0.85 | 0.00028 | 0.00054 | 0.52 |
| **14** | 0.3534 | 0.4190 | 0.84 | 0.00034 | 0.00067 | 0.51 |

### 2. Zużycie Pamięci RAM (Peak Allocation)
| $n$ | Pamięć Held-Karp [KB] | Pamięć Christofides [KB] |
| :---: | :---: | :---: |
| **10** | 494.3 KB | 4.9 KB |
| **11** | 945.8 KB | 6.5 KB |
| **12** | 2 991.0 KB | 7.4 KB |
| **13** | 6 364.4 KB | 8.4 KB |
| **14** | 13 145.5 KB (~13 MB) | 9.4 KB |

*Zgodnie z przewidywaniami teoretycznymi, zużycie pamięci w Held-Karp podwaja się z każdym dodanym miastem ze względu na $2^n$ podzbiorów bitowych, podczas gdy heurystyka zachowuje niemal płaski profil zużycia zasobów.*

### 3. Jakość Rozwiązania (Aproximation Gap)
| $n$ | Koszt Optimum (Held-Karp) | Koszt Heurystyki | Błąd względny (Gap %) |
| :---: | :---: | :---: | :---: |
| **10** | 2641.39 | 2754.67 | **4.29%** |
| **11** | 2721.44 | 2834.56 | **4.16%** |
| **12** | 2722.49 | 2871.14 | **5.46%** |
| **13** | 2755.17 | 3046.84 | **10.59%** |
| **14** | 2849.06 | 3106.24 | **9.03%** |

*W badaniach empirycznych heurystyka uzyskuje średnio odchylenie na poziomie 4-10% od optimum globalnego, znacznie przewyższając pesymistyczną gwarancję teoretyczną 50%.*

---

## 📁 Struktura Projektu

- `christofides.py` – Implementacja algorytmu aproksymacyjnego z zachłannym skojarzeniem
- `heldKarp.py` – Implementacja dokładnego programowania dynamicznego z maskami bitowymi
- `distance.py` – Obliczanie macierzy odległości euklidesowych w przestrzeni 2D
- `generator.py` – Deterministyczny generator losowych instancji miast (`seed`)
- `metrics.py` – Profiler czasu (`time.perf_counter`) i alokacji pamięci (`tracemalloc`)
- `theory.py` – Model kalibracji stałych asymptotycznych i predykcji teoretycznych
- `experiment.py` – Środowisko uruchomieniowe serii eksperymentów
- `main.py` – Główny skrypt generujący tabele podsumowujące

---

## 🚀 Uruchomienie

Projekt nie wymaga instalacji żadnych zewnętrznych bibliotek (wykorzystuje wyłącznie standardową bibliotekę Pythona).

```bash
python main.py
```

---

## 📜 Licencja
Projekt dydaktyczno-naukowy zrealizowany w ramach studiów na Wydziale Cybernetyki WAT.
