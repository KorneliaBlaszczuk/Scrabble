# Projekt PIPR - Gra SCRABBLE

### Autor

<strong>Kornelia Błaszczuk</strong> <br>
Studentka 1 Semestru Informatyki I stopnia na Politechnice Warszawskiej <br>
<strong>Numer Indeksu:</strong> 331361 <br>
<strong>Mail:</strong> 01187210@pw.edu.pl <br>

## Temat projektu

Przygotuj program który pozwoli grać w grę scrabble.
<br><br>
Gra polega na układaniu słów z wylosowanych klocków z literkami i dokładaniu ich do planszy tak żeby zdobyć jak najwięcej punktów. Słowa dokładać można tylko w jednym kierunku (pion lub poziom), a po dołożeniu nowego słowa wszystkie zbitki liter na planszy musza mieć sens (Zarówno w pionie jak i w poziomie).
<br><br>
W wersji piprowej proponuję uproszczenie gry do maksymalnie 5-literowych słów (w wersji z botem, żeby ułatwić przeszukiwanie słownika) i zrezygnowanie z pól z dodatkowymi premiami. Do rozwiązania zadania (stworzenia bota) należy wykorzystać słownik np: https://sjp.pl/slownik/growy/
<br><br>
Dokładne reguły, punktacja i liczba płytek z daną literą są dostępne na stronie: http://www.pfs.org.pl/reguly.php

## Cel i opis projektu

Celem projektu jest wykonanie gry SCRABBLE, implementując ją z wykorzystaniem języka Python. Zrealizowany został z dużym naciskiem na stronę wizualną programu (duże znaczenie ma doświadczenie użytkownika).

Projekt jest implementacją gry planszowej SCRABBLE. Gracz rywalizuje z Botem. Zgodnie z zasadami gry, gracz może ułożyć słowa na następujące sposoby:
<br>

1. Dołożenie jednej lub kilku płytek na początku, lub na końcu słowa już znajdującego się na planszy, albo też zarówno na początku, jak i na końcu takiego słowa.
2. Ułożenie słowa pod kątem prostym do słowa znajdującego się na planszy. Nowe słowo musi wykorzystywać jedną z liter słowa leżącego na planszy.
3. Ułożenie całego słowa równolegle do słowa już istniejącego w taki sposób, by stykające się płytki także tworzyły całe słowa.
4. Nowe słowo może także dodać literę do istniejącego słowa.
5. Ostatnia możliwość to „mostek” między dwiema lub więcej literami.

Bot ma za zadanie symulować drugiego gracza. Może on ułożyć słowo na 1, 2 i 4 sposób. W przypadku nie znalezienia odpowiedniego słowa wymienia on stojak. Założenie jest następujące: bot nie może być idealny! Nie jest to więc mile widziane, aby za każdym razem ułożył on prawidłowe słowo.

## Co to SCRABBLE?

SCRABBLE to gra słowna. Polega na układaniu na planszy powiązanych ze sobą słów przy użyciu płytek z literami o różnej wartości - przypomina to budowanie krzyżówki. Celem gry jest uzyskanie jak najwyższego wyniku. Każdy gracz stara się uzyskać jak najwięcej punktów układając słowa w taki sposób, by wykorzystać wartość liter i premiowane pola na planszy. Zależnie od umiejętności graczy, suma uzyskanych w grze punktów może osiągnąć od 400 do 800, albo nawet więcej.

## Instrukcja użytkownika

1. Będąc na ekranie tytułowym, kliknij spację, aby przejść dalej.
2. Jeśli chcesz, wpisz swoje imię (maksymalnie 10 znaków). W innym przypadku nadanie zostanie ci automatycznie imię 'Player'.
3. Czas na rozpoczęcie rozgrywki. Zaczynasz ty! Pierwsze słowo musi się znajdować na środkowym polu o charakterystycznym kolorze.
4. Aby zatwierdzić słowo, kliknij ENTER. Następuje kolej Bota
5. Jeśli nie jesteś w stanie ułożyć żadnego słowa w momencie gry, możesz albo wymienić stojak, albo opuścić kolejkę (maksymalnie dwie pod rząd).
6. Możesz ułożyć słowa zgodnie z zasadami wymienionymi wyżej (patrz: cel i opis projektu)
7. W każdej chwili możesz zakończyć rozgrywkę, klikając przycisk E. Wyświetli się wtedy punktacja oraz wygrany.
   Powodzenia!

## Instrukcja rozgrywki

### Rozpoczęcie gry

