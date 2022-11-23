#Import the tkinter library
from tkinter import *

#Create an instance of tkinter frame
root = Tk()

#Set the geometry
root.geometry("650x250")

#Creating a canvas
canvas = Canvas(root, bg="white", height=200, width=200)
cordinates= 10, 10, 200, 200
arc = canvas.create_arc(cordinates, start=0, extent=320, fill="red")
canvas.pack()

#Clearing the canvas
#canvas.delete('all')