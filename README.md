# Projekt PIPR - Gra SCRABBLE


## Wprowadzenie
SCRABBLE to gra słowna. Polega na układaniu na planszy powiązanych ze sobą słów przy użyciu płytek z literami o różnej wartości - przypomina to budowanie krzyżówki. Celem gry jest uzyskanie jak najwyższego wyniku. Każdy gracz stara się uzyskać jak najwięcej punktów układając słowa w taki sposób, by wykorzystać wartość liter i premiowane pola na planszy. Zależnie od umiejętności graczy, suma uzyskanych w grze punktów może osiągnąć od 400 do 800, albo nawet więcej.

## Instrukcja rozgrywki
### Rozpoczęcie gry
Z woreczka z literami losuje się 7 z nich, które następnie pojawiają się na stojaku gracza. Pierwszy ruch w grze należy do gracza. Po wyłożeniu przez niego płytek i zatwierdzeniu ruchu, sprawdzana jest poprawność słowa. Jeśli zostało ono niepoprawnie ułożone (nie w poziomie lub pionie), nie znajduje się w słowniku, lub jeśli ilość liter nie mieści się w zakresie od 2 do 5, to płytki wracają na stojak. Następuje kolejka bota.

### Wymiana płytek
Gracz może wymienić wszystkie płytki, jeśli nie wyłożył jeszcze żadnej płytki lub w przypadku, gdy w woreczku znajduje się odpowiednia liczba liter, po tym jego ruch się kończy.

### Opuszczanie kolejki
Gracz może opuścić kolejkę maksymalnie dwukrotnie, inaczej gra się kończy.

### Tworzenie nowych słów
Nowe słowa można tworzyć na pięć sposobów:
1. Dołożenie jednej lub kilku płytek na początku lub na końcu słowa już znajdującego się na planszy, albo też zarówno na początku, jak i na końcu takiego słowa.
2. Ułożenie słowa pod kątem prostym do słowa znajdującego się na planszy. Nowe słowo musi wykorzystywać jedną z liter słowa leżącego na planszy.
3. Ułożenie całego słowa równolegle do słowa już istniejącego w taki sposób, by stykające się płytki także tworzyły całe słowa.
4. Nowe słowo może także dodać literę do istniejącego słowa.
5. Ostatnia możliwość to „mostek” między dwiema lub więcej literami.

### Zakończenie gry
Gra kończy się, gdy jeden z graczy nie ma już żadnych płytek na stojaku. Gra kończy się także wtedy, gdy bot nie znajdzie żadnego możliwego ruchu i wszyscy gracze opuszczą dwie kolejki z rzędu.
Uwaga: Opuszczenie przez wszystkich graczy dwu kolejek z rzędu kończy grę niezależnie od tego jak wiele płytek pozostało jeszcze w woreczku i na stojakach.


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

### Klasy
 - Board <br>
Zarządza planszą. Jest odpowiedzialna za sprawdzanie poprawności ruchów graczy, określaniu koordynatów danego słowa, za przechowywanie wszystkich słów znajdujących się na planszy. Zarządza również woreczkiem z literami możliwymi do użycia przez graczy.

 - Tile<br>
 Klasa dziedziczy po wbudowanej klasie z modułu pygame (pygame.sprite.Sprite), która zarządza widocznymi obiektami gry. Posiada atrybuty: letter i position.

 - Player<br>
 Zarządza graczem. Odpowiedzialna za przechowywanie informacji o liście słów, stojaka na płytki oraz imienia konkretnego gracza. Co więcej właśnie w niej obecna jest funkcja zwracająca ostateczny wynik danego gracza.

 - Bot <br>
 Jest klasą, która dziedziczy po Player. Oprócz funkcjonalności powyższej klasy, posiada ona też takie, które pozwalają na to, że bot jest pełnoprawnym graczem z własnymi decyzjami. Bot, tak jak gracz, może ułożyć nowe słowo, dodać do już istniejącego lub wymienić swój stojak z literami. 

### Rozgrywka i przedstawienie aspektu wizualnego
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
Po zakończeniu rozgrywki wyświetli się ekran końcowy. Przedstawiony na nim jest wynik punktowy zarówno gracza, jak i bota. 

