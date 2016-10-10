import argparse

from Worker import DownloadWorker
from utils import *
from instagram_source import *

parser = argparse.ArgumentParser()
parser.add_argument("--user", help="Instagram account name to be used as source of images", required=True)
parser.add_argument("--num_photos", help="number of photos to use in collage.", type=int, default=0)
parser.add_argument("--rows", help="number of rows in collage", type=int, default=5)
parser.add_argument("--cols", help="number of columns in collage", type=int, default=5)
parser.add_argument("--cell_width", help="width of a single cell in pixels", type=int, default=128)
parser.add_argument("--cell_height", help="height of a single cell in pixels", type=int, default=128)
parser.add_argument("--border", help="Add black borders to cells and extra border to whole image", type=int, default=0)
parser.add_argument("-o", "--output", help="Output file name.", default='collage.png')
parser.add_argument("-s", "--show", help="Show collage after script complete", action="store_true")

args = parser.parse_args()

username = args.user
rows = args.rows
if rows <= 0: print "Error: Rows should be greater than zero", quit()

columns = args.cols
if columns <= 0: print "Error: Cols should be greater than zero", quit()

width = args.cell_width
if width <= 0: print "Error: Width should be greater than zero", quit()

height = args.cell_height
if height <= 0: print "Error: Height should be greater than zero", quit()

num_photos = args.num_photos
if num_photos < 0 : print "Error: Height should be equal or greater than zero", quit()
if num_photos == 0: num_photos = rows * columns
elif num_photos > rows * columns: num_photos = rows * columns


out = args.output
border = args.border
if border < 0 : border = 0

print "Fetching media info..."
urls = source.get_images_urls(username, num_photos)
urls.extend(fill_missing_image_urls( rows * columns - len(urls) ))

print "Downloading content..."
images = download_with_workers(urls, width, height, border)

print "Processing..."
merged_rows = []
offset = 0
for i in range(0,rows):
	merged_rows.append(merge_horizontally(images[offset:offset+columns]))
	offset += columns
result = merge_vertically(merged_rows)

if border != 0:
	b = border
	result = cv2.copyMakeBorder(result,b,b,b,b,cv2.BORDER_CONSTANT,value=[0,0,0])

cv2.imwrite(out, result)
if args.show is True:
	cv2.imshow(out, result)
if cv2.waitKey() & 0xff == 27: quit()
