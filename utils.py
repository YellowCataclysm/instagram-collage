import instagram_source as source
import cv2
import numpy

from Worker import DownloadWorker
from Queue import Queue
import multiprocessing

def download_with_workers(urls, resize_widht, resize_height,border=0):
	downloaded_images = [None] * len(urls)
	workers = []
	q = Queue()
	for i in range(multiprocessing.cpu_count()):
		worker = DownloadWorker(q,resize_widht,resize_height,border)
		worker.setDaemon(True)
		worker.start()
		workers.append(worker)
	index = 0
	for url in urls:
		q.put((url, index))
		index += 1
	q.join()
	for w in workers:
		for image, index in w.data:
			downloaded_images[index] = image
	return downloaded_images

def fill_missing_image_urls(num):
	return ['']*num

def merge_horizontally(images):
	rows_num, _ , channels_num = images[0].shape
	result = numpy.zeros([rows_num,0,channels_num],numpy.uint8) # initially create a fake array
	for image in images:
		result = numpy.concatenate((result,image),axis=1)
	return result

def merge_vertically(images):
	_, columns_num, channels_num = images[0].shape
	result = numpy.zeros([0,columns_num,channels_num],numpy.uint8) # initially create a fake array
	for image in images:
		result = numpy.concatenate((result,image),axis=0)
	return result