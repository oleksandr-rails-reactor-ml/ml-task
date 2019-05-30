import sys
import pathlib
import itertools
import numpy as np
from PIL import Image

def hash_to_string(x):
	ret = ''
	for i in x.reshape(-1):
		if i == True:
			ret+='1'
		else:
			ret+='0'
	return ret
def diff(x,y):
	res = 0
	for i in range(len(x)):
		if(x[i] != y[i]):
			res +=1
	return res
def average_hash(image, hash_size=8):
	image = image.convert("RGB").resize((hash_size, hash_size), Image.ANTIALIAS)
	pixels = np.asarray(image)
	r = np.zeros(shape = (hash_size, hash_size), dtype = float)
	g = np.copy(r)
	b = np.copy(r)
	for i,j in np.ndindex(r.shape):
			r[i][j] = pixels[i][j][0]
			g[i][j] = pixels[i][j][1]
			b[i][j] = pixels[i][j][2]
	avg_r = r.mean()
	avg_g = g.mean()
	avg_b = b.mean()
	diff_r = r > avg_r
	diff_g = g > avg_b
	diff_b = b > avg_b
	return hash_to_string(diff_r) + hash_to_string(diff_g) + hash_to_string(diff_b)


if len(sys.argv[1:]) == 2 and sys.argv[1] == '--path':
	hashes = []
	for x in pathlib.Path(sys.argv[2]).iterdir():
		with Image.open(x) as im:
			hashes.append((average_hash(im), x.name))
	for x,y in itertools.combinations(hashes,2):
			hash_x, hash_y = x[0], y[0]
			fname_x, fname_y = x[1], y[1]
			if(diff(hash_x, hash_y) <= 10):
				print(fname_x + ' ' + fname_y)
elif len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == '-h'):
	print("""usage: solution.py [-h] --path PATH

First test task on images similarity.

optional arguments:

-h, --help            show this help message and exit

--path PATH           folder with images""")
else:
	print("""usage: solution.py [-h] --path PATH 
solution.py: error: the following arguments are required: --path""")