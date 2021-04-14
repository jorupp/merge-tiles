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

xDirs = [f.path for f in os.scandir(dir) if f.is_dir()]
yFiles = [f.path for xDir in xDirs for f in os.scandir(xDir) if f.is_file()]

xvalues = sorted([int(f.split(os.path.sep)[-1]) for f in xDirs])
yvalues = sorted(list(set([int(f.split(os.path.sep)[-1].split('.')[0]) for f in yFiles])))

xMax = max(xvalues)-min(xvalues)+1
yMax = max(yvalues)-min(yvalues)+1

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
        tileFile = tileFileFormat.format(xvalues[0]+x, yvalues[0]+y)
        if os.path.isfile(tileFile):
            tileImage = Image.open(tileFile)
            image.paste(tileImage, [ x * width, y * height ])
        else:
            print('File does not exist: ' + tileFile)

bar.finish()

outputImageFile = os.path.join(dir, 'output.jpg')
print('writing output image to {}'.format(outputImageFile))
image.save(outputImageFile)
print('finished writing output image to {}'.format(outputImageFile))