Z woreczka z literami losuje się 7 z nich, które następnie pojawiają się na stojaku gracza. Pierwszy ruch w grze należy do gracza. Po wyłożeniu przez niego płytek i zatwierdzeniu ruchu, sprawdzana jest poprawność słowa. Jeśli zostało ono niepoprawnie ułożone (nie w poziomie lub pionie), nie znajduje się w słowniku, lub jeśli ilość liter w słowie nie mieści się w zakresie od 2 do 5, to płytki wracają na stojak. Następuje kolejka bota.

### Wymiana płytek

Gracz może wymienić wszystkie płytki, jeśli nie wyłożył jeszcze żadnej płytki lub w przypadku, gdy w woreczku znajduje się odpowiednia liczba liter, po tym jego ruch się kończy.

### Opuszczanie kolejki

Gracz może opuścić kolejkę maksymalnie dwukrotnie, potem gra się kończy.

### Tworzenie nowych słów

Gracz ma możliwość stworzenia słów, tak jak zostało to wspomniane w opisie projektu.

### Zakończenie gry

Gra kończy się, gdy jeden z graczy nie ma już żadnych płytek na stojaku. Opuszczenie gracza dwóch kolejek z rzędu kończy grę niezależnie od tego jak wiele płytek pozostało jeszcze w woreczku i na stojakach.

### Dokładne zasady

