# Projekt PIPR - Gra SCRABBLE
## ENG
# PIPR Project - SCRABBLE Game

### Author

<strong>Kornelia Błaszczuk</strong> <br>
Computer Science Student at Warsaw University of Technology <br>

## Project Topic

Create a program that allows playing the game of Scrabble.
<br><br>
The game involves creating words from randomly drawn tiles with letters and placing them on the board to score the most points. Words can only be placed in one direction (horizontal or vertical), and after placing a new word, all letter combinations on the board must make sense (both vertically and horizontally).
<br><br>
In the pip version, I suggest simplifying the game to a maximum of 5-letter words (for the bot version, to ease dictionary search) and removing the premium tiles. To implement the bot, use a dictionary, e.g., https://sjp.pl/slownik/growy/.
<br><br>
Exact rules, point scoring, and the number of tiles for each letter are available at: http://www.pfs.org.pl/reguly.php

## Project Goal and Description

The goal of the project is to create a SCRABBLE game using the Python language. The project focuses on the visual aspect of the program (user experience is important).

This project is an implementation of the SCRABBLE board game. The player competes against a bot. According to the rules of the game, the player can form words in the following ways:
<br>

1. Add one or several tiles to the beginning or end of an already existing word on the board, or to both ends of that word.
2. Place a word perpendicular to an existing word on the board. The new word must use one letter from the existing word on the board.
3. Place a word parallel to an existing word in such a way that the tiles touching each other also form valid words.
4. A new word can also add a letter to an existing word.
5. The last option is a "bridge" between two or more letters.

The bot’s task is to simulate the second player. It can place a word in options 1, 2, and 4. If it cannot find a valid word, it swaps tiles. The assumption is that the bot will not always play perfectly. It should not always find a valid word.

## What is SCRABBLE?

SCRABBLE is a word game. It involves arranging words on the board by using letter tiles with varying values, resembling the construction of a crossword puzzle. The goal is to score as many points as possible. Each player tries to get the highest possible score by placing words in such a way that the letter values and premium squares on the board are used. Depending on the skill of the players, the total points in a game can range from 400 to 800 or more.

## User Instructions

1. On the title screen, press the spacebar to proceed.
2. If you wish, enter your name (up to 10 characters). Otherwise, the name 'Player' will be assigned automatically.
3. The game begins. You start first! The first word must be placed in the center square, which has a special color.
4. To confirm a word, press ENTER. The bot’s turn follows.
5. If you cannot form any word during your turn, you can either swap your tiles or skip your turn (up to two times).
6. You can form words according to the rules mentioned earlier (see: project goal and description).
7. At any time, you can end the game by pressing the E key. The score and the winner will then be displayed.
   Good luck!

## Game Instructions

### Starting the Game

Seven letter tiles are randomly drawn from the letter bag and appear on the player's rack. The first turn belongs to the player. After placing their tiles and confirming their move, the validity of the word is checked. If the word is invalid (it’s not placed horizontally or vertically, not in the dictionary, or not within 2 to 5 letters), the tiles return to the rack. The bot’s turn follows.

### Swapping Tiles

The player can swap all tiles if they haven’t placed any tiles yet or if there are enough tiles remaining in the bag, after which their turn ends.

### Skipping Turns

The player can skip their turn up to two times, after which the game ends.

### Forming New Words

The player can form words in accordance with the rules listed in the project goal and description.

### Ending the Game

The game ends when one of the players has no tiles left on their rack. Skipping two turns in a row also ends the game, regardless of how many tiles are left in the bag and on the racks.

### Detailed Rules

