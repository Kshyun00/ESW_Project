from PIL import Image, ImageDraw
from paddle import Paddle
from ball import Ball
from brick import Brick

class Game:
    def __init__(self, display):
        self.display = display
        self.display_width = 240  
        self.display_height = 240

        # 배경 이미지 로드 및 디스플레이 크기에 맞게 조정
        self.background = Image.open("images/background.png").resize(
            (self.display_width, self.display_height)
        )

        self.paddle_image_path = "images/paddle.png"  # 패들 이미지 경로 저장
        self.paddle = Paddle(display, self.paddle_image_path, width=70, height=40)
        self.paddle.y -= 10  # 패들의 Y 좌표를 10 픽셀 위로 올림

        self.ball = Ball(display)
        self.ball.x = self.paddle.x + (70 // 2)  # 공의 X 좌표를 패들의 중앙으로 설정
        self.ball.y = self.paddle.y - 3  # 공의 Y 좌표를 패들 위로 설정

        # 벽 충돌 범위 (이미지의 테두리에 맞게 설정)
        self.wall_bounds = {
            "left": 25,
            "right": self.display.width - 25,
            "top": 30,
        }

        # 벽돌을 벽 경계 안쪽에 생성
        brick_width = 24
        brick_height = 12
        brick_margin_x = 4
        brick_margin_y = 3

        # 이미지 기반 블록 레이아웃 구성
        colors = [
            (157, 157, 157),  # 회색: 두 번 튕겨야 없어짐
            (255, 0, 0),      # 빨강
            (255, 255, 0),    # 노랑
            (0, 112, 255),    # 파랑
            (255, 0, 255),    # 분홍
            (0, 255, 0),      # 초록
        ]

        hit_points = [2, 1, 1, 1, 1, 1]  # 첫 줄은 두 번 튕겨야 없어짐

        self.bricks = []
        for y, (color, hp) in enumerate(zip(colors, hit_points)):
            for x in range(7):  # 7개의 열
                brick_x = x * (brick_width + brick_margin_x) + self.wall_bounds["left"]
                brick_y = y * (brick_height + brick_margin_y) + self.wall_bounds["top"]
                self.bricks.append(Brick(brick_x, brick_y, brick_width, brick_height, color=color, hit_points=hp))

        # self.bricks = [
        #     Brick(
        #         x * (brick_width + brick_margin_x) + self.wall_bounds["left"],
        #         y * (brick_height + brick_margin_y) + self.wall_bounds["top"],
        #         brick_width,
        #         brick_height,
        #     )
        #     for y in range(5)  # 5줄의 벽돌
        #     for x in range(7)  # 6개의 열
        # ]


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
        
        # Check ball collision with walls (회색 테두리)
        if self.ball.x - self.ball.radius <= self.wall_bounds["left"]:
            self.ball.dx = abs(self.ball.dx)  # 오른쪽으로 반사
        elif self.ball.x + self.ball.radius >= self.wall_bounds["right"]:
            self.ball.dx = -abs(self.ball.dx)  # 왼쪽으로 반사
        if self.ball.y - self.ball.radius <= self.wall_bounds["top"]:
            self.ball.dy = abs(self.ball.dy)  # 아래로 반사

        # Check ball collision with bricks and remove destroyed bricks
        for brick in self.bricks[:]:  # 복사본을 순회하여 리스트 수정 가능
            if brick.check_collision(self.ball) and brick.hit_points <= 0:
                self.bricks.remove(brick)  # 블록 제거

        # Check for game over
        if self.ball.y > self.display.height:
            print("Game Over!")
            self.reset()

    def reset(self):
        """Reset the game state."""
        self.ball = Ball(self.display)
        self.paddle = Paddle(self.display, self.paddle_image_path, width=70, height=40)  # 패들 이미지 경로 전달

    def draw(self):
        """Draw all game elements on the display."""
        # Create a new image as the drawing canvas
        image = self.background.copy()

        # Use the Image object as the canvas
        self.paddle.draw(image)
        self.ball.draw(ImageDraw.Draw(image))  # Draw ball using ImageDraw
        for brick in self.bricks:
            brick.draw(ImageDraw.Draw(image))  # Draw bricks using ImageDraw

        # Display the final rendered image on the screen
        self.display.disp.image(image)

    def run(self):
        """Main game loop."""
        while True:
            self.update()
            self.draw()
