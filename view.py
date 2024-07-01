import arcade


class DefaultView(arcade.View):
    def __init__(self, screen_text, screen_color=arcade.color.AMAZON):
        super().__init__()
        arcade.set_background_color(screen_color)
        self.text = screen_text

    def on_draw(self):
        arcade.draw_text(self.text, 50, self.window.height / 2, arcade.color.WHITE_SMOKE, 44)
