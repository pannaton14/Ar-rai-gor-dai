from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

def interpolate_color(start_color, end_color, progress):
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * progress),
        int(start_color[1] + (end_color[1] - start_color[1]) * progress),
        int(start_color[2] + (end_color[2] - start_color[2]) * progress),
        255
    )

class Renderer(Window):
    def __init__(self):
        super().__init__(2000, 600, "Bubble Sort Visualization")  # Adjusted width to fit 58 bars
        self.batch = Batch()
        self.x = [random.randint(5, 30) for _ in range(55)]  # Generate random heights for 58 bars
        self.bars = []

        light_purple = (220, 180, 220)
        dark_purple = (128, 0, 128)

        for e, i in enumerate(self.x):
            progress = e / len(self.x)  # Calculate the progress from 0 to 1
            current_color = interpolate_color(light_purple, dark_purple, progress)

            # Add the color to the Rectangle
            self.bars.append(Rectangle(100 + e * 25, 70, 20, i * 15, color=current_color, batch=self.batch))  # Adjusted position and size

        self.passes = 0
        self.i = 0

    def on_update(self, deltatime):
        n = len(self.x)
        if self.passes < n - 1:
            if self.i < n - 1 - self.passes:
                if self.x[self.i] > self.x[self.i + 1]:
                    self.x[self.i], self.x[self.i + 1] = self.x[self.i + 1], self.x[self.i]
                    self.bars[self.i].height, self.bars[self.i + 1].height = self.bars[self.i + 1].height, self.bars[self.i].height
                self.i += 1
            else:
                self.i = 0
                self.passes += 1

    def on_draw(self):
        self.clear()
        self.batch.draw()

renderer = Renderer()
clock.schedule_interval(renderer.on_update, 0.1)
run()
