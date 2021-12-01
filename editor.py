from tkinter import *
from PIL import Image, ImageTk
import glob
import os
import sys

currentPath = ""
imageBuffer = None
photoImageBuffer = None
imageSize = None
currentImageId = None
rectID = None
numExportsPerImage = 0

def readDoneImages():
	if os.path.exists("doneimages.txt"):
		f = open("doneimages.txt", "r")
		return f.readlines()
	return []

def collectTodo(path):
	l = glob.glob(f"{path}*.jpg") 
	print(f"found {len(l)} images")
	return l

startPos = None
rectID = None

def pressed(event):
	global startPos
	print(f"clicked at{event.x}/{event.y}")
	startPos = [event.x, event.y]
    	
def saveClip(x, y):    	
    	global startPos
    	global currentPath
    	global outDirectory
    	global numExportsPerImage
    	
    	minX = min(x, startPos[0])
    	minY = min(y, startPos[1])
    	maxX = max(x, startPos[0])
    	maxY = max(y, startPos[1])
    	area = (minX, minY, maxX, maxY)
    	cropped_img = imageBuffer.crop(area)
    	exportname = os.path.basename(currentPath)
    	cropped_img.save(outDirectory + f"/export-{numExportsPerImage}-" + exportname)
    	numExportsPerImage += 1
    	startPos = None

def released(event):
	print(f"released at{event.x}/{event.y}")
	global canvas
	global rectID
	saveClip(event.x, event.y)
	canvas.delete(rectID)
    
def drag(event):
	global startPos
	global rectID
	global canvas
	
	if rectID:
		canvas.delete(rectID)
	rectID = canvas.create_rectangle(startPos[0], startPos[1], event.x, event.y)
    
def key(event):
	print(f"key pressed:{event.char}")
	
	if event.char == 's':
		loadNextAndMarkAsDone()
	if event.char == 'd':
		global doneImages
		writeDoneImages(doneImages)

def writeDoneImages(doneImages):
	f = open("doneimages.txt", "a")
	f.writelines(doneImages)
	f.close()
    	
def loadNextAndMarkAsDone():
	global currentPath
	global doneImages
	global itemsToDo
	global numExportsPerImage
	
	if currentPath:
		doneImages.append(currentPath)
	currentPath = itemsToDo.pop(0)
	numExportsPerImage = 0
	showImage()

def showImage():
	global currentImageId
	global canvas
	global imageBuffer
	global photoImageBuffer
	global imageSize
	
	if currentImageId != None:
		canvas.delete(currentImageId)

	if currentPath:
		imageBuffer = Image.open(currentPath)
		photoImageBuffer = ImageTk.PhotoImage(imageBuffer)
		imageSize = imageBuffer.getbbox()
		currentImageId = canvas.create_image(imageSize[2] / 2, imageSize[3] / 2 ,image=photoImageBuffer)
		canvas.pack()

def deleteImage():
	canvas.delete(imagesprite)
    

if __name__ == "__main__":
	print(f"Arguments count: {len(sys.argv)}")
	for i, arg in enumerate(sys.argv):
		print(f"Argument {i:>6}: {arg}")        
	doneImages = readDoneImages()
	inDirectory = sys.argv[1]
	outDirectory = sys.argv[2]
	itemsToDo = collectTodo(inDirectory)

	root = Tk()
	root.geometry('1500x1000')
	canvas = Canvas(root,width=1499,height=999)
	canvas.bind("<Button-1>", pressed)
	canvas.bind("<ButtonRelease-1>", released)
	canvas.bind("<B1-Motion>", drag)
	root.bind("<Key>", key)
	canvas.pack()


	root.mainloop()
    

