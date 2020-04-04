from ipy_lib import SnakeUserInterface  #import interface
from Coordinate import Coordinate
from CoordinateRow import CoordinateRow

WIDTH = 32
HEIGHT = 24
FPS = 10
RIGHT = 'r'
LEFT = 'l'
UP = 'u'
DOWN = 'd'

ui = SnakeUserInterface(WIDTH,HEIGHT)   #create GUI object
ui.set_animation_speed(FPS)

apple = Coordinate(0,0)
apple_amount = 0
snake_direction = Coordinate(1,0)
snake_length = 2
direction = RIGHT

'''
Functions
'''
def process_event(event):
    global snake_direction
    global direction
    global snake_row
    global snake_length
    global apple
    global apple_amount
    no_borders(snake_head)
    
    if event.name == 'arrow':
        if event.data == RIGHT and direction != LEFT:
            snake_direction.x = 1
            snake_direction.y = 0
            direction = RIGHT
        if event.data == LEFT and direction != RIGHT:
            snake_direction.x = -1
            snake_direction.y = 0
            direction = LEFT
        if event.data == DOWN and direction != UP:
            snake_direction.x = 0
            snake_direction.y = 1
            direction = DOWN
        if event.data == UP and direction != DOWN:
            snake_direction.x = 0
            snake_direction.y = -1
            direction = UP
        
    if event.name == 'alarm':
        if len(snake_row) > (snake_length):
            remove_item(snake_row[0])
            del snake_row[0]
        
        for coordinate in snake_row:
            no_borders(coordinate)
            place_snake(coordinate)
        
        #snake eats apple
        if snake_head.x == apple.x and snake_head.y == apple.y:
            snake_length += 1
            apple_amount = 0

        #snake eats himself
        for coordinate in snake_row[0:(snake_length-2)]:
            if snake_head.x == coordinate.x and snake_head.y == coordinate.y:
                game_over()
                
        snake_head.x += snake_direction.x
        snake_head.y += snake_direction.y
        place_apple(snake_row)
        snake_row += CoordinateRow().append(Coordinate(snake_head.x, snake_head.y))
          
def place_snake(coordinate):
    ui.place(coordinate.x,coordinate.y,ui.SNAKE)
    coordinate = Coordinate(coordinate.x,coordinate.y)
    ui.show()
    return coordinate
        
def remove_item(coordinate):
    ui.place(coordinate.x,coordinate.y,ui.EMPTY)
    ui.show()

def no_borders(coordinate):
    if coordinate.x == WIDTH:
        coordinate.x = 0
    if coordinate.x < 0:
        coordinate.x = WIDTH-1
    if coordinate.y == HEIGHT:
        coordinate.y = 0
    if coordinate.y < 0:
        coordinate.y = HEIGHT-1
    return coordinate

def place_apple(row):
    global apple_amount
    global apple
    if apple_amount == 1:
        return
    else:
        apple.x = ui.random(WIDTH)
        apple.y = ui.random(HEIGHT)
        for coordinate in row:
            if apple.x == coordinate.x and apple.y == coordinate.y:
                place_apple(row)
        ui.place(apple.x,apple.y,ui.FOOD)
        ui.show()
        apple_amount = 1
        return

def game_over():
    ui.print_("Game over\nThis window will close in 5..")
    ui.wait(1000)
    ui.print_("4..")
    ui.wait(1000)
    ui.print_("3..")
    ui.wait(1000)
    ui.print_("2..")
    ui.wait(1000)
    ui.print_("1..")
    ui.wait(1000)
    ui.close()

'''
Program
'''
#starting positions
snake_tail = Coordinate(0,0)
snake_head = Coordinate(1,0)

snake_row = CoordinateRow().append(Coordinate(snake_tail.x,snake_tail.y))
snake_row += CoordinateRow().append(Coordinate(snake_head.x,snake_head.y))

while True: #infinite loop
    event = ui.get_event()
    process_event(event)
