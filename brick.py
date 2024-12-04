class Brick:
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = True

    def check_collision(self, ball):
        if (
            self.active
            and self.x < ball.x < self.x + self.width
            and self.y < ball.y < self.y + self.height
        ):
            self.active = False
            ball.dy = -ball.dy
            return True
        return False

    def draw(self, draw):
        if self.active:
            draw.rectangle(
                [self.x, self.y, self.x + self.width, self.y + self.height],
                fill=self.color,
            )