[Polska Federacja SCRABBLE](http://www.pfs.org.pl/reguly.php)

## Mapowanie klawiszy

| Klawisz                | Akcja                                                                  |
| ---------------------- | ---------------------------------------------------------------------- |
| <strong>SPACE</strong> | Rozpoczęcie gry                                                        |
| <strong>ENTER</strong> | Zatwierdzenie słowa; przejście do kolejki bota / Zatwierdzenie imienia |
| <strong>R</strong>     | Wymiana płytek                                                         |
| <strong>S</strong>     | Opuszczenie kolejki                                                    |
| <strong>E</strong>     | Zakończenie rozgrywki</strong>                                         |

## Klasy

- <strong>Game</strong> <br>
  Klasa mająca za zadanie zarządzanie aktualną instancją gry.

- <strong>Board</strong> <br>
  Zarządza planszą, np.: w tym rysowaniem jej elementów, jak i wizualnej strony stojaka z literami. Zarządza również listą słów znajdujących się na planszy.

- <strong>LettersBag</strong> <br>
  Klasa zarządza woreczkiem z literami. Umożliwia wyjmowanie i wkładanie liter do niego, jak również losowy wybór płytki (symulujący rzeczywistość)

- <strong>Tile</strong><br>
  Klasa dziedziczy po wbudowanej klasie z modułu pygame (pygame.sprite.Sprite), która zarządza widocznymi obiektami gry. Posiada atrybuty: letter i position. Obsługuje płytki z literami.

- <strong>Move</strong> <br>
  Zarządza ruchem graczy, w tym: kliknięciami myszki, ułożeniem słów na planszy i ich poprawnością.

- <strong>Player</strong><br>
  Zarządza graczem. Odpowiedzialna za przechowywanie informacji o liście słów, stojaka na płytki oraz imienia konkretnego gracza. Co więcej, właśnie w niej obecna jest funkcja zwracająca ostateczny wynik danego gracza.

- <strong>Bot</strong> <br>
  Jest klasą, która dziedziczy po Player. Oprócz funkcjonalności powyższej klasy posiada ona też takie, które pozwalają na to, że bot jest pełnoprawnym graczem z własnymi decyzjami. Bot, tak jak gracz, może ułożyć nowe słowo, dodać do już istniejącego lub wymienić swój stojak z literami.

## Bot

Bot jest swoistym programem, który symuluje gracza. Jego ruch jest losowy (chyba że na planszy nie ma jeszcze płytek). Najpierw losuje on to, czy położy nowe słowo (doda do jednej literki), lub czy doda litery do już istniejącego na planszy. W przypadku nowego słowa położenie słowa bota jest prostopadłe. Bot szuka możliwości dodania liter do wylosowanego słowa czy litery na planszy. Następnie w kolejnej funkcji sprawdza możliwość dodania liter do niego.
<br><br>
Bot obsługuje puste płytki.
<br><br>
Bot próbuje ułożyć akceptowalne słowo maksymalnie 5 razy, po czym wymienia stojak z literami. Jest to rozwiązanie zaimplementowane, między innymi ze względów optymalizacyjnych.
<br><br>
Przez pierwszą sekundę swojego ruchu nie dzieje się nic (w celu rzeczywistej symulacji ruchu).

## Testy

Testy zostały dobrane tak, aby sprawdzić powstawanie instancji funkcji oraz realizację ich funkcji. W ramach nich przetestowane zostało również wyświetlanie okna z programem oraz kolory na nim obecne.
Przewagą rozwiązania gry w pygame jest to, że gracz ma ograniczone możliwości ingerencji. Nie jest on w stanie wykonać ruchu zabronionego, a więc nie spotka się on z błędami, takimi jak, np. ValueError itd.

## Użyte moduły i czcionki

### Moduły

- <strong>[re](https://docs.python.org/3/library/re.html?highlight=re#module-re)</strong> <br>
  Użyty w konstrukcji bota do znajdowania nowych słów.
- <strong>[random](https://docs.python.org/3/library/random.html?highlight=random#module-random)</strong> <br>
  Moduł wykorzystany do stworzenia bota z daną losowością.
- <strong>[PyGame](https://www.pygame.org/docs/ref/pygame.html)</strong> <br>
  Użyty do wykonania apektu wizualnego gry.
- <strong>[time](https://docs.python.org/3/library/time.html?highlight=time#module-time)</strong>
  Moduł został użyty celu lepszej symulacji ruchu bota. Jego runda jest widoczna dla gracza, dzięki użyciu funkcji sleep() z tego modułu.
- <strong>[sys](https://docs.python.org/3/library/sys.html?highlight=sys#module-sys)</strong> <br>
  Wykorzystywane podczas zamykania ekranu gry.
- <strong>[pytest](https://docs.pytest.org/en/7.1.x/contents.html)</strong> <br>
  Użyty podczas testów.

### Czcionki

W grze zostały użyte dwie czcionki GoogleFonts:

- <strong>[Rubik Doodle Shadow](https://fonts.google.com/specimen/Rubik+Doodle+Shadow?query=rubik)</strong>
- <strong>[Rubik](https://fonts.google.com/specimen/Rubik?query=rubik)</strong>

## Refleksja

Do projektu od początku podeszłam z wielkim zapałem i zaangażowaniem. Był on zdecydowanie dla mnie wyzwaniem, ale również dobrą zabawą. W mojej opinii zrealizował zadanie z czułością o detale. Starałam się uzyskać interfejs przyjazny użytkownikowi, co uważam, że się udało. Jestem niezmiernie szczęśliwa ze zrealizowania bota, który jest jak prawdziwy gracz. Uważam, że to, co tworzymy, pisząc kod, musi powodować dobre emocje u użytkowników. Do zrealizowania mojego celu wykorzystałam moduł pygame, który pozwolił mi, między innymi, na spersonalizowanie rozgrywki dla każdego gracza (wprowadzenie imienia).
<br><br>
W fazie wstępnego szkicu nie przywiązywał takiej uwagi do dozwolonych ruchów, co później okazało się głównym ciałem mojego projektu. Osobiście uważam, że moja wizja pierwotna nie odbiegała od wersji ostatecznej, a może jest nawet szersza. Nie uwzględniałam w szkicu dodatkowych efektów wizualnych, co myślę, że aktualnie uatrakcyjnia mój projekt. Również, nie zdawałam sobie sprawy z całej złożoności projektu.
<br><br>
Choć nie udało mi się zaimplementować dla bota każdego możliwego ruchu, jakie ma gracz, to i tak uważam, że jest on dosyć rozbudowany. Nie mam wątpliwości, że powodem, dla którego bot nie może wykonać każdego ruchu dozwolonego w zasadach, jest najzwyczajniej ograniczony czas projektu. Myślę, że w wolnym czasie zdecydowanie spróbuje jeszcze zaimplementować kolejne funkcjonalności.
<br><br>
Wyzwaniem w trakcie projektu było oswojenie się z zasadami gry w SCRABBLE. Był to może i najtrudniejszy etap, tym bardziej że z tą grą nigdy nie miałam styczności.
<br><br>
Największym wyzwaniem dla mnie była implementacja w ruchach bota pustych płytek. Wymagało to ode mnie dużo planowania oraz cierpliwości.
<br><br>
Innym wyzwaniem było samo stworzenie bota, który symulowałby realnego gracza. Choć nie ukrywam, że jego tworzenie sprawiło mi mnóstwo zabawy!
<br><br>
Podsumowując rzeczy, których nie udało mi się osiągnąć (są one tak naprawdę rzeczami dodatkowymi, jeszcze bardziej rozszerzającymi grę):

- Wymiana <strong>konkretnej</strong> litery ze stojaka (powód: brak wystarczającej ilości czasu; skupienie się na bocie)
- Wykonywanie przez bota wszystkich możliwych ruchów jak w zasadach (powód: brak wystarczającej ilości czasu)
- Zakończenie gry, gdy nie ma już możliwości wykonania innych ruchów (powód: brak wystarczającej ilości czasu)
  Podsumowując, powodem niezrealizowanych funkcjonalności jest ograniczony zakres czasowy projektu.
