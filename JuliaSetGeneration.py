#MAY NEED:
# https://ffmpeg.zeranoe.com/builds/
# http://www.wikihow.com/Install-FFmpeg-on-Windows

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import numpy.ma as ma
from matplotlib.colors import ListedColormap
import operator
import math


def main():
	fps = 10
	num_cycles = 25	#number if iterations of the polynomial
	num_points = 500
	number_of_frames = fps*30
	
	FFMpegWriter = manimation.writers['ffmpeg']
	metadata = dict(title='Movie', artist='markers', comment='markers movie')
	writer = FFMpegWriter(fps, metadata=metadata)
	fig = plt.figure()
	
	
	
	colormap = get_colormap((4/15.,4/5.,1.,1.), (1,0,0,1), num_cycles)
	
	
	
	

	
	with writer.saving(fig, "writer_test_2.mp4", 100):
		angle_delta = 2*math.pi /  number_of_frames
		for frame_index in range(number_of_frames):
			print 'frame_index', frame_index, '/', number_of_frames
			
			angle = frame_index*angle_delta
			c = 0.6180*math.cos(angle) + 0.6180j*math.sin(angle)
			indexes = get_indexes(num_cycles, num_points, c)
			plt.imshow(indexes, cmap=colormap)
			
			if frame_index == 0:
				plt.axis('off')
				plt.colorbar()
				
			writer.grab_frame()
			
#END main()


#num_cycles - power looping
#num_points - resolution of the image
def get_indexes(num_cycles, num_points, c):
	y, x = np.ogrid[-1.5:1.5:(num_points*1j), -2:+2:(num_points*1j)]
	
	#mandlebrot
	#c = x + 1j*y
	#z = c			#skip zero to allow indexes to be built
	
	#julia
	z = x + 1j*y
	#c = -0.6180 + 0.0j
	
	
	indexes = num_cycles * np.ones(z.shape)
	for power_index in range(num_cycles):
		print '\tpower_index:', power_index
		
		z = z**2 + c
		
		#oh my god this was a pain in the ass tofigure out...
		m1 = ma.masked_where(np.isfinite(z.real), power_index * np.ones(z.shape))
		m1 = m1.filled(num_cycles)
		indexes = np.minimum(indexes, m1)
		#print 'indexes:', indexes
		
		
	#END for power_index
	indexes = indexes % num_cycles	#set the center to zero
	return indexes
	
	
def get_colormap(c1, c2, num_points):
	#ListedColormap([(1,0,0), (0,1,0), (0,0,1)])
	col = []
	col.append((0,0,0,1))		#set zeroth element to black
	for idx in range(num_points-1):
		degree = 1.0 - (idx/float(num_points))
		#degree = degree**(1.0/2)
		cn = (degree*c1[0]+(1-degree)*c2[0], degree*c1[1]+(1-degree)*c2[1], degree*c1[2]+(1-degree)*c2[2], degree*c1[3]+(1-degree)*c2[3])
		#print degree, cn
		col.append(cn)
	
	return ListedColormap(col)

	
if __name__ == '__main__':
	main()