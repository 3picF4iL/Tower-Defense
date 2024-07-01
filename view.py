import arcade


class DefaultWindow(arcade.Window):
    def __init__(self, width, height, screen_text, screen_color=arcade.color.AMAZON):
        super().__init__(width, height, "Tower Defense Game")
        self.background = screen_color
        self.text = screen_text

    def on_draw(self):
        arcade.draw_text(self.text, self.width / 2, self.height / 2, arcade.color.WHITE_SMOKE, 44)
