from PIL import Image

class Paddle:
    def __init__(self, display, image_path, width=50, height=10):
        self.display = display
        self.width = width
        self.height = height
        self.x = (self.display.width - self.width) // 2
        self.y = self.display.height - 20
        self.dx = 0  # 패들의 수평 이동 방향 (-1: 왼쪽, 1: 오른쪽)
        self.dy = 0  # 패들의 수직 이동 방향 (-1: 위, 1: 아래)
        self.image = Image.open(image_path).resize((self.width, self.height))  # 이미지를 로드하고 크기 조정

    def move(self, direction):
        """패들의 움직임을 조작."""
        if direction == "left" and self.x > 0:
            self.x -= 5
            self.dx = -1
        elif direction == "right" and self.x < (self.display.width - self.width):
            self.x += 5
            self.dx = 1
        elif direction == "up" and self.y > 0:
            self.y -= 5
            self.dy = -1
        elif direction == "down" and self.y < (self.display.height - self.height):
            self.y += 5
            self.dy = 1
        else:
            self.dx = 0
            self.dy = 0  # 정지 상태

    def draw(self, canvas):
        """패들을 화면에 그립니다."""
        canvas.paste(self.image, (self.x, self.y), self.image.convert("RGBA"))  # 이미지 렌더링
