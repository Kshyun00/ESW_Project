from PIL import Image, ImageDraw
from paddle import Paddle
from ball import Ball
from brick import Brick
from item import Item
import random
import time

class Game:
    def __init__(self, display):
        self.display = display
        self.display_width = 240  
        self.display_height = 240

        # 게임 시작 화면 이미지 로드
        self.start_screen = Image.open("images/gamestart.png").resize(
            (self.display_width, self.display_height)
        )

        # Game Over 화면 이미지 로드
        self.gameover_screen = Image.open("images/gameover.png").resize(
            (self.display_width, self.display_height)
        )

        self.gameclear_screen = Image.open("images/gameclear.png").resize(
            (self.display_width, self.display_height)
        )

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
        self.balls = [self.ball]

        # 라운드 설정
        self.round = 3

        # 목숨 설정
        self.lives = 3  # 초기 목숨 수
        self.life_icon = Image.open(self.paddle_image_path).resize((20, 10))  # 목숨 아이콘 크기 조정

        # 벽 충돌 범위 (이미지의 테두리에 맞게 설정)
        self.wall_bounds = {
            "left": 25,
            "right": self.display.width - 25,
            "top": 30,
        }

        # 아이템 효과 타이머
        self.laser_timer = None
        self.enlarge_timer = None

        self.bricks = []
        self.initialize_bricks()
        self.items = []  # 현재 화면에 표시되는 아이템 리스트 
        self.lasers = []  # 레이저를 관리하는 리스트


    def show_start_screen(self):
        """게임 시작 화면을 표시."""
        self.display.disp.image(self.start_screen)  # 시작 화면 표시

        # "A" 버튼이 눌릴 때까지 대기
        while True:
            if not self.display.button_A.value:  # "A" 버튼이 눌리면 False
                break

    def initialize_bricks(self):
        self.bricks = []  # 기존 벽돌 제거

        if self.round == 1:
            # 벽돌을 벽 경계 안쪽에 생성
            brick_width = 24
            brick_height = 12
            brick_margin_x = 4
            brick_margin_y = 3

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

        elif self.round == 2:
            brick_width = 24
            brick_height = 12
            brick_margin_x = 4
            brick_margin_y = 3

            colors = [
                (157, 157, 157),  # Gray (2 hit points)
                (255, 0, 0),      # Red
                (255, 255, 0),    # Yellow
                (0, 112, 255),    # Blue
                (255, 0, 255),    # Pink
                (0, 255, 0)       # Green
            ]

            hit_points = [2, 1, 1, 1, 1, 1]

            for y in range(7):
                for x in [0, 1, 2, 4, 5, 6]:
                    brick_x = x * (brick_width + brick_margin_x) + self.wall_bounds["left"]
                    brick_y = y * (brick_height + brick_margin_y) + self.wall_bounds["top"]
                    if y == 0 or y == 6:
                        color = (157, 157, 157)
                        hp = 2
                    else:
                        color = colors[y % len(colors)]
                        hp = hit_points[y % len(hit_points)]
                    self.bricks.append(Brick(brick_x, brick_y, brick_width, brick_height, color=color, hit_points=hp))
            
        elif self.round == 3:
            brick_width = 24
            brick_height = 12
            brick_margin_x = 4
            brick_margin_y = 3
            
            colors = {
                'y': (255, 255, 0),  # Yellow
                'r': (255, 0, 0),    # Red
                'g': (157, 157, 157) # Gray
            }
            
            layout = [
                ['y', None, None, None, None, None, 'y'],
                [None, 'y', None, None, None, 'y', None],
                [None, 'g', 'g', 'g', 'g', 'g', None],
                ['g', 'r', 'g', 'g', 'g', 'r', 'g'],
                ['g', 'g', 'g', 'g', 'g', 'g', 'g'],
                ['g', 'g', 'g', 'g', 'g', 'g', 'g'],
                ['g', 'g', None, None, None, 'g', 'g'],
                [None, 'g', 'g', None, 'g', 'g', None],
                [None, None, 'g', None, 'g', None, None]
            ]
            
            for y, row in enumerate(layout):
                for x, brick_type in enumerate(row):
                    if brick_type:
                        brick_x = x * (brick_width + brick_margin_x) + self.wall_bounds["left"]
                        brick_y = y * (brick_height + brick_margin_y) + self.wall_bounds["top"]
                        self.bricks.append(Brick(brick_x, brick_y, brick_width, brick_height, color=colors[brick_type], hit_points=2 if brick_type == 'g' else 1))


    
    def reset_ball_and_paddle(self):
        """공과 패들의 위치를 초기화."""
        paddle_width = self.paddle.width
        paddle_height = self.paddle.height

        self.paddle.x = (self.display_width - paddle_width) // 2
        self.paddle.y = self.display_height - paddle_height - 10  # 화면 하단에서 약간 위

        new_ball = Ball(self.display)
        new_ball.x = self.paddle.x + self.paddle.width // 2
        new_ball.y = self.paddle.y - new_ball.radius
        new_ball.dx = 6
        new_ball.dy = -6

        self.balls = [new_ball]  # 공 리스트 초기화

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
        
        # 아이템 이동 및 충돌 체크
        for item in self.items[:]:
            item.move()
            if item.check_collision_with_paddle(self.paddle):
                self.apply_item_effect(item.item_type)  # 아이템 효과 적용
                self.items.remove(item)
            elif item.y > self.display_height:
                self.items.remove(item)  # 화면 밖으로 나간 아이템 제거
        
        # 모든 공 업데이트
        for ball in self.balls[:]:
            ball.move()

            # Check ball collision with paddle
            if (
                self.paddle.y < ball.y + ball.radius < self.paddle.y + self.paddle.height
                and self.paddle.x < ball.x < self.paddle.x + self.paddle.width
            ):
                ball.dy = -ball.dy  # 공의 Y 방향 반전
                if self.paddle.move_direction == "left":
                    ball.dx = -abs(ball.dx)  # 공이 왼쪽으로 반사
                elif self.paddle.move_direction == "right":
                    ball.dx = abs(ball.dx)  # 공이 오른쪽으로 반사

            # Check ball collision with walls
            if ball.x - ball.radius <= self.wall_bounds["left"]:
                ball.dx = abs(ball.dx) # 오른쪽으로 반사
            elif ball.x + ball.radius >= self.wall_bounds["right"]:
                ball.dx = -abs(ball.dx) # 왼쪽으로 반사
            if ball.y - ball.radius <= self.wall_bounds["top"]:
                ball.dy = abs(ball.dy) # 아래로 반사
            
            # 벽돌과 충돌 처리
            for brick in self.bricks[:]:  # 모든 벽돌에 대해 검사
                if (
                    brick.x < ball.x < brick.x + brick.width
                    and brick.y < ball.y < brick.y + brick.height
                ):
                    ball.dy = -ball.dy  # 공의 방향 반전
                    brick.hit_points -= 1  # 벽돌의 체력 감소
                    if brick.hit_points <= 0:
                        self.bricks.remove(brick)  # 벽돌 제거
                        # 아이템 생성 로직 추가
                        if random.random() < 0.2:  # 20% 확률로 아이템 생성
                            item_type = random.choice(["laser", "enlarge", "disruption"])
                            self.items.append(Item(brick.x + brick.width // 2, brick.y, item_type, self.display))
                    break  # 한 벽돌만 충돌

            # Check if the ball falls below the screen
            if ball.y > self.display_height:
                self.balls.remove(ball)  # 공 제거
                if not self.balls:  # 모든 공이 사라졌을 때
                    self.lives -= 1
                    if self.lives > 0:
                        self.reset_ball_and_paddle()
                    else:
                        print("Game Over!")
                        self.show_gameover_screen()  # Game Over 화면 표시            
                
        
        # 아이템 효과 관리
        current_time = time.time()

        # 레이저 효과 종료
        if self.laser_timer and current_time > self.laser_timer:
            self.laser_timer = None
            self.paddle.shoot_laser = False

        # 패들 확장 효과 종료
        if self.enlarge_timer and current_time > self.enlarge_timer:
            self.enlarge_timer = None
            self.paddle.change_size(1 / 1.5)  # 패들 크기 및 이미지 원상 복구
        
        # 레이저 이동 및 충돌 체크
        for laser in self.lasers[:]:
            laser["y"] -= 10  # 레이저 위로 이동
            if laser["y"] < 0:  # 화면을 벗어나면 제거
                self.lasers.remove(laser)
            else:
                # 레이저와 벽돌 충돌 체크
                for brick in self.bricks[:]:
                    if (
                        brick.x < laser["x"] < brick.x + brick.width
                        and brick.y < laser["y"] < brick.y + brick.height
                    ):
                        self.bricks.remove(brick)  # 벽돌 제거
                        self.lasers.remove(laser)  # 레이저 제거
                        break  # 하나의 레이저는 한 번만 충돌
        
        # 라운드 변경 벽돌이 모두 파괴되었는지 확인
        if not self.bricks:
            self.round += 1  # 다음 라운드로 이동
            self.initialize_bricks()  # 다음 라운드 벽돌 초기화
            self.reset_ball_and_paddle()  # 공과 패들 초기화
            if self.round > 3:  # 모든 라운드가 끝나면 Game Over
                print("Game Clear! You win!")
                self.show_gameclear_screen()
            else:
                self.initialize_bricks()  # 다음 라운드 벽돌 초기화
                self.reset_ball_and_paddle()  # 공과 패들 초기화

    def start_laser_firing(self):
        """패들이 레이저를 발사."""
        def fire_lasers():
            while self.paddle.shoot_laser:
                self.lasers.append({"x": self.paddle.x + 10, "y": self.paddle.y})
                self.lasers.append({"x": self.paddle.x + self.paddle.width - 10, "y": self.paddle.y})
                time.sleep(0.5)  # 0.5초 간격으로 발사
        
        import threading
        threading.Thread(target=fire_lasers, daemon=True).start()

    def apply_item_effect(self, item_type):
        """아이템 효과를 적용."""
        current_time = time.time()

        if item_type == "laser":
            self.paddle.shoot_laser = True
            self.laser_timer = current_time + 3  # 3초간 지속
            self.start_laser_firing()

        elif item_type == "enlarge":
            if not self.enlarge_timer:  # 중복 적용 방지
                self.paddle.change_size(1.5)  # 패들 크기 및 이미지 확대
                self.enlarge_timer = current_time + 5  # 5초간 지속
                
        elif item_type == "disruption":
            for _ in range(2):
                new_ball = Ball(self.display)
                new_ball.x = self.balls[0].x
                new_ball.y = self.balls[0].y
                new_ball.dx = random.choice([-6,6])
                new_ball.dy = -6
                self.balls.append(new_ball)

    def enable_laser(self):
        """7초 동안 패들이 레이저를 발사."""
        self.paddle.shoot_laser = True
        time.sleep(7)
        self.paddle.shoot_laser = False

    def enlarge_paddle(self):
        """7초 동안 패들을 1.5배로 확장."""
        original_width = self.paddle.width
        self.paddle.width = int(self.paddle.width * 1.5)
        time.sleep(7)
        self.paddle.width = original_width

    def disrupt_ball(self):
        """공을 3개로 늘림."""
        for _ in range(2):
            new_ball = Ball(self.display)
            new_ball.x = self.ball.x
            new_ball.y = self.ball.y
            new_ball.dx = -self.ball.dx  # 방향 변경
            new_ball.dy = self.ball.dy
            self.balls.append(new_ball)

    def show_gameover_screen(self):
        """Game Over 화면을 표시."""
        self.display.disp.image(self.gameover_screen)  # Game Over 화면 표시
        time.sleep(3)  # 3초간 표시
        self.show_start_screen()  # 시작 화면으로 돌아가기
        self.reset_game()  # 게임 전체 초기화

    def show_gameclear_screen(self):
        """Game Clear 화면을 표시."""
        self.display.disp.image(self.gameclear_screen)  # Game Clear 화면 표시
        time.sleep(3)  # 3초간 표시
        self.show_start_screen()  # 시작 화면으로 돌아가기
        self.reset_game()  # 게임 전체 초기화

    def reset_game(self):
        """게임 전체를 초기화."""
        self.round = 1  # 라운드 초기화
        self.lives = 3  # 목숨 초기화
        self.reset_ball_and_paddle()
        self.initialize_bricks()  # 블록 상태를 초기화
        self.items = []  # 아이템 초기화
        self.lasers = []  # 레이저 초기화

    def draw(self):
        """Draw all game elements on the display."""
        # Create a new image as the drawing canvas
        image = self.background.copy()

        # Draw remaining lives
        for i in range(self.lives):
            image.paste(self.life_icon, (5 + i * 25, 5))

        # Use the Image object as the canvas
        self.paddle.draw(image)
        # Draw balls
        for ball in self.balls:
            ball.draw(ImageDraw.Draw(image))
                      
        for brick in self.bricks:
            brick.draw(ImageDraw.Draw(image))  # Draw bricks using ImageDraw
        
        # Draw items
        for item in self.items:
            item.draw(image)
        
        # Draw lasers
        draw = ImageDraw.Draw(image)
        for laser in self.lasers:
            draw.rectangle(
                [laser["x"] - 2, laser["y"], laser["x"] + 2, laser["y"] + 10],
                fill=(255, 0, 0),
            )

        # Display the final rendered image on the screen
        self.display.disp.image(image)

    def run(self):
        """Main game loop."""
        self.show_start_screen()  # 게임 시작 화면 표시
        while True:
            self.update()
            self.draw()
