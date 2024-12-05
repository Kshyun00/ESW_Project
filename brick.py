class Brick:
    def __init__(self, x, y, width, height, color=(0, 255, 0), hit_points=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hit_points = hit_points  

    def check_collision(self, ball):
        """공과의 충돌을 확인하고 블록의 hit_points를 감소시킴."""
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
            border_thickness = 2 # 경계선 두께
            #경계선 블럭
            draw.rectangle(
                [
                    self.x - border_thickness,
                    self.y - border_thickness,
                    self.x + self.width + border_thickness,
                    self.y + self.height + border_thickness,
                ],
                outline=(0, 0, 0),  
                fill=(0, 0, 0),     
            )
            #내부 색깔 블럭
            draw.rectangle(
                [self.x, self.y, self.x + self.width, self.y + self.height],
                fill=self.color, 
            )
