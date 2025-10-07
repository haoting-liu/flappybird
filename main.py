import turtle
import random
import time

# Set up the screen
screen = turtle.Screen()
screen.title("Flappy Bird - Turtle Version")
screen.bgcolor("lightblue")
screen.setup(width=600, height=800)
screen.tracer(0)

# Bird
bird = turtle.Turtle()
bird.speed(0)
bird.shape("square")
bird.color("yellow")
bird.penup()
bird.goto(-100, 0)
bird.dy = 0

# Pipes
pipes = []
pipe_gap = 200
pipe_width = 80

# Score
score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("black")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 350)
score_display.write("Score: 0", align="center", font=("Arial", 24, "normal"))

# Game state
game_over = False

def jump():
    """Make the bird jump"""
    bird.dy = 8

def create_pipe():
    """Create a new pipe"""
    pipe_top = turtle.Turtle()
    pipe_top.speed(0)
    pipe_top.shape("square")
    pipe_top.color("green")
    pipe_top.shapesize(stretch_wid=random.randint(5, 15), stretch_len=4)
    pipe_top.penup()
    pipe_top.goto(300, 250)
    
    pipe_bottom = turtle.Turtle()
    pipe_bottom.speed(0)
    pipe_bottom.shape("square")
    pipe_bottom.color("green")
    pipe_bottom.shapesize(stretch_wid=random.randint(5, 15), stretch_len=4)
    pipe_bottom.penup()
    pipe_bottom.goto(300, -250)
    
    pipes.append((pipe_top, pipe_bottom))

def check_collision():
    """Check for collisions with pipes or ground"""
    global game_over
    
    # Check ground collision
    if bird.ycor() < -350:
        game_over = True
        return True
    
    # Check pipe collisions
    for pipe_top, pipe_bottom in pipes:
        if (bird.xcor() + 20 > pipe_top.xcor() - 40 and 
            bird.xcor() - 20 < pipe_top.xcor() + 40):
            if (bird.ycor() + 10 > pipe_top.ycor() - pipe_top.shapesize()[0] * 10 or 
                bird.ycor() - 10 < pipe_bottom.ycor() + pipe_bottom.shapesize()[0] * 10):
                game_over = True
                return True
    return False

def update_score():
    """Update the score display"""
    global score
    score += 1
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=("Arial", 24, "normal"))

def game_loop():
    """Main game loop"""
    global game_over, score
    
    # Gravity
    bird.dy -= 0.5
    bird.sety(bird.ycor() + bird.dy)
    
    # Move pipes
    pipes_to_remove = []
    for i, (pipe_top, pipe_bottom) in enumerate(pipes):
        pipe_top.setx(pipe_top.xcor() - 5)
        pipe_bottom.setx(pipe_bottom.xcor() - 5)
        
        # Check if pipe is off screen
        if pipe_top.xcor() < -350:
            pipes_to_remove.append(i)
        
        # Check if bird passed the pipe
        if pipe_top.xcor() + 40 < bird.xcor() - 20 and pipe_top.xcor() + 41 >= bird.xcor() - 20:
            update_score()
    
    # Remove off-screen pipes
    for i in sorted(pipes_to_remove, reverse=True):
        pipes[i][0].hideturtle()
        pipes[i][1].hideturtle()
        del pipes[i]
    
    # Create new pipes occasionally
    if random.random() < 0.02:
        create_pipe()
    
    # Check for collisions
    if check_collision():
        game_over = True
        score_display.goto(0, 0)
        score_display.write("GAME OVER\nClick to restart", align="center", font=("Arial", 24, "normal"))
        return
    
    screen.update()
    
    if not game_over:
        screen.ontimer(game_loop, 30)

def restart_game(x, y):
    """Restart the game"""
    global game_over, score, pipes
    
    if game_over:
        # Reset game state
        game_over = False
        score = 0
        
        # Clear pipes
        for pipe_top, pipe_bottom in pipes:
            pipe_top.hideturtle()
            pipe_bottom.hideturtle()
        pipes = []
        
        # Reset bird
        bird.goto(-100, 0)
        bird.dy = 0
        
        # Reset score display
        score_display.clear()
        score_display.goto(0, 350)
        score_display.write("Score: 0", align="center", font=("Arial", 24, "normal"))
        
        # Start game loop
        game_loop()

# Set up controls
screen.listen()
screen.onkeypress(jump, "space")
screen.onkeypress(jump, "Up")
screen.onclick(restart_game)

# Start the game
create_pipe()  # Create initial pipe
game_loop()

screen.mainloop()