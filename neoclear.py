#!/usr/bin/python
# -*- coding:utf-8 -*-

# *************************
# ** Before running this **
# ** code ensure you've  **
# ** set up CircuitPy    **
# ** and connected Neo   **
# ** Pixels to D18       **
# *************************
import board
import neopixel


##############################################
# GLOBAL SETTINGS
##############################################
NEO_NUM_PIXELS =     28*28
NEO_BRIGHTNESS =       0.2


##############################################
# SETUP
##############################################
pixels = neopixel.NeoPixel(board.D18, NEO_NUM_PIXELS, brightness=NEO_BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)

# Set all pixels to black, refresh, and quit

for i in range(0, NEO_NUM_PIXELS):
  pixels[i] = (0, 0, 0, 0)
  
pixels.show()

exit()