# -*- coding: utf-8 -*-
"""imageFallspeed

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12IfFvffYZqhVQpsQxykbUKRM9dCeAB4E

#Calculate the fall speed from a series of images
Written to find the fallspeed from series of 7 images taken from video of fall speed test rig where 15cm = 780pixels

#Setup
"""

import cv2
from google.colab.patches import cv2_imshow
import os

!mkdir C0001Frames
!mkdir C0004Frames
!mkdir C0007Frames
!mkdir C0008Frames

!mv /content/*.png C0008Frames

cap = cv2.VideoCapture("C0001.mp4")
output = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'MPEG'), 240, (1920, 1080))

def videoToFrames(videoPath, outputFolder="/content"):
  capture = cv2.VideoCapture(videoPath)
  output = cv2.VideoWriter(outputFolder,cv2.VideoWriter_fourcc(*’MP4’),240,(1920,1080))
  capture = cv2.VideoCapture(videoPath)

  frameNum = 0
  while(True):
    success, frame = capture.read()
    if success:
      path = outputFolder + "//000" + str(frameNum) + ".png"
      cv2.imwrite(path, frame)
    else:
      break
    frameNum += 1
  capture.release()

videoToFrames("/content/C0001.MP4", "/content/C0001Frames")
videoToFrames("/content/C000.MP4", "/content/C0001Frames")
videoToFrames("/content/C0001.MP4", "/content/C0001Frames")
videoToFrames("/content/C0001.MP4", "/content/C0001Frames")

"""#Locate the "snowflake""""

def widestRow(arr):
  width = 0
  widestRow = 0
  flag = False
  cnt = 0
  for i in range(0, len(arr)):
    for j in range(0, len(arr[i])):
      if(arr[i][j] >= 1):
        flag = True
        cnt += 1
      else:
        if(flag):
          if(cnt > width):
            widestRow = i
            width = cnt
        flag = False
        cnt = 0
  return widestRow

def getFlakeY(filename):
  #Load the image
  img = cv2.imread(filename, 0)

  #Get rid of the bottom of the image (lots of glare and we don't need it)
  for i in range(950, len(img)):
    for j in range(0, len(img[i])):
      img[i][j] = 0

  #Get rid of the sides of the image (lots of glare and we don't need it)
  for i in range(0, len(img)):
    for j in range(280, len(img[i])):
      img[i][j] = 0
  for i in range(0, len(img)):
    for j in range(0, 20):
      img[i][j] = 0

  ret,img2 = cv2.threshold(img,25,40,cv2.THRESH_BINARY)
  return widestRow(img2)

"""#Distance between flake across images"""

def getLocations(directory):
  dir_list = os.listdir(directory)
  locations = [0]*len(dir_list)
  for file in dir_list:
    locations[int(file[5])-1] = getFlakeY(directory + "//" + file)
  return locations

def getDistancesP(locations):
  distances = [0]*(len(locations)-1)
  for i in range(0, len(distances)):
    distances[i] = locations[i+1] - locations[i]
  return distances

def getDistancesC(distancesP, pixelSize=0.01923):
  distances = [0.0] * len(distancesP)
  for i in range(0, len(distances)):
    distances[i] = distancesP[i] * pixelSize
  return distances

def getSpeedsMS(distancesC, time=0.10):
  speeds = [0.0] * len(distancesC)
  for i in range(0, len(speeds)):
    speeds[i] = (distancesC[i] / 100) * (1/time)
  return speeds

def average(speeds):
  sum = 0
  for i in speeds:
    sum += i
  return (sum / len(speeds))

"""#Do the thing"""

def details(directory):
  locations = getLocations(directory)
  print("Location of flake (pixels): " + str(locations))
  distancesP = getDistancesP(locations)
  print("Pixel distances between flakes: " + str(distancesP))
  distancesC = getDistancesC(distancesP)
  print("cm distances between flakes: " + str(distancesC))
  speeds = getSpeedsMS(distancesC)
  print("Speeds (m/s): " + str(speeds))
  averageSpeed = average(speeds)
  print("Average speed of snowflake: " + str(averageSpeed) + " m/s")
  speedFt = averageSpeed * 3.28084
  print("Average speed of snowflake: " + str(speedFt) + " ft/s")
  adjustedSpeed = speedFt * (260/60)
  print("Speed adjusted by a factor of (240/60): " + str(adjustedSpeed) + " ft/s")

details("/content/C0001Frames")

details("/content/C0004Frames")

details("/content/C0007Frames")

details("/content/C0008Frames")
