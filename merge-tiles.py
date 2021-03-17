import os
import sys
import time
import progressbar
from PIL import Image

if len(sys.argv) < 2:
    raise Exception('Directory required')

dir = sys.argv[1]

if not os.path.isdir(dir):
    raise Exception('{} is not a directory'.format(dir))

xvalues = sorted([int(f.path.split(os.path.sep)[-1]) for f in os.scandir(dir) if f.is_dir()])
yvalues = sorted([int(f.path.split(os.path.sep)[-1].split('.')[0]) for f in os.scandir(os.path.join(dir, str(xvalues[0]))) if f.is_file()])

xMax = max(xvalues)-min(xvalues)
yMax = max(yvalues)-min(yvalues)

tileFileFormat = os.path.join(os.path.join(dir, '{}'), '{}.png')
sampleImage = Image.open(tileFileFormat.format(xvalues[0], yvalues[0]))
width = sampleImage.width
height = sampleImage.height

image = Image.new(sampleImage.mode, [width * xMax, height * yMax])

print ('loading tile images')
bar = progressbar.ProgressBar(max_value=xMax*yMax)

for x in range(xMax):
    for y in range(yMax):
        bar.update(x*yMax+y)
        tileFile = tileFileFormat.format(xvalues[x], yvalues[y])
        tileImage = Image.open(tileFile)
        image.paste(tileImage, [ x * width, y * height ])

bar.finish()

outputImageFile = os.path.join(dir, 'output.png')
print('writing output image to {}'.format(outputImageFile))
image.save(outputImageFile)
print('finished writing output image to {}'.format(outputImageFile))