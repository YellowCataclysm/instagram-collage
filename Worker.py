from threading import Thread
from Queue import Queue
import urllib
import cv2
import numpy

class DownloadWorker(Thread):
	def __init__(self, queue, widht, height, border_width = 0):
		Thread.__init__(self)
		self.data = []
		self.__queue = queue
		self.__width = widht
		self.__height = height
		#self.__border_color = [144, 238, 144]
		self.__border_width = border_width
		self.__border_color = [0, 0, 0]
		self.__blank_image = numpy.zeros((widht,height,3), numpy.uint8)
		self.__blank_image = self.add_border(self.__blank_image)

	def run(self):
		while True:
			url, index = self.__queue.get()
			if url == '':
				self.data.append((self.__blank_image,index))
			else:
				resp = urllib.urlopen(url)
				img_buffer= numpy.asarray(bytearray(resp.read()), dtype="uint8")
				original_image = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)
				resized_image = self.resized_image(original_image)
				resized_image = self.add_border(resized_image)
				self.data.append((resized_image,index))
			self.__queue.task_done()

	def resized_image(self,image):
		return cv2.resize(image, (self.__width,self.__height), interpolation=cv2.INTER_AREA)

	def add_border(self,image):
		if self.__border_width != 0:
			b = self.__border_width
			return cv2.copyMakeBorder(image,b,b,b,b,cv2.BORDER_CONSTANT,value=self.__border_color)
		return image


