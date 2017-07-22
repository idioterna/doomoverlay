# https://github.com/id-Software/DOOM/blob/master/linuxdoom-1.10/f_wipe.c
from PIL import Image
import numpy as np
import sys

# 1920 / 640 = 3
# 1920 / 320 = 6

class Wipe(object):
	SX = 6
	SY = 32

	DY = 64
	A = 32

	VX = 1920
	VY = 1080

	def __init__(self):
		self.y = np.empty(self.VX//self.SX, dtype=np.int)
		y0 = -np.random.randint(self.A)

		for i in range(self.y.shape[0]):
			self.y[i] = y0
			y0 = np.clip(y0 + np.random.randint(-2, 3), -self.A+1, 0)

		self.y = self.y * self.SY

		self.N = (self.VY - np.amin(self.y))//self.DY+1

	def render(self, start, end, n):
		# start = starting pic
		# end = ending pic
		# n = frame number - 0, 1, 2, ..., N-1
		frame = np.array(end)

		dy = np.clip(self.y + n * self.DY, 0, self.VY)

		for i in range(self.VX):
			j = i//self.SX
			frame[dy[j]:,i] = start[0:self.VY-dy[j],i]

		return frame

def main():
	pstart, pend = sys.argv[1:]

	blank = Image.new("RGB", (1920,1080))
	ablank = np.asarray(blank)

	i = 1
	for j in range(10):
		wipe = Wipe()
		for n in range(wipe.N+25):
			end = Image.open("frames/frame%04d.jpg" % i)
			aend = np.asarray(end)

			aframe = wipe.render(ablank, aend, n)
			frame = Image.fromarray(aframe)

			frame.save("wipe/wipe%04d.png" % i)

			i += 1

		wipe = Wipe()
		for n in range(wipe.N):
			start = Image.open("frames/frame%04d.jpg" % i)
			astart = np.asarray(start)

			aframe = wipe.render(astart, ablank, n)
			frame = Image.fromarray(aframe)

			frame.save("wipe/wipe%04d.png" % i)

			i += 1

if __name__ == "__main__":
	main()
