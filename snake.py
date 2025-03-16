import tkinter
import random  
from tkinter import messagebox

# Constants
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS  # 25*25 = 625
WINDOW_HEIGHT = TILE_SIZE * ROWS  # 25*25 = 625

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Game window setup
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Game variables
snake = None
food = None
velocityX = 0
velocityY = 0
snake_body = []
game_over = False
score = 0

def reset_game():
    """Resets the game state and restarts the loop correctly."""
    global snake, food, velocityX, velocityY, snake_body, game_over, score

    # Reset game variables
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)  # Reset snake position
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)  # Reset food position
    velocityX = 0
    velocityY = 0
    snake_body = []  # Empty the snake body
    game_over = False
    score = 0

    # 🔄 Restart the game loop correctly (Only one `window.after()` call)
    window.after(200, draw)

def change_direction(e):
    """Handles key press events to change the snake's direction."""
    global velocityX, velocityY, game_over

    if game_over and e.keysym == "space":
        ask_restart()
        return

    if game_over:
        return  # Prevent movement if the game is over

    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0

def move():
    """Moves the snake forward based on its velocity."""
    global snake, food, snake_body, game_over, score

    if game_over:
        return
    
    # Check collision with walls
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return
    
    # Check collision with itself
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return
    
    # Check if the snake eats the food
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))  # Grow the snake
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    # Update snake body
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    # Move snake head
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    """Renders the game elements and updates the game loop."""
    global snake, food, snake_body, game_over, score

    move()  # Move the snake
    canvas.delete("all")  # Clear the canvas

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

    # Draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='lime green')

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='lime green')

    # Display Game Over message
    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20", text=f"Game Over: {score}", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")

    # 🏁 Schedule the next frame (only one active at a time)
    if not game_over:
        window.after(200, draw)

def ask_restart():
    """Displays a restart prompt when the game is over."""
    global game_over
    if game_over:
        response = messagebox.askyesno("Game Over", f"Your score: {score}\nDo you want to play again?")
        if response:
            reset_game()  # Restart the game

# Call reset_game after defining draw()
reset_game()

# Bind key events
window.bind("<KeyRelease>", change_direction)  

# Start the game loop
window.mainloop()
