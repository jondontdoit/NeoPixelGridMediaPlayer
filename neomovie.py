#!/usr/bin/python
# -*- coding:utf-8 -*-

# *************************
# ** Before running this **
# ** code ensure you've  **
# ** set up CircuitPy    **
# ** and connected Neo   **
# ** Pixels to D18       **
# *************************

import os, time, random, subprocess
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
RENDERS_FOLDER = "renders/"


##############################################
# SETUP
##############################################
pixels = neopixel.NeoPixel(board.D18, NEO_NUM_PIXELS, brightness=NEO_BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)

# Ensure this is the correct path to your folders
rnddir = os.path.join(os.path.dirname(os.path.realpath(__file__)), RENDERS_FOLDER)

# Arguments
parser = argparse.ArgumentParser(description='NeoMovie Settings')
parser.add_argument('-r', '--render', type=str, default='$',
    help="Select a file to render")
parser.add_argument('-p', '--play', type=str, default='$',
    help="Select a folder name to play from the renders folder")
parser.add_argument('-d', '--delay', type=float, default=0.0, 
  help="Delay between screen updates, in seconds")
parser.add_argument('-i', '--inc', type=int, default=1, 
  help="Number of frames skipped between screen updates")
parser.add_argument('-s', '--start', type=int, default=0, 
  help="Start at a specific frame")
args = parser.parse_args()

frameDelay = float(args.delay)
print("Frame Delay = %f seconds" %frameDelay )

increment = int(args.inc)
print("Increment = %d frames" %increment )

startFrame = int(args.start)
print("Start at Frame = %d" %startFrame )

currentVideo = ""

# First, let's see if it's a render command
if args.render and args.render != '$':
  rndfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.render)
  
  # Check if the file exists
  if not os.path.isfile(rndfile):
    print("No video file to render! Quitting.")
    exit()
  
  # Assuming it's a good file format, move ahead to rendering
  filename = os.path.basename(rndfile)
  print("Rendering %s" %filename)
  foldname = filename[0:filename.rfind(".")]
  print("Making folder: %s" %foldname)
  subprocess.run("mkdir "+rnddir+foldname, stdout=subprocess.PIPE, shell=True)
  ffmpegcmd = "ffmpeg -i "+rndfile+"  -vf \"scale="+str(NEO_WIDTH)+":"+str(NEO_HEIGHT)+":force_original_aspect_ratio=1,pad="+str(NEO_WIDTH)+":"+str(NEO_HEIGHT)+":(ow-iw)/2:(oh-ih)/2\" "+rnddir+foldname+"/%d.bmp"
  print("Command: %s" %ffmpegcmd)
  subprocess.run(ffmpegcmd, stdout=subprocess.PIPE, shell=True)
  currentVideo = foldname
  print("%s was successfully rendered! Now let's play it" %currentVideo)
  
# Next, we'll check if it's a play command with a folder name
if currentVideo == "" and args.play and args.play != '$':  
  # Check if the file exists
  if not os.path.isdir(rnddir + args.play):
    print("Render not found!")
    exit()
  
  # Assuming it's a good render folder, move ahead to playing
  currentVideo = args.play
  
# If no file or render has been picked, play random files
playRandom = False
if currentVideo == "":
  playRandom = True
  renderList = next(os.walk(rnddir))[1]
  
  if not renderList:
    print("No renders available to play. Render something!")
    exit()
  
  currentVideo = random.choice(renderList)
  print("Playing RANDOM")


##############################################
# LOOP
##############################################
while True: 
  print("Playing %s..." %currentVideo)

  # Get number of frames
  frmdir = rnddir + currentVideo
  frameCount = len([f for f in os.listdir(frmdir)if os.path.isfile(os.path.join(frmdir, f))])
  print("Frame count: %d" %frameCount)

  # Set start position
  currentPosition = startFrame

  for frame in range(currentPosition, frameCount, increment):
    
    # Open frame in PIL  
    pilFrame = Image.open(frmdir+"/"+str(frame+1)+'.bmp')

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
    
    #print('Diplaying frame %d of %d' %(frame,frameCount))

    # Delay between frames
    time.sleep(frameDelay)
  
  # If it's play random mode, pick a new file to play
  if playRandom:
    currentVideo = random.choice(renderList)

exit()