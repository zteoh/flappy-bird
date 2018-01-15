from tkinter import *
import random
import math

def init(data):
	data.isGameOver = False
	data.mx, data.my = 0,0
	data.bird = Bird(data)
	data.obstacle = Obstacle(data)
	data.totalTime = 0
	data.mode = "splashScreen"

##############################################################################
# classyClasses
##############################################################################

class Bird(object):
	def __init__ (self, data):
		self.x = data.width//3
		self.y = data.height//2
		self.r = data.height//20
		self.color = "gold"
		self.vy = 0
		self.gravity = 3

	def getRadius(self):
		return self.r

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def changeSpeed(self, newVy):
		self.vy = newVy

	def moveBird(self):
		#get the velocity (speed with direction)
		self.vy += self.gravity
		#get displacement (distance with direction)
		self.y += self.vy

	def drawBird(canvas, self):
		beakAngle = math.pi/6
		#getting the points of the beak
		x1 = self.x + math.cos(beakAngle) * self.r
		y1 = self.y - math.sin(beakAngle) * self.r
		x2 = self.x + math.cos(beakAngle) * self.r
		y2 = self.y + math.sin(beakAngle) * self.r
		x3 = self.x + 1.5 * self.r
		y3 = self.y
		#draw beak
		canvas.create_polygon(x1,y1,x2,y2,x3,y3, fill="orange")
		#draw body
		canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, 
			self.y + self.r, fill = self.color, width = 0)
		#draw eye
		canvas.create_oval(x1-10, y1+7.5, x1-5, y1+2.5, fill="black")
		pass

class Obstacle(object):
	def __init__ (self, data):
		self.obColor = "olive drab"
		self.obs = []
		self.obWidth = Bird.getRadius(data.bird) * 4
		self.gapSize = Bird.getRadius(data.bird) * 5
		self.obFreq = 4000
		self.totalTime = 0

	def getObFreq(self):
		return self.obFreq

	def moveOb(self):
		pass

	def addObstacle(self, data):
		x = data.width
		y = random.randrange(self.gapSize, data.height-self.gapSize)
		if (data.totalTime % self.obFreq == 0):
			self.obs.append([x,y])

	def removeObstacle(self, data):
		for ob in self.obs:
			ob[0] -= 30
			if ob[0] <= 0:
				self.obs.remove(ob)

	def drawOb(canvas, self, data):
		for obs in self.obs:
			x = obs[0]
			y = obs[1]
			canvas.create_rectangle(x- self.obWidth//2, 0, x + self.obWidth//2,
				y - self.gapSize//2, fill= self.obColor, width = 0)
			canvas.create_rectangle(x- self.obWidth//2, y+ self.gapSize//2, 
				x + self.obWidth//2, y + data.height, fill= 
				self.obColor, width = 0)

	def isColliding(self, data):
		birdTop, birdButt = Bird.getY(data.bird) - Bird.getRadius(data.bird),\
		 Bird.getY(data.bird) + Bird.getRadius(data.bird)
		birdLeft, birdRight = Bird.getX(data.bird) - Bird.getRadius(data.bird),\
		 Bird.getX(data.bird) + Bird.getRadius(data.bird)

		#access each individual pipe which is kept in a list
		for ob in self.obs:
			obX = ob[0]
			obY = ob[1]

			topObLeft, topObRight = obX- self.obWidth//2, obX + self.obWidth//2
			topObTop, topObBottom = 0, obY - self.gapSize//2

			bottomObTop = obY + self.gapSize//2

			#checks whether the bird is touching the pipes
			if (birdTop <= topObBottom and topObLeft <= birdRight 
				and birdLeft <= topObRight) or (birdButt >= bottomObTop 
				and topObLeft <= birdRight and birdLeft <= topObRight):
				data.isGameOver = True

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
	if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
	elif (data.mode == "playGame"):   playGameMousePressed(event, data)
	elif (data.mode == "help"):       helpMousePressed(event, data)

def keyPressed(event, data):
	if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
	elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
	elif (data.mode == "help"):       helpKeyPressed(event, data)

def timerFired(data):
	if (data.mode == "splashScreen"): splashScreenTimerFired(data)
	elif (data.mode == "playGame"):   playGameTimerFired(data)
	elif (data.mode == "help"):       helpTimerFired(data)

def redrawAll(canvas, data):
	canvas.create_rectangle(0,0,data.width, data.height, fill= "skyblue1")
	if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
	elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
	elif (data.mode == "help"):       helpRedrawAll(canvas, data)


##############################################################################
# splashScreen mode
##############################################################################

def splashScreenMousePressed(event, data):
	pass

def splashScreenKeyPressed(event, data):
	data.mode = "playGame"

def splashScreenTimerFired(data):
	pass

def splashScreenRedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2-20,
					   text="F L A P P Y    B U R D", font="Arial 26 bold")
	canvas.create_text(data.width/2, data.height/2+20,
					   text="Press any key to play!", font="Arial 20")

##############################################################################
# playGame mode
##############################################################################

def playGameMousePressed(event, data):
	pass

def playGameKeyPressed(event, data):
	if (event.keysym == 'h'):
		data.mode = "help"
	elif  event.char == "r":
		init(data)
	elif event.char == " ":
		Bird.changeSpeed(data.bird, -20)

def playGameTimerFired(data):
	if not data.isGameOver:
		Bird.moveBird(data.bird)
		data.totalTime += 2 * data.timerDelay
		Obstacle.addObstacle(data.obstacle, data)
		Obstacle.removeObstacle(data.  obstacle, data)
		Obstacle.isColliding(data.obstacle, data)
	pass

def playGameRedrawAll (canvas, data):
	Bird.drawBird(canvas, data.bird)
	Obstacle.drawOb(canvas, data.obstacle, data)
	canvas.create_text(data.width/2, data.height/15,
					   text="Press 'h' for help!", font="Arial 20")
	if data.isGameOver:
		canvas.create_text(data.width//2, data.height//2, anchor= S, 
			text="G A M E    O V E R!", font="Helvetica 64 bold")
		canvas.create_text(data.width/2, data.height/2, anchor= N,
						   text="Press 'r' to RESET!", font="Arial 20")


##############################################################################
# help mode
##############################################################################

def helpMousePressed(event, data):
	pass

def helpKeyPressed(event, data):
	data.mode = "playGame"

def helpTimerFired(data):
	pass

def helpRedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2-40,
					   text="I see you need H E L P", font="Arial 26 bold")
	canvas.create_text(data.width/2, data.height/2-10,
					   text="Objective: DONT TOUCH THE GREEN PIPES", 
					   font="Arial 20")
	canvas.create_text(data.width/2, data.height/2+15,
					   text="Press spacebar to F L Y!", font="Arial 20")
	canvas.create_text(data.width/2, data.height/2+40,
					   text="Being a lazybum will make you F A L L", 
					   font="Arial 20")

##############################################################################
# use the run function as-is
##############################################################################

def run(width=600, height=600):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()    

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100 # milliseconds
	init(data)
	# create the root and the canvas
	root = Tk()
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("thanks for playing!!")

run()