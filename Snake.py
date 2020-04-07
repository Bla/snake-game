from ipy_lib import SnakeUserInterface  #import interface
from Coordinate import Coordinate
from CoordinateRow import CoordinateRow

FIELD_WIDTH = 32
FIELD_HEIGHT = 24
FPS = 10
RIGHT = 'r'
LEFT = 'l'
UP = 'u'
DOWN = 'd'
apple_stock = CoordinateRow()

'''
Functions
'''
def create_field(width=FIELD_WIDTH, height=FIELD_HEIGHT, speed=FPS):
    ui = SnakeUserInterface(width, height)   #create GUI object
    ui.set_animation_speed(speed)
    return ui

def initialize_snake():
    snake_tail = Coordinate(0,0)
    snake_head = Coordinate(1,0)
    snake_row = CoordinateRow().append(Coordinate(snake_tail.x, snake_tail.y))
    snake_row += CoordinateRow().append(Coordinate(snake_head.x, snake_head.y))
    snake_direction = Coordinate(1,0)
    snake_length = len(snake_row)
    return snake_row, snake_direction, snake_length

def place_snake(field, coordinate, alive=True):
    if alive:
        field.place(coordinate.x, coordinate.y, game_field.SNAKE)
    if not alive:
        field.place_transparent(coordinate.x, coordinate.y, game_field.SNAKE)
    field.show()

def create_apple(field):
    apple_coordinate = Coordinate()
    apple_coordinate.x = field.random(field.snake_interface.width)
    apple_coordinate.y = field.random(field.snake_interface.height)
    return apple_coordinate

def place_apple(field, coordinate_row, apple_coordinate_row):
    apple = create_apple(field)
    for coordinate in coordinate_row:
        if apple.x == coordinate.x and apple.y == coordinate.y:
            apple = create_apple(field)
    field.place(apple.x, apple.y, field.FOOD)
    field.show()
    apple_coordinate_row.append(apple)

def remove_item(field, coordinate):
    field.place(coordinate.x, coordinate.y, field.EMPTY)
    field.show()

def border_action(field, coordinate):
    if coordinate.x == field.snake_interface.width:
        coordinate.x = 0
    if coordinate.x < 0:
        coordinate.x = field.snake_interface.width-1
    if coordinate.y == field.snake_interface.height:
        coordinate.y = 0
    if coordinate.y < 0:
        coordinate.y = field.snake_interface.height-1
    return coordinate

def game_over(field, event):
    time_left = 10
    field.print_("Game over!\nThis window will close in.. ")
    for i in range(time_left, 0, -1):
        field.print_(str(i))
        field.print_(".. ")
        field.wait(1000)
    field.close()

def game_process(field, event, coordinate_row):
    global apple_stock
    snake_direction = coordinate_row[1]
    snake_length = coordinate_row[2]
    new_head_coordinate = Coordinate()

    if event.name == 'arrow':
        if event.data == RIGHT and snake_direction.x != -1:
            snake_direction.x = 1
            snake_direction.y = 0
        if event.data == LEFT and snake_direction.x != 1:
            snake_direction.x = -1
            snake_direction.y = 0
        if event.data == DOWN and snake_direction.y != -1:
            snake_direction.x = 0
            snake_direction.y = 1
        if event.data == UP and snake_direction.y != 1:
            snake_direction.x = 0
            snake_direction.y = -1
    
    if event.name == 'alarm':
        if len(coordinate_row[0]) > snake_length:
            remove_item(field, coordinate_row[0][0])
            del coordinate_row[0][0]
        
        for coordinate in coordinate_row[0]:
            border_action(field, coordinate)
            place_snake(field, coordinate, True)

        if len(apple_stock.coordinate_row) == 0:
            place_apple(field, coordinate_row[0], apple_stock)
        
        #snake eats apple
        if coordinate_row[0][-1].x == apple_stock.coordinate_row[0].x and coordinate_row[0][-1].y == apple_stock.coordinate_row[0].y:
            snake_length += 1
            del apple_stock.coordinate_row[0]
            new_tail_coordinate = Coordinate(coordinate_row[0][0].x, coordinate_row[0][0].y)
            coordinate_row[0].insert(0, new_tail_coordinate)
        
        #snake eats himself
        for coordinate in coordinate_row[0][0:-2]:
            if coordinate_row[0][-1].x == coordinate.x and coordinate_row[0][-1].y == coordinate.y:
                for coordinate in coordinate_row[0]:
                    place_snake(field, coordinate, False)
                game_over(field, event)

        new_head_coordinate.x = coordinate_row[0][-1].x + snake_direction.x
        new_head_coordinate.y = coordinate_row[0][-1].y + snake_direction.y
        new_head_coordinate = Coordinate(new_head_coordinate.x, new_head_coordinate.y)
        coordinate_row[0].append(new_head_coordinate)

'''
Program
'''
game_field = create_field()
snake = initialize_snake()

game_field.print_("Welcome!\nUse the arrow keys on your keyboard to play.")
while True:
    event = game_field.get_event()
    game_process(game_field, event, snake)
