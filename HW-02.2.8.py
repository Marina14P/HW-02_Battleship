import random

# Класс для координат точки на поле
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Класс для корабля
class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates

# Класс для игровой доски
class Board:
    def __init__(self, size, name):
        self.size = size
        self.board = [['О' for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.name = name

    def place_ship(self, ship):
        for point in ship.coordinates:
            x, y = point.x, point.y
            self.board[y][x] = '■'
        self.ships.append(ship)

    def display(self):
        print(f"   игровая доска {self.name}")
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i in range(self.size):
            row = [str(i + 1)]
            row.extend(self.board[i])
            print(" | ".join(row))

    def shoot(self, x, y):
        if self.board[y][x] == '■':
            self.board[y][x] = 'X'  # Подбит корабль
            for ship in self.ships:
                if Point(x, y) in ship.coordinates:
                    ship.coordinates.remove(Point(x, y))
                    if not ship.coordinates:
                        self.ships.remove(ship)
            return True
        elif self.board[y][x] == 'О':
            self.board[y][x] = 'T'  # Промах
            return False
        else:
            raise ValueError("Вы уже стреляли в эту клетку")

# Функция для создания случайного корабля
def create_random_ship(size, board):
    while True:
        x = random.randint(0, board.size - 1)
        y = random.randint(0, board.size - 1)
        direction = random.choice(['horizontal', 'vertical'])
        coordinates = []
        for _ in range(size):
            if direction == 'horizontal':
                if x + size > board.size:
                    continue
                if any(Point(x + i, y) in board.ships for i in range(size)):
                    continue
                coordinates.append(Point(x + _, y))
            elif direction == 'vertical':
                if y + size > board.size:
                    continue
                if any(Point(x, y + i) in board.ships for i in range(size)):
                    continue
                coordinates.append(Point(x, y + _))
        if len(coordinates) == size:
            return Ship(coordinates)

# Функция для отображения доски компьютера
def display_computer_board(board):
    print(f"  игровая доска {board.name}")
    print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
    for i in range(board.size):
        row = [str(i + 1)]
        row.extend(board.board[i])
        print(" | ".join(row))

# Функция для игры
def play_game():
    size = 6
    player_board = Board(size, "'Игрока'")
    computer_board = Board(size, "'Компьютера'")

    # Расставляем корабли
    for _ in range(4):
        player_ship = create_random_ship(1, player_board)
        computer_ship = create_random_ship(1, computer_board)
        player_board.place_ship(player_ship)
        computer_board.place_ship(computer_ship)
    for _ in range(2):
        player_ship = create_random_ship(2, player_board)
        computer_ship = create_random_ship(2, computer_board)
        player_board.place_ship(player_ship)
        computer_board.place_ship(computer_ship)
    player_ship = create_random_ship(3, player_board)
    computer_ship = create_random_ship(3, computer_board)
    player_board.place_ship(player_ship)
    computer_board.place_ship(computer_ship)

    player_won = False
    computer_won = False
    player_shots = set()
    computer_shots = set()

    while not player_won and not computer_won:
        # Ход игрока
        player_board.display()
        display_computer_board(computer_board)
        try:
            x, y = map(int, input("Ваш ход (x y): ").split())
            x -= 1
            y -= 1
            if (x, y) in player_shots:
                raise ValueError("Вы уже стреляли в эту клетку")
            player_shots.add((x, y))
            if computer_board.shoot(x, y):
                print("Вы попали!")
            else:
                print("Промах!")
        except (ValueError, IndexError):
            print("Неправильный ввод. Попробуйте еще раз.")
            continue

        if not computer_board.ships:
            player_won = True
            break

        # Ход компьютера
        while True:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            if (x, y) not in computer_shots:
                computer_shots.add((x, y))
                if player_board.shoot(x, y):
                    print(f"Компьютер попал в клетку {x + 1} {y + 1}!")
                    break

        if not player_board.ships:
            computer_won = True
            break

    player_board.display()
    display_computer_board(computer_board)
    if player_won:
        print("Вы победили!")
    else:
        print("Компьютер победил!")

if __name__ == "__main__":
    play_game()

