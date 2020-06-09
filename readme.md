# System automatycznej obsługi sprzedaży i kupna pojazdów elektrycznych

## Wstęp
Prototyp projektu zaprojektowany na potrzeby prezentacji z dokumentacją.

## Elementy zawarte
Prototyp poprawnie łączy się z bazą danych. Obsługuje logowanie oraz rejestrację. Dodatkowo opcje związane z dodaniem oferty są w pełni funkcjonalne. Główna strona wyświetlana zaraz po wejściu na stronę jest funkcjonalna i pobiera oferty z bazy. Ankieta przypisana do użytkownika zapisuje sie w bazie danych i jest egzekwowana podczas wyświetlania ofert na stronie głównej tzn. gdy uzupełnimy, że interesują nas Toyoty, rocznik 2000-2020, w przedziale 1000 - 10000zł, takie zostaną nam wyświetlone. Dodatkowo opcje związane ze zmianą hasła są funkcjonalne

## Elementy potrzebne
By uruchomić serwis potrzebujemy:

1. Python 3.8.3
2. Usługę pip domyślnie instalowaną w pakietach python-windows, w przypadku linuxa trzeba zainstalować ręcznie
3. Plik config.py dorzucony do głównego folderu projektu tzn. tam gdzie znajduje się plik strona.py

## Plik config.py
Przykładowy plik config.py:

```python
host="db_server_url"
user="username"
passwd="password"
database="database on server"
```

## Instalacja bibliotek

By zainstalować biblioteki należy wykonać polecenie
```bash
pip install -r requirements.txt
```

## Uruchomienie

By uruchomić należy wykonać plik strona.py tzn. wpisać w konsole:

```bash
python strona.py
```

Następnie serwer lokalny zostanie uruchomiony, a serwis zagnieździ się na porcie 5000. Należy wtedy wpisać w przeglądarkę:

```
127.0.0.1:5000
```