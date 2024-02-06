from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

class Renderer(Window):
    def __init__(self, start_color=(72, 61, 139), end_color=(47, 79, 79)):
        super().__init__(width=2000, height=600, caption="Merge sort")
        self.batch = Batch()
        self.bar_width = 24
        self.spacing = 2
        self.bars = []
        self.num_bars = 58

        # Start and end colors for gradient
        self.start_color = start_color
        self.end_color = end_color

        # Generate gradient colors
        self.bar_colors = self.generate_gradient_colors()

        self.heights = [random.randint(10, 500) for _ in range(self.num_bars)]
        self.create_bars()

        self.sorting_generator = self.merge_sort(self.heights, 0, len(self.heights) - 1)

    def generate_gradient_colors(self):
        gradient = []
        start_r, start_g, start_b = self.start_color
        end_r, end_g, end_b = self.end_color

        for i in range(self.num_bars):
            ratio = i / (self.num_bars - 1)
            r = int(start_r + ratio * (end_r - start_r))
            g = int(start_g + ratio * (end_g - start_g))
            b = int(start_b + ratio * (end_b - start_b))
            gradient.append((r, g, b))

        return gradient

    def create_bars(self):
        self.bars.clear()

        x = self.spacing
        for height, color in zip(self.heights, self.bar_colors):
            bar = Rectangle(x, 0, self.bar_width, height, batch=self.batch, color=color)
            self.bars.append(bar)
            x += self.bar_width + self.spacing

    def merge_sort(self, arr, start, end):
        if start < end:
            mid = (start + end) // 2
            yield from self.merge_sort(arr, start, mid)
            yield from self.merge_sort(arr, mid + 1, end)
            yield from self.merge(arr, start, mid, end)

    def merge(self, arr, start, mid, end):
        merged = []
        left_idx = start
        right_idx = mid + 1

        while left_idx <= mid and right_idx <= end:
            if arr[left_idx] < arr[right_idx]:
                merged.append(arr[left_idx])
                left_idx += 1
            else:
                merged.append(arr[right_idx])
                right_idx += 1

        while left_idx <= mid:
            merged.append(arr[left_idx])
            left_idx += 1

        while right_idx <= end:
            merged.append(arr[right_idx])
            right_idx += 1

        for i, val in enumerate(merged):
            arr[start + i] = val
            yield arr

    def on_update(self, dt):
        try:
            next(self.sorting_generator)
            self.create_bars()
        except StopIteration:
            clock.unschedule(self.on_update)

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    start_color = (220, 180, 220)  # Lavender
    end_color = (128, 0, 128)       # Indigo
    renderer = Renderer(start_color, end_color)
    clock.schedule_interval(renderer.on_update, 1 / 20.0)  # 20 frames
    run()
