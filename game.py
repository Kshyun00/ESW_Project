from PIL import Image, ImageDraw
from paddle import Paddle
from ball import Ball
from brick import Brick

class Game:
    def __init__(self, display):
        self.display = display
        self.paddle = Paddle(display)
        self.ball = Ball(display)
        self.bricks = [Brick(x * 40, y * 20, 38, 18) for y in range(5) for x in range(8)]

    def update(self):
        # Read joystick input for paddle movement
        if not self.display.button_L.value:  # 왼쪽 버튼
            self.paddle.move("left")
        elif not self.display.button_R.value:  # 오른쪽 버튼
            self.paddle.move("right")
        elif not self.display.button_U.value:  # 위쪽 버튼
            self.paddle.move("up")
        elif not self.display.button_D.value:  # 아래쪽 버튼
            self.paddle.move("down")
        else:
            self.paddle.move_direction = None  # 버튼이 눌리지 않을 때 이동 방향 초기화

        # Move ball and check collisions
        self.ball.move()

        # Check ball collision with paddle
        if (
            self.paddle.y < self.ball.y + self.ball.radius < self.paddle.y + self.paddle.height
            and self.paddle.x < self.ball.x < self.paddle.x + self.paddle.width
        ):
            self.ball.dy = -self.ball.dy  # 공의 Y 방향 반전
            # 공의 X 방향은 패들의 이동 방향에 따라 반영
            if self.paddle.move_direction == "left":
                self.ball.dx = -abs(self.ball.dx)  # 공이 왼쪽으로 반사
            elif self.paddle.move_direction == "right":
                self.ball.dx = abs(self.ball.dx)  # 공이 오른쪽으로 반사

        # Check ball collision with bricks
        for brick in self.bricks:
            brick.check_collision(self.ball)

        # Check for game over
        if self.ball.y > self.display.height:
            print("Game Over!")
            self.reset()

    def reset(self):
        """Reset the game state."""
        self.ball = Ball(self.display)
        self.paddle = Paddle(self.display)

    def draw(self):
        """Draw all game elements on the display."""
        image = Image.new("RGB", (self.display.width, self.display.height))
        draw = ImageDraw.Draw(image)

        # Draw paddle, ball, and bricks
        self.paddle.draw(draw)
        self.ball.draw(draw)
        for brick in self.bricks:
            brick.draw(draw)

        self.display.disp.image(image)

    def run(self):
        """Main game loop."""
        while True:
            self.update()
            self.draw()
