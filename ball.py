class Ball:
    def __init__(self, display, radius=3, color=(255, 255, 255)):
        self.display = display
        self.radius = radius  # 공의 반지름
        self.x = self.display.width // 2  # 공의 초기 X 좌표
        self.y = self.display.height // 2  # 공의 초기 Y 좌표
        self.dx = 6  # X축 이동 속도
        self.dy = -6 # Y축 이동 속도
        self.color = color  # 공의 색상

    def move(self):
        """공의 위치를 업데이트하고 화면 경계를 확인."""
        self.x += self.dx
        self.y += self.dy

        # 화면 좌우 벽에 충돌 시 X축 방향 반전
        if self.x <= 0 or self.x >= self.display.width:
            self.dx = -self.dx

        # 화면 상단에 충돌 시 Y축 방향 반전
        if self.y <= 0:
            self.dy = -self.dy

    def draw(self, draw):
        """공을 화면에 그립니다."""
        draw.ellipse(
            [
                self.x - self.radius,  # 왼쪽
                self.y - self.radius,  # 위쪽
                self.x + self.radius,  # 오른쪽
                self.y + self.radius,  # 아래쪽
            ],
            fill=self.color,  # 공의 색상
        )
