#!/usr/bin/python
# -*- coding:utf-8 -*-

# *************************
# ** Before running this **
# ** code ensure you've  **
# ** set up CircuitPy    **
# ** and connected Neo   **
# ** Pixels to D18       **
# *************************

import os, time, random
from PIL import Image
import argparse
import board
import neopixel


##############################################
# GLOBAL SETTINGS
##############################################
NEO_NUM_PIXELS =     28*28
NEO_WIDTH =             28
NEO_HEIGHT =            28
NEO_BRIGHTNESS =       0.2
ZIGZAG =              True
IMAGES_FOLDER =  "images/"


##############################################
# SETUP
##############################################
pixels = neopixel.NeoPixel(board.D18, NEO_NUM_PIXELS, brightness=NEO_BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)

# Ensure this is the correct path to your folders
imgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), IMAGES_FOLDER)

# Arguments
parser = argparse.ArgumentParser(description='NeoImage Settings')
parser.add_argument('-p', '--play', type=str, default='$',
    help="Select a file name to play from the images folder")
parser.add_argument('-d', '--delay', type=float, default=3.0, 
  help="Delay between screen updates, in seconds")
args = parser.parse_args()

frameDelay = float(args.delay)
print("Refresh Delay = %f seconds" %frameDelay )

currentImage = ""

# First, we'll check if it's a play command with a folder name
if currentImage == "" and args.play and args.play != '$':  
  imgfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.play)
  # Check if the file exists
  if not os.path.isfile(imgfile):
    print("Image not found!")
    exit()
  
  # Assuming it's a good render folder, move ahead to playing
  currentImage = imgfile
  
# If no file or render has been picked, play random files
playRandom = False
if currentImage == "":
  playRandom = True
  imageList = [f for f in os.listdir(imgdir) if os.path.isfile(os.path.join(imgdir, f))]
  
  if not imageList:
    print("No images available to display. Add some files!")
    exit()
  
  currentImage = imgdir+random.choice(imageList)
  print("Playing RANDOM")


##############################################
# LOOP
##############################################
while True: 
  print("Displaying %s..." %currentImage)

  # Open frame in PIL  
  pilFrame = Image.open(currentImage)
  
  # Perform a crude resizing if it isn't already the right size
  width, height = pilFrame.size
  if width != NEO_WIDTH or height != NEO_HEIGHT:
    pilFrame = pilFrame.resize((NEO_WIDTH, NEO_HEIGHT))

  # Display the image on the NeoPixels
  i = 0
  for x in range(0, NEO_WIDTH):
    for y in range(0, NEO_HEIGHT):
      if ZIGZAG and (x%2) == 0:
        pixels[i] = pilFrame.getpixel((x,y))
      else:
        pixels[i] = pilFrame.getpixel((x,NEO_HEIGHT-y-1))
      i += 1
  pixels.show()

  # Actually, no need to loop if just displaying a single image
  if not playRandom:
    exit()

  # Delay between frames
  time.sleep(frameDelay)

  currentImage = imgdir+random.choice(imageList)

exit()