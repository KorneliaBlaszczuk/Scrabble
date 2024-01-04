# Projekt PIPR - Gra SCRABBLE

### Autor
Kornelia Błaszczuk <br>
Studentka Informatyki I stopnia na Politechnice Warszawskiej <br>
Number Indeksu: 331361 <br>
Mail: 01187210@pw.edu.pl <br>

## Temat projektu
Przygotuj program który pozwoli grać w grę scrabble.
<br><br>
Gra polega na układaniu słów z wylosowanych klocków z literkami i dokładaniu ich do planszy tak żeby zdobyć jak najwięcej punktów. Słowa dokładać można tylko w jednym kierunku (pion lub poziom), a po dołożeniu nowego słowa wszystkie zbitki liter na planszy musza mieć sens (Zarówno w pionie jak i w poziomie).
<br><br>
W wersji piprowej proponuję uproszczenie gry do maksymalnie 5-literowych słów (w wersji z botem, żeby ułatwić przeszukiwanie słownika) i zrezygnowanie z pól z dodatkowymi premiami. Do rozwiązania zadania (stworzenia bota) należy wykorzystać słownik np: https://sjp.pl/slownik/growy/
<br><br>
Dokładne reguły, punktacja i liczba płytek z daną literą są dostępne na stronie: http://www.pfs.org.pl/reguly.php

## Cel i opis projektu
Celem projektu jest wykonanie gry SCRABBLE implementując ją z wykorzystaniem języka Python. Zrealizowany został z dużym naciskiem na stronę wizualną programu (duże znaczenie ma doświadczenie użytkownika). 

Projekt jest implementacją gry planszowej SCRABBLE. Gracz rywalizuje z Botem. Zgodnie z zasadami gry, gracz może ułożyć słowa na następujące sposoby:
<br>
1. Dołożenie jednej lub kilku płytek na początku lub na końcu słowa już znajdującego się na planszy, albo też zarówno na początku, jak i na końcu takiego słowa.
2. Ułożenie słowa pod kątem prostym do słowa znajdującego się na planszy. Nowe słowo musi wykorzystywać jedną z liter słowa leżącego na planszy.
3. Ułożenie całego słowa równolegle do słowa już istniejącego w taki sposób, by stykające się płytki także tworzyły całe słowa.
4. Nowe słowo może także dodać literę do istniejącego słowa.
5. Ostatnia możliwość to „mostek” między dwiema lub więcej literami.

Bot ma za zadanie symulować drugiego gracza. Może on ułożyć słowo na 1, 2 i 4 sposób. W przypadku nie znalezienia odpowiedniego słowa, wymienia on stojak. Założenie jest następujące: bot nie może być idealny! Nie jest to więc mile widziane, aby za każdym razem ułożył on prawidłowe słowo.

## Co to SCRABBLE?
SCRABBLE to gra słowna. Polega na układaniu na planszy powiązanych ze sobą słów przy użyciu płytek z literami o różnej wartości - przypomina to budowanie krzyżówki. Celem gry jest uzyskanie jak najwyższego wyniku. Każdy gracz stara się uzyskać jak najwięcej punktów układając słowa w taki sposób, by wykorzystać wartość liter i premiowane pola na planszy. Zależnie od umiejętności graczy, suma uzyskanych w grze punktów może osiągnąć od 400 do 800, albo nawet więcej.

## Instrukcja rozgrywki
### Rozpoczęcie gry
Z woreczka z literami losuje się 7 z nich, które następnie pojawiają się na stojaku gracza. Pierwszy ruch w grze należy do gracza. Po wyłożeniu przez niego płytek i zatwierdzeniu ruchu, sprawdzana jest poprawność słowa. Jeśli zostało ono niepoprawnie ułożone (nie w poziomie lub pionie), nie znajduje się w słowniku, lub jeśli ilość liter nie mieści się w zakresie od 2 do 5, to płytki wracają na stojak. Następuje kolejka bota.

### Wymiana płytek
Gracz może wymienić wszystkie płytki, jeśli nie wyłożył jeszcze żadnej płytki lub w przypadku, gdy w woreczku znajduje się odpowiednia liczba liter, po tym jego ruch się kończy.

### Opuszczanie kolejki
Gracz może opuścić kolejkę maksymalnie dwukrotnie, inaczej gra się kończy.

### Tworzenie nowych słów
Gracz ma możliwość stworzenia słów, tak jak zostało to wspomniane w opisie projektu.

### Zakończenie gry
Gra kończy się, gdy jeden z graczy nie ma już żadnych płytek na stojaku. Opuszczenie przez wszystkich graczy dwu kolejek z rzędu kończy grę niezależnie od tego jak wiele płytek pozostało jeszcze w woreczku i na stojakach.


