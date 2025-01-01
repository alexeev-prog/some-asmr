import math
import pygame as pg
from cardioid.pygame_recorder import ScreenRecorder


class Cardioid:
	def __init__(self, app):
		self.app = app

		self.radius = 200
		self.num_lines = 200

		self.translate = self.app.screen.get_width() // 2, self.app.screen.get_height() // 2

		self.counter, self.inc = 0, 0.01

	def get_color(self):
		self.counter += self.inc
		self.counter, self.inc = (self.counter, self.inc) if 0 < self.counter < 1 else (
			max(min(self.counter, 1), 0), -self.inc)

		return pg.Color('red').lerp('orange', self.counter)

	def draw(self):
		time = pg.time.get_ticks()
		self.radius = 175 + 25 * abs(math.sin(time * 0.002) - 0.25)
		# factor = 1 + 0.0001 * time
		factor = 2

		for i in range(self.num_lines):
			theta = (2 * math.pi / self.num_lines) * i
			x1 = int(self.radius * math.cos(theta)) + self.translate[0]
			y1 = int(self.radius * math.sin(theta)) + self.translate[1]

			x2 = int(self.radius * math.cos(factor * theta)) + self.translate[0]
			y2 = int(self.radius * math.sin(factor * theta)) + self.translate[1]

			pg.draw.aaline(self.app.screen, self.get_color(), (x1, y1), (x2, y2))


class App:
	def __init__(self):
		pg.init()

		self.screen = pg.display.set_mode([450, 750])
		self.clock = pg.time.Clock()
		self.FPS = 60
		self.cardioid = Cardioid(self)

		self.font = pg.font.Font("mono.otf", 24)

		self.recorder = ScreenRecorder(450, 750, 60)

	def print(self, text, position, rgb_channel=(255,255,255), font_size=32):
		self.font = pg.font.Font("terminess.ttf", font_size)

		text_surface = self.font.render(text, True, rgb_channel)
		self.screen.blit(text_surface, position)

	def draw(self):
		self.screen.fill('black')

		self.cardioid.draw()

		self.print("Heart Cardioid", (120, 30), rgb_channel=(255, 100, 100))
		self.print("Subscribe to channel", (110, 80), font_size=26)

		pg.display.flip()
		pg.display.update()

	def run(self):
		while True:
			self.draw()

			for event in pg.event.get():
				if event.type == pg.QUIT:
					exit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						exit()

			self.recorder.capture_frame(self.screen)

			self.clock.tick(self.FPS)

		self.recorder.end_recording()


if __name__ == '__main__':
	app = App()
	app.run()
