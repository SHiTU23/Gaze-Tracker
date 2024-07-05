####################################################################
## In this project, all objects that are looked at will be shown by
## drawing a rectangle arounf it
## default path for saving recordings => C:\Users\ASUS\recordings
## changed the path to this => E:\SHiTU\programming\projects\gazeTracker\Gaze-Tracker\src\gaze_tracker\world_camera_capture\world_video_capture
####################################################################
###   Author: https://github.com/SHiTU23                         ###
#################################################################### 

import os
import sys
import pygame
import numpy as np
import cv2

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from gaze_tracker.world_view import capture_world

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

### worldCamera_Fps is set in Pupil Core software
world = capture_world(worldCamera_Fps=30)
capture_length = 1 ## second **min of 0.7**
world.capture(capture_length)
world_image_path = world.save_frame()

world_image = pygame.image.load(world_image_path).convert()

world_image_width = world_image.get_width()
world_image_height = world_image.get_height()
print(f"w:{world_image_width}, h:{world_image_height}")

gaze_on_object = world.gaze_pose_onWorld() ###[x,y]
[x, y] = gaze_on_object

x = int(np.interp(x, [0, 1], [0, world_image_width]) )
y =int(abs(world_image_height - (np.interp(y, [0,1], [0, world_image_height]))))
print(f"gaze: {gaze_on_object}, mapped_x: {x}, y:{y}")

center_coordinates = (x, y)
radius = 10
color = (0, 0, 255)  # Green color in BGR
thickness = 20
img = cv2.imread(world_image_path)
cv2.circle(img, center_coordinates, radius, color, thickness)
cv2.imwrite('./detected_image.jpg', img)





'''
running = True
while running:
    screen.blit(world_image, (0, 0))
    pygame.display.update()
    pygame.display.flip()

    pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)
    pygame.display.update()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
            running = False
pygame.quit()
'''