# Współczynniki prestiżu stron WWW

1. Założenie: Dany jest graf skierowany w postaci listy incydencji, dotyczący fragmentu sieci WWW. Każdy dokument WWW (wierzchołek grafu) jest opisany za pomocą ciągu znaków, np.:
```
strona A: strona B, strona C
strona B: strona C
strona C:
```

2. Obliczanie współczynników prestiżu.
    - Współczynniki prestiżu stron są wyznaczane na podstawie wektora własnego macierzy reprezentującej graf.
    - Aplikacja powinna wypisać obliczone współczynniki prestiżu dla każdej strony WWWoraz umożliwiać sortowania stron względem ich prestiżu. 

3. Dodatkowe opcje do implementacji (za każdą pół oceny więcej):
    - Wizualizacja stworzonego grafu wraz z obliczonymi współczynnikami prestiżu.
    - Możliwość graficznego tworzenia grafu stron WWW.
    - Wizualizacja macierzy sąsiedztwa przestawiającej graf.
    - Zaproponować i zaimplementować algorytm wyliczania współczynników stron. Algorytmmoże wykorzystywać wzory, które pojawiły się na zajęciach pt. Ranking stron WWW na bazie linków. 