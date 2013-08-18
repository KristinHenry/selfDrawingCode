#  by Kristin Henry, 2013  @KristinHenry
#
#  other monospaced fonts can be found here http://www.fontsquirrel.com/fonts/list/classification/monospaced

import random, math

import PIL
from PIL import Image, ImageFont, ImageDraw


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
		
		# get code as text data
		filename = "selfDrawingCode_oop.py" # ToDo: get the name of this file automatically
		try :
			data = open(filename).readlines()
		except :
			data = ""
			print "Error reading file: ", filename

		# preprocess data
		letterCounts = self.getLetters(data)
		# idea: do visualization of interesing chars like {} for dictionaries, etc

		# get random base color, use as common seed for colors based on letter frequencies in the code
		baseColor = [random.randrange(0,255), random.randrange(0,255), random.randrange(0,255), 100]
		letterColors = self.getLetterColors(letterCounts, baseColor)
		
		# get initial positions and colors for each char in code
		# randomizing a little, so that each generated image is different
		x_initial = (imgSize[0] - (2*border))/2 + random.randrange(-100, 100)
		y_initial = (imgSize[1] - (2*border))/2 + random.randrange(-100, 100)
		angle_initial = 0
		xya = [x_initial, y_initial, angle_initial]  # ToDo: better name for this variable
		dots = self.getDots(data, letterColors, xya)

		# get extreme positions of the resulting dots
		self.minmax = self.getDotsMinMax(dots)

		# adjust positions of dots and image size, so that image contains all dots
		self.shiftDots(dots)
		imgSize = self.resizeImage(imgSize)
		# print imgSize

		# create background  and image to draw into
		backgroundColor = "white"
		backgroundColorAlpha = "white"
		bkg = Image.new("RGB", (imgSize[0], imgSize[1]), backgroundColor)
		im = Image.new("RGBA", (imgSize[0], imgSize[1]), backgroundColorAlpha)
		draw = ImageDraw.Draw(im)

		# Do the drawing
		r = 50
		self.drawDots(draw, dots, r)
		#drawChars(draw)  # if on linux, you may uncomment this

		# paste drawing onto image background--attempting to blend alphas of dots
		bkg.paste(im, (0,0), im)

		# save image with source file name, but with png suffix
		bkg.save(filename[:-2] + "png")


	def getLetters(self, data):

		letterCounts = {}
		for line in data:
			for char in line:
				if (char != '\n') & (char != '\t'):
					self.countLetters(char, letterCounts)
		return letterCounts
		

	def countLetters(self, char, letterCounts):

		if char in letterCounts:
			letterCounts[char] += 1
		else:
			letterCounts[char] = 1


	def getLetterColors(self, letterCounts, baseColor):

		letterColors = {}

		for char in letterCounts:
			count = letterCounts[char]

			red = (baseColor[0] + (count * random.randrange(1, 5))) % 255
			grn = (baseColor[1] + (count * random.randrange(1, 5))) % 255
			blu = (baseColor[2] + (count * random.randrange(1, 5))) % 255

			color = [red, grn, blu, baseColor[3]]
			letterColors[char] = color

		return letterColors
		

	def getXYfromChar(self, char, xya):

		angle = xya[2]

		r = random.randrange(10, 20) 

		if char == ' ':
			# change direction of growth for next dots
			xya[2] += random.randrange(10, 20)
			if xya[2] >= 360:
				xya[2] = 0

		xya[0] += int(math.floor(r * math.cos(angle)))
		xya[1] += int(math.floor(r * math.sin(angle)))

		return xya


	def getDots(self, data, letterColors, xya):
		pos = xya
	 	dots = []
		# determin position and color of each character in code from text file
		for line in data:
			for char in line:
				if char == '\n':
					char = ' '
				if (char != '\n') & (char != '\t'):
					xya = self.getXYfromChar(char, xya)
					pos = [xya[0], xya[1], xya[2]]
					c = letterColors[char]
					dot = [char, pos, c]
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
		# ToDo: get this working correctly
		imgSize[0] = 10000 #int(self.minmax[2]) + self.dx + 2*(self.rMax + self.buff) 
		imgSize[1] = 10000 #int(self.minmax[3]) + self.dy + 2*(self.rMax + self.buff)	
		return imgSize


	def drawDots(self, draw, dots, r):
		for dot in dots:
			x1 = dot[1][0] - r
			y1 = dot[1][1] - r
			x2 = x1 + r
			y2 = y1 + r
			c = dot[2]
			char = dot[0]

			c[3] = 60
			dx = 0 
			dy = 0 

			#draw.ellipse((x-r + dx, y-r + dy, x+r + dx, y+r + dy), fill=tuple(c))
			draw.ellipse((x1, y1, x2, y2), fill=tuple(c))
			list(c)




artist = selfDrawingCode()

