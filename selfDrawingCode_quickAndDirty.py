#  by Kristin Henry, 2013  @KristinHenry
#
#  other monospaced fonts can be found here http://www.fontsquirrel.com/fonts/list/classification/monospaced

import PIL
from PIL import Image
import ImageFont, ImageDraw
import random
import math


filename = "selfDrawingCode_quickAndDirty.py"
fontname = "Anonymous_Pro.ttf"   # change this to a font you have

imgSizeX = imgSizeY = 500	# set default size of image
backgroundColor = "white"
backgroundColorAlpha = "white"

maxX = imgSizeX -10
minX = 10
maxY = imgSizeY -10
minY = 10

rMax = 60
dxMax = 0
dyMax = 0
buff = 50
dx = 0
dy = 0

letters = []
counts = []
letterColors = {}

baseColor = [random.randrange(0,255), random.randrange(0,255), random.randrange(0,255), 100]

xy = [(maxX - minX)/2 + random.randrange(-100, 100), (maxY - minY)/2 + random.randrange(-100, 100)]
angle = 0


def getLetters():
	for line in data:
		for char in line:
			if (char != '\n') & (char != '\t'):
				countLetters(char)


def countLetters(char):
	global letters
	global counts
	if char in letters:
		i = letters.index(char)
		counts[i] += 1
	else:
		letters.append(char)
		counts.append(1)


def getLetterColors():
	global letters
	global counts
	global letterColors
	global baseColor

	for char in letters:
		i = letters.index(char)
		count = counts[i]

		red = (baseColor[0] + (count * random.randrange(1, 5))) % 255
		grn = (baseColor[1] + (count * random.randrange(1, 5))) % 255
		blu = (baseColor[2] + (count * random.randrange(1, 5))) % 255

		color = [red, grn, blu, baseColor[3]]
		letterColors[char] = color
	

def getXYfromChar(char):
	global xy
	global angle

	r = random.randrange(10, 20) 

	if char == ' ':
		# change direction of growth for next dots
		angle += random.randrange(10, 20)

	xy[0] += int(math.floor(r * math.cos(angle)))
	xy[1] += int(math.floor(r * math.sin(angle)))

	return [xy[0],xy[1]]


def getDots():
	global letterColors
	dots = []
	# pre-process code from text file
	for line in data:
		for char in line:
			if char == '\n':
				char = ' '
			if (char != '\n') & (char != '\t'):

				xy = getXYfromChar(char)
				
				getLetterColors()
				c = letterColors[char]
				dot = [char, xy, c]
				dots.append(dot)
						
	return dots


def getDotsMinMax():
	global dots

	xMin = xMax = 500
	yMin = yMax = 500

	i = 0
	for dot in dots:
		p = dot[1]
		
		xMin = p[0] if p[0] < xMin else xMin
		xMax = p[0] if p[0] > xMax else xMax

		yMin = p[1] if p[1] < yMin else yMin
		yMax = p[1] if p[1] > yMax else yMax

	return [xMin, yMin, xMax, yMax]


def shiftDots():
	global dots
	global minmax
	global dx
	global dy

	dx = -int(minmax[0]) if minmax[0] > 0 else int(math.fabs(minmax[0]))
	dy = -int(minmax[1]) if minmax[1] > 0 else int(math.fabs(minmax[1]))

	for dot in dots:
		p = dot[1]
		p[0] += dx + rMax + buff
		p[1] += dy + rMax + buff


def resizeImage():
	global minmax
	global imgSizeX
	global imgSizeY
	global dx
	global dy

	imgSizeX = int(minmax[2]) + dx + 2*(rMax + buff) 
	imgSizeY = int(minmax[3]) + dy + 2*(rMax + buff)		


def drawDots(draw):
	for dot in dots:
		x = dot[1][0] 
		y = dot[1][1] 
		c = dot[2]
		char = dot[0]
		r = rMax 
		c[3] = 60
		dx = 0 
		dy = 0 
		draw.ellipse((x-r + dx, y-r + dy, x+r + dx, y+r + dy), fill=tuple(c))
		list(c)


def drawChars(draw):
	for dot in dots:
		dx = random.randrange(-100, 100)
		dy = random.randrange(-100, 100)
		x = dot[1][0] 
		y = dot[1][1] 
		xy = (x + dx,y + dy)
		c = dot[2]
		char = dot[0]
		c[3] = 255
		fontsize = 42 
		font = ImageFont.truetype(fontname, fontsize)
		draw.text(xy, char, font=font, fill=tuple(c))
		list(c)


#----------------------
# get code as text data
with open(filename) as f:
    data = f.readlines()


# clean up the txt file
for line in data:
	line.replace("\n", " ")


# preprocess data
getLetters()
dots = getDots()
minmax = getDotsMinMax()

# adjust positions and image size
shiftDots()
resizeImage()


# create background 
bkg = Image.new("RGB", (imgSizeX, imgSizeY), backgroundColor)

# create new image to draw into
im = Image.new("RGBA", (imgSizeX, imgSizeY), backgroundColorAlpha)

# Do the drawing
draw = ImageDraw.Draw(im)
drawDots(draw)
#drawChars(draw)  # if on linux, can uncomment this

bkg.paste(im, (0,0), im)

# save image with source file name, but with png suffix
bkg.save(filename[:-2] + "png")