### Dokładne zasady
[Polska Federacja SCRABBLE](http://www.pfs.org.pl/reguly.php)


## Mapowanie klawiszy


|   Klawisz  |       Akcja           |
| ---------- | ---------------------- |
| SPACE | Rozpoczęcie gry |
|    ENTER   |    Zatwierdzenie słowa; przejście do kolejki bota  /   Zatwierdzenie imienia  |
|      R     |    Wymiana płytek    |
|      S     |    Opuszczenie kolejki |
| E | Zakończenie rozgrywki |

## Klasy
 - Game <br>
 Klasa mająca za zadanie zarządzanie aktualną instancją gry.

 - Board <br>
 Zarządza planszą, w tym rysowaniem jej elementów, jak i wizualnej strony stojaka z literami. 

 - LettersBag <br>
 Klasa zarządza woreczkiem z literami. Umożliwia wyjmowanie i wkładanie liter do niego, jak również losowy wybór płytki (symulujący rzeczywistość)

 - Tile<br>
 Klasa dziedziczy po wbudowanej klasie z modułu pygame (pygame.sprite.Sprite), która zarządza widocznymi obiektami gry. Posiada atrybuty: letter i position.

 - Move <br>
 Zarządza ruchem graczy, w tym: kliknięciami myszki, ułożeniem słów na planszy i ich poprawnością. 

 - Player<br>
 Zarządza graczem. Odpowiedzialna za przechowywanie informacji o liście słów, stojaka na płytki oraz imienia konkretnego gracza. Co więcej właśnie w niej obecna jest funkcja zwracająca ostateczny wynik danego gracza.

 - Bot <br>
 Jest klasą, która dziedziczy po Player. Oprócz funkcjonalności powyższej klasy, posiada ona też takie, które pozwalają na to, że bot jest pełnoprawnym graczem z własnymi decyzjami. Bot, tak jak gracz, może ułożyć nowe słowo, dodać do już istniejącego lub wymienić swój stojak z literami. 

## Rozgrywka i przedstawienie aspektu wizualnego
Po uruchomieniu programu gracz witany jest ekranem starowym, gdzie znajduje się informacja o twórcy. Następnie klikając przycisk SPACE przeniesiony zostaje do ekranu z polem na wpisanie imienia. W przypadku nie podania informacji, na ekranie końcowym wyświetli się imię 'Player'.
<br><br>
Następnie rozpoczyna się rozgrywka. Pierwsze słowo musi znaleźć się na polu o indeksach (7,7), co zostało oznaczone wyróżniającym się kolorem. Jeśli gracz nie wykona ruchu, spróbuje go zrobić bot.
<br><br>
Poniżej stojaka z literami gracza wyświetla się aktualna runda.
<br><br>
Podczas rozgrywki gracz ma trzy możliwości wykorzystania swojej kolejki: opuszczenie jej, wymiana stojaka z literami lub wyłożenie liter na plansze. 
<br><br>
Gra kończy się w momencie, gdy gracz opuści swoją kolejkę dwa razy, stojak jednego z graczy będzie pusty lub po naciśnięciu przycisku E. 
<br><br>
Po zakończeniu rozgrywki wyświetli się ekran końcowy. Przedstawiony na nim jest wynik punktowy zarówno gracza, jak i bota. Na dole ekrany zostaje wyświetlony zwycięzca.

## Bot
Bot jest swoistym programem, który symuluje gracza. Jego ruch jest losowy. Najpierw losuje on to, czy położy nowe słowo, lub czy doda litery do już istniejącego. Następnie w przypadku tworzenia nowego słowa losuje on jego kierunek. Następuje losowanie rzędu i kolumny, po których rozpoczynamy iteracje, szukając odpowiedniej i zgodnej z warunkami pozycji słowa.
<br>
W przypadku już istniejącego słowa, bot szuka możliwości dodania liter do jednego ze słów na planszy. Następnie w kolejnej funkcji sprawdza możliwość dodania liter do danego słowa. 
<br><br>
W przypadku dodania nowego słowa bot bierze pod uwagę puste literki.
<br><br>
Bot próbuje ułożyć akceptowalne słowo maksymalnie 4 razy, po czym wymienia stojak z literami.

## Użyte moduły i czcionki
### Moduły
- [RE](https://docs.python.org/3/library/re.html?highlight=re#module-re) <br>
Użyty w konstrukcji bota do znajdowania nowych słów.
- [Random](https://docs.python.org/3/library/random.html?highlight=random#module-random) <br>
Moduł wykorzystany do stworzenia bota z daną losowością.
- [PyGame](https://www.pygame.org/docs/ref/pygame.html) <br>
Użyty do wykonania apektu wizualnego gry.  

### Czcionki 
W grze zostały użyte dwie czcionki GoogleFonts:
- [Rubik Doodle Shadow](https://fonts.google.com/specimen/Rubik+Doodle+Shadow?query=rubik)
- [Rubik](https://fonts.google.com/specimen/Rubik?query=rubik)

## Refleksja
To be done...
