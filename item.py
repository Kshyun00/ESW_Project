from PIL import Image

class Item:
    def __init__(self, x, y, item_type, display):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 12
        self.item_type = item_type  # 아이템 유형: "laser", "enlarge", "disruption"
        self.speed = 3  # 아이템 낙하 속도
        self.image = Image.open(f"images/{item_type}.png").resize((self.width, self.height))
        self.display = display

    def move(self):
        """아이템을 아래로 이동."""
        self.y += self.speed

    def draw(self, canvas):
        """아이템을 화면에 그립니다."""
        canvas.paste(self.image, (self.x, self.y))

    def check_collision_with_paddle(self, paddle):
        """패들과의 충돌을 확인."""
        return (
            self.x < paddle.x + paddle.width
            and self.x + self.width > paddle.x
            and self.y < paddle.y + paddle.height
            and self.y + self.height > paddle.y
        )
