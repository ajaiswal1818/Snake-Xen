# MIT License
#
# Copyright (c) 2021 Riley Franco
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Python Snake Game

from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 110
SPACE_SIZE = 50
BODY_PARTS = 1
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
highest_score = 10
highest_score_name = "Abhi"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    global direction, score, window, canvas

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)



def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_restart():
    global canvas, score, direction

    canvas.delete("all")
    canvas.delete("gameover")
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    snake = Snake()
    food = Food()
    next_turn(snake, food)



def submit_name(name):
    global highest_score, highest_score_name, score
    if score > highest_score:
        highest_score = score
        highest_score_name = name
    canvas.delete("gameover")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 30), 
	    text="Highest Scorer is {}: {}".format(highest_score_name, highest_score), fill="white", tag="gameover")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50,
            font=('consolas', 30), text="Press R to restart the game", fill="white", tag="gameover")

def game_over():
    global canvas, window, score, label, direction, highest_score, highest_score_name, restart_label

    canvas.delete("all")
    score_text = canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2,
        font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

    your_score_text = canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50,
        font=('consolas', 30), text="Your score: {}".format(score), fill="white", tag="gameover")

    window.bind('<Key-r>', lambda event: game_restart())
    restart_label = canvas.create_text(
            canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 100,
            font=('consolas', 30), text="Press R to restart the game", fill="white", tag="gameover")
    if score > highest_score:
        name_entry_label = canvas.create_text(
            canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 150,
            font=('consolas', 30), text="Enter your name:", fill="white", tag="gameover")

        name_entry = Entry(window, font=('consolas', 30))
        name_entry_window = canvas.create_window(
            canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 200,
            window=name_entry, tag="gameover")

        name_entry_button = Button(
            window, text="Submit",
            command=lambda: submit_name(name_entry.get()),
            font=('consolas', 30))
        name_entry_button_window = canvas.create_window(
            canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 250,
            window=name_entry_button, tag="gameover")


def main():
    try:
        global canvas, window, score, label, direction

        score = 0
        direction = 'down'

        label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
        label.pack()
        window.update()

        window.bind('<Left>', lambda event: change_direction('left'))
        window.bind('<Key-a>', lambda event: change_direction('left'))
        window.bind('<Right>', lambda event: change_direction('right'))
        window.bind('<Key-d>', lambda event: change_direction('right'))
        window.bind('<Up>', lambda event: change_direction('up'))
        window.bind('<Key-w>', lambda event: change_direction('up'))
        window.bind('<Down>', lambda event: change_direction('down'))
        window.bind('<Key-s>', lambda event: change_direction('down'))
        window.bind('<Escape>', lambda event: window.destroy())

        snake = Snake()
        food = Food()

        next_turn(snake, food)
    except Exception as e:
        print("Error during game initialization:", e)
        exit(1)


if __name__ == "__main__":
    global canvas, window
    try:
        window = Tk()
        window.title("Snake Xen")
        window.resizable(False, False)

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        canvas = Canvas(window, bg="black", height=GAME_HEIGHT, width=GAME_WIDTH)
        canvas.pack()
    except Exception as e:
        print("Error initializing the game window:", e)
        exit(1)
	
    def start_game():
        start_button.destroy()
        main()

    start_button = Button(window, text="Start Game", command=start_game, width=15, height=2, font=("Arial", 16))
    start_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    x = (screen_width - window.winfo_reqwidth()) // 6
    y = (screen_height - window.winfo_reqheight()) // 6

    window.geometry("+{}+{}".format(x, y))
    window.mainloop()