#  by Kristin Henry, 2013  @KristinHenry
#
#  other monospaced fonts can be found here http://www.fontsquirrel.com/fonts/list/classification/monospaced

import random, math

import PIL
from PIL import Image
import ImageFont, ImageDraw


class selfDrawingCode :

	def __init__(self, fontname=None) :

		self.fontname = "Anonymous_Pro.ttf"   # change this to a font you have

		

		self.rMax = 60
		self.buff = 50
		self.dx = 0
		self.dy = 0
		self.dxMax = 0
		self.dyMax = 0

		
		imgSize = [500, 500] # set default size of image, will be resized
		border = 10
		maxX = imgSize[0] - border
		maxY = imgSize[1] - border
		minX = border
		minY = border
		self.xy = [(maxX - minX)/2 + random.randrange(-100, 100), (maxY - minY)/2 + random.randrange(-100, 100)]
		self.angle = 0

		
		# get code as text data
		filename = "selfDrawingCode_oop.py" # ToDo: get the name of this file automatically
		try :
			data = open(filename).readlines()
		except :
			data = ""
			print "Error reading file: ", filename

		# preprocess data
		letters = []
		counts = []
		self.getLetters(data, letters, counts)

		baseColor = [random.randrange(0,255), random.randrange(0,255), random.randrange(0,255), 100]
		letterColors = self.getLetterColors(letters, counts, baseColor)
		
		dots = self.getDots(data, letterColors)
		self.minmax = self.getDotsMinMax(dots)

		# adjust positions of dots and image size, so that image contains all dots
		self.shiftDots(dots)
		self.resizeImage(imgSize)

		# create background  and image to draw into
		backgroundColor = "white"
		backgroundColorAlpha = "white"
		bkg = Image.new("RGB", (imgSize[0], imgSize[1]), backgroundColor)
		im = Image.new("RGBA", (imgSize[0], imgSize[1]), backgroundColorAlpha)
		draw = ImageDraw.Draw(im)
		
		# Do the drawing
		self.drawDots(draw, dots)
		#drawChars(draw)  # if on linux, you may uncomment this

		bkg.paste(im, (0,0), im)

		# save image with source file name, but with png suffix
		bkg.save(filename[:-2] + "png")



	def getLetters(self, data, letters, counts):
		for line in data:
			for char in line:
				if (char != '\n') & (char != '\t'):
					self.countLetters(char, letters, counts)
		

	def countLetters(self, char, letters, counts):
		if char in letters:
			i = letters.index(char)
			counts[i] += 1
		else:
			letters.append(char)
			counts.append(1)


	def getLetterColors(self, letters, counts, baseColor):

		letterColors = {}

		for char in letters:
			i = letters.index(char)
			count = counts[i]

			red = (baseColor[0] + (count * random.randrange(1, 5))) % 255
			grn = (baseColor[1] + (count * random.randrange(1, 5))) % 255
			blu = (baseColor[2] + (count * random.randrange(1, 5))) % 255

			color = [red, grn, blu, baseColor[3]]
			letterColors[char] = color

		return letterColors
		

	def getXYfromChar(self, char):
		xy = self.xy
		angle = self.angle

		r = random.randrange(10, 20) 

		if char == ' ':
			# change direction of growth for next dots
			angle += random.randrange(10, 20)

		xy[0] += int(math.floor(r * math.cos(angle)))
		xy[1] += int(math.floor(r * math.sin(angle)))

		return [xy[0],xy[1]]


	def getDots(self, data, letterColors):
		
	 	dots = []
		# determin position and color of each character in code from text file
		for line in data:
			for char in line:
				if char == '\n':
					char = ' '
				if (char != '\n') & (char != '\t'):
					xy = self.getXYfromChar(char)
					c = letterColors[char]
					dot = [char, xy, c]
					dots.append(dot)
							
		return dots


	def getDotsMinMax(self, dots):
		
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


	def shiftDots(self, dots):
		
		minmax = self.minmax
		dx = self.dx
		dy = self.dy

		dx = -int(minmax[0]) if minmax[0] > 0 else int(math.fabs(minmax[0]))
		dy = -int(minmax[1]) if minmax[1] > 0 else int(math.fabs(minmax[1]))

		for dot in dots:
			p = dot[1]
			p[0] += dx + self.rMax + self.buff
			p[1] += dy + self.rMax + self.buff	


	def resizeImage(self, imgSize):
		imgSize[0] = int(self.minmax[2]) + self.dx + 2*(self.rMax + self.buff) 
		imgSize[1] = int(self.minmax[3]) + self.dy + 2*(self.rMax + self.buff)	


	def drawDots(self, draw, dots):
		for dot in dots:
			x = dot[1][0] 
			y = dot[1][1] 
			c = dot[2]
			char = dot[0]
			r = self.rMax 
			c[3] = 60
			dx = 0 
			dy = 0 
			draw.ellipse((x-r + dx, y-r + dy, x+r + dx, y+r + dy), fill=tuple(c))
			list(c)




artist = selfDrawingCode()

