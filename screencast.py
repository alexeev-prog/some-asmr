import pygame as pg
from pygame_screen_record import ScreenRecorder

pg.init()

recorder = ScreenRecorder(60)
recorder.start_rec()

try:
	while True:
		pass
finally:
	recorder.stop_rec()
	recorder.save_recording("example.mp4")
	pg.quit()