[Polska Federacja SCRABBLE](http://www.pfs.org.pl/reguly.php)

## Key Mappings

| Key                     | Action                                                                 |
| ------------------------ | ---------------------------------------------------------------------- |
| <strong>SPACE</strong>   | Start the game                                                          |
| <strong>ENTER</strong>   | Confirm the word; move to bot's turn / Confirm name                     |
| <strong>R</strong>       | Swap tiles                                                              |
| <strong>S</strong>       | Skip turn                                                               |
| <strong>E</strong>       | End the game                                                            |

## Classes

- <strong>Game</strong> <br>
  The class responsible for managing the current game instance, including the graphical interface.

- <strong>Board</strong> <br>
  Manages the board, including the list of words and the tiles placed on the board.

- <strong>LettersBag</strong> <br>
  The class that manages the letter bag, allowing tiles to be drawn and returned to the bag, as well as randomly selecting tiles (simulating real-life gameplay).

- <strong>Tile</strong><br>
  A class inheriting from the built-in class from the pygame module (pygame.sprite.Sprite) that handles visible game objects. It has the attributes: letter and position. It handles tiles with letters.

- <strong>Move</strong> <br>
  Manages mouse clicks.

- <strong>Player</strong><br>
  Manages the player, storing information about the word list, tile rack, and the player's name. This class also has a function that returns the final score of the player.

- <strong>Bot</strong> <br>
  A class that inherits from Player. In addition to the functionalities of the Player class, it has methods that allow it to simulate a full-fledged player with its own decisions. Like a player, the bot can form new words, add to existing words, or swap its letter rack.

## Bot

The bot is a program that simulates a player. Its moves are random (unless the board has no tiles yet). First, it randomly decides whether to form a new word (by adding to an existing one) or to add letters to an existing word on the board. When creating a new word, the bot places the word perpendicular to the existing word. It looks for possible positions where it can add letters to the word or letter on the board. In the next function, it checks the possibility of adding letters to the word.

The bot handles blank tiles.

The bot attempts to form a valid word up to 5 times. If it cannot find a valid word, it swaps the tiles. This approach is implemented, partly for optimization reasons.

For the first second of its turn, the bot does nothing (for realistic turn simulation).

## Testing

The tests were chosen to verify the creation of function instances and their execution. They also tested the display of the program's window and the colors present in it.
A significant advantage of implementing the game in pygame is that the player has limited options for interference. Therefore, they will not encounter errors such as ValueError, etc.

## Used Modules and Fonts

### Modules

- <strong>[re](https://docs.python.org/3/library/re.html?highlight=re#module-re)</strong> <br>
  Used in the bot's construction to find new words.
- <strong>[random](https://docs.python.org/3/library/random.html?highlight=random#module-random)</strong> <br>
  Used to create randomness for the bot.
- <strong>[PyGame](https://www.pygame.org/docs/ref/pygame.html)</strong> <br>
  Used for the visual aspects of the game.
- <strong>[time](https://docs.python.org/3/library/time.html?highlight=time#module-time)</strong>
  Used to simulate the bot's turn. The sleep() function from this module allows the turn to be visible to the player.
- <strong>[sys](https://docs.python.org/3/library/sys.html?highlight=sys#module-sys)</strong> <br>
  Used for closing the game window.
- <strong>[pytest](https://docs.pytest.org/en/7.1.x/contents.html)</strong> <br>
  Used for testing.

### Fonts

Two Google Fonts were used in the game:

- <strong>[Rubik Doodle Shadow](https://fonts.google.com/specimen/Rubik+Doodle+Shadow?query=rubik)</strong>
- <strong>[Rubik](https://fonts.google.com/specimen/Rubik?query=rubik)</strong>

## Reflection

I approached the project with great enthusiasm and commitment. It was definitely a challenge for me, but also a fun experience. I believe I successfully completed the task with attention to detail. I focused on creating a user-friendly interface, which I think I achieved. I’m particularly happy with the bot’s implementation, which behaves like a real player. I believe that the code we write should evoke good emotions in users. I used the pygame module to personalize the gameplay for each player (e.g., entering a name).
<br><br>
In the initial draft phase, I didn’t pay as much attention to the allowed moves, which turned out to be the core of my project. Personally, I think the initial vision didn’t stray much from the final version, and it may even be broader. I didn’t account for additional visual effects in the draft, but I think they currently make my project more engaging. Also, I didn't realize the full complexity of the project.
<br><br>
Although I didn’t manage to implement every possible move for the bot as the player has, I still think it is quite a robust bot. There is no doubt that the reason the bot cannot perform every allowed move is due to the limited time available for the project. I plan to implement more functionalities in my free time.
<br><br>
One of the most challenging aspects during the project was understanding the rules of SCRABBLE. This was probably the hardest stage, especially since I had never played the game before.
<br><br>
The biggest challenge for me was implementing blank tiles in the bot’s moves. This required a lot of planning and patience.
<br><br>
Another challenge was creating the bot that simulated a real player. Although I won’t deny that building it was a lot of fun!
<br><br>
In conclusion, there were some things I didn’t manage to achieve (these are additional features that would further expand the game):

- Swapping <strong>specific</strong> tiles from the rack (reason: lack of time; focus on the bot)
- Making the bot perform all possible moves as allowed by the rules (reason: lack of time)
- Ending the game when no more moves can be made (reason: lack of time)

In summary, the reason for not achieving all functionalities was the limited scope of the project.


## PL
### Autor

<strong>Kornelia Błaszczuk</strong> <br>
Studentka Informatyki I stopnia na Politechnice Warszawskiej <br>

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
  Klasa mająca za zadanie zarządzanie aktualną instancją gry. W tym stroną graficzną.

- <strong>Board</strong> <br>
  Zarządza planszą, również listą słów oraz aktualnie wyłożonych znajdujących się na planszy.

- <strong>LettersBag</strong> <br>
  Klasa zarządza woreczkiem z literami. Umożliwia wyjmowanie i wkładanie liter do niego, jak również losowy wybór płytki (symulujący rzeczywistość)

- <strong>Tile</strong><br>
  Klasa dziedziczy po wbudowanej klasie z modułu pygame (pygame.sprite.Sprite), która zarządza widocznymi obiektami gry. Posiada atrybuty: letter i position. Obsługuje płytki z literami.

- <strong>Move</strong> <br>
  Zarządza klinięciami myszki.

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
