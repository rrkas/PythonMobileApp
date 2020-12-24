from kivy.app import App
from kivy.uix.widget import Widget  # user interface
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # latest position = current velocity + current position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    paddle1 = ObjectProperty(None)
    paddle2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(6, 0).rotate(randint(-360, 360))

    def update(self, dt):
        self.ball.move()
        # bounce top and bottom
        if (self.ball.y < 0) or (self.ball.y + self.ball.height > self.height):
            self.ball.velocity_y *= -1
        # bounce left and right
        if (self.ball.x < 0) or (self.ball.x + self.ball.width > self.width):
            if self.ball.x < 0:
                self.paddle2.score += 1
            else:
                self.paddle1.score += 1
            self.ball.velocity_x *= -1
        self.paddle1.bounce_ball(self.ball)
        self.paddle2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width * 1 / 4:
            self.paddle1.center_y = touch.y
        if touch.x > self.width * 3 / 4:
            self.paddle2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
