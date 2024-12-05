class Brick:
    def __init__(self, x, y, width, height, color=(0, 255, 0), hit_points=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hit_points = hit_points  # 블록이 없어지기 전 튕겨야 하는 횟수

    def check_collision(self, ball):
        """공과의 충돌을 확인하고 블록의 hit_points를 감소시킵니다."""
        if (
            self.x < ball.x < self.x + self.width
            and self.y < ball.y < self.y + self.height
        ):
            ball.dy = -ball.dy  # 공의 Y 방향 반전
            self.hit_points -= 1  # 충돌 시 블록의 hit_points 감소
            return True  # 충돌 발생
        return False

    def draw(self, draw):
        """블록을 화면에 그립니다."""
        if self.hit_points > 0:
            # Draw black border (slightly larger rectangle)
            border_thickness = 2 # 경계선 두께
            draw.rectangle(
                [
                    self.x - border_thickness,
                    self.y - border_thickness,
                    self.x + self.width + border_thickness,
                    self.y + self.height + border_thickness,
                ],
                outline=(0, 0, 0),  # 검은색 경계선
                fill=(0, 0, 0),     # 검은색 배경
            )
            
            # Draw the inner colored rectangle
            draw.rectangle(
                [self.x, self.y, self.x + self.width, self.y + self.height],
                fill=self.color,  # 블록의 색상
            )
