# -*- coding: utf-8 -*-
#
# Version: 1
# Date: 2018-01-23
#
# Author: Edwin Dalmaijer
#
# If you use this example for a publication, please cite the following paper:
#
# Dalmaijer, E.S., Mathôt, S., & Van der Stigchel, S. (2014). PyGaze: an 
#   open-source, cross-platform toolbox for minimal-effort programming of eye
#   tracking experiments. Behavior Research Methods, 46, p. 913-921. 
#   doi:10.3758/s13428-013-0422-2
#
# This is an example eye-tracking experiment for video stimuli. It uses
# PyGaze for eye tracking, and OpenCV for loading videos. The following files
# should be included in this example:
# - constants.py
# - experiment.py (this file)
# - videos
#   - documentary_coral_reef_adventure_1280x720.mp4
#   - sport_surfing_in_thurso_900x720.mp4
#   - sport_wimbledon_federer_final_1280x704.mp4
#
# Video credit: https://thediemproject.wordpress.com/

import os
import time
import datetime
import random

from constants import *

import pygaze
from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.keyboard import Keyboard
from pygaze.eyetracker import EyeTracker
from pygaze.logfile import Logfile
import pygaze.libtime as timer

import cv2
import numpy
if DISPTYPE == 'psychopy':
    from psychopy.visual import ImageStim
elif DISPTYPE == 'pygame':
    import pygame


# # # # #
# INITIALISE

# Start a new Display instance to be able to show things on the monitor.
# The important parameters will automatically be loaded from the constants.
disp = Display()

# Initialise a Keyboard instance to detect key presses. Again, important
# parameters will be loaded from the constants.
kb = Keyboard()

# Initialise the EyeTracker and let it know which Display instance to use by
# passing it to the EyeTracker.
tracker = EyeTracker(disp)

# Create a Logfile instance that keeps track of when videos start.
log = Logfile()
# Write a header to the log file.
log.write(['date', 'time', 'trialnr', 'video', 'timestamp'])


# # # # #
# SCREENS

# Create a screen to show instructions on.
textscr = Screen()
textscr.draw_text("Press any key to start the next video.", fontsize=24)

# Create a screen to show images on. This will be the screen that we will use
# to display each video frame.
stimscr = Screen()


# # # # #
# PLAY VIDEOS

# Calibrate the eye tracker.
tracker.calibrate()

# Randomise the list of videos. Remove this line if you want the videos to be
# displayed in alphabetical order.
random.shuffle(VIDEOS)

# Run through the list of videos.
for trialnr, vidname in enumerate(VIDEOS):
    
    # Get the full path to the video.
    vidpath = os.path.join(VIDDIR, vidname)
    
    # Open a VideoCapture to be able to load the frames.
    cap = cv2.VideoCapture(vidpath)
    # Get the number of frames and the framerate from the video.
    nframes = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    framerate = float(cap.get(cv2.cv.CV_CAP_PROP_FPS))
    # Compute the frame duration in milliseconds.
    framedur = 1000.0 / framerate
    # Get the frame size.
    width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    
    # Reset the current stimscr.
    stimscr.clear()
    
    # For PsychoPy, prepare a new ImageStim.
    if DISPTYPE == 'psychopy':
        # Create a black frame, formatted as an all-zeros NumPy array.
        frame = numpy.zeros((height, width, 3), dtype=float)
        # Now create a PsychoPy ImageStim instance to draw the frame with.
        stim = ImageStim(pygaze.expdisplay, image=frame, size=(width, height))
        # When DISPTYPE='psychopy', a Screen instance's screen property is a list
        # of PsychoPy stimuli. We would like to add the ImageStim we just created
        # to that list, and record at what index in the list it was added.
        # First we get the current length of the stimscr's list of stimuli, which
        # will be the index at which the new ImageStim will be assigned to.
        stim_index = len(stimscr.screen)
        # Then we add the ImageStim to the stimscr. Every time you call
        # disp.fill(stimscr) and then disp.show(), all stimuli in stimscr
        # (including the ImageStim) will be drawn.
        stimscr.screen.append(stim)
    
    # Wait until the participant presses any key to start.
    disp.fill(textscr)
    disp.show()
    kb.get_key(keylist=None, timeout=None, flush=True)
    
    # Log the start of the trial.
    log.write([time.strftime("%y-%m-%d"), time.strftime("%H-%M-%S"), \
        trialnr, vidname, timer.get_time()])
    
    # Start eye tracking.
    tracker.start_recording()
    timer.pause(5)
    tracker.log("TRIALSTART")
    
    # Show a status message on the EyeLink.
    if TRACKERTYPE == 'eyelink':
        tracker.status_msg("Trial %d/%d (%s)" % (trialnr, len(VIDEOS), vidname))
    
    # Log trial specifics to gaze data file.
    timer.pause(5)
    tracker.log("TRIALNR %d; VIDNAME %s; EXPTIME %d; PCTIME %s" % \
        (trialnr, vidname, timer.get_time(), \
        datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
    
    # Loop until the video ends.
    for framenr in range(nframes):
        
        # Get a timestamp for the start of the loading time.
        loadstart = timer.get_time()

        # Load the next frame, and convert it to a format that PsychoPy's
        # ImageStim can actually recognise.
        if cap.isOpened():
            # Read the frame. The result is a NumPy array with a BGR format,
            # in which all values are unsigned 8-bit integers. The frame is
            # also upside-down.
            success, frame = cap.read()
            # Sometimes the returned frame is None, but the success bool is
            # somehow still True. This sets success to False if frame is None.
            if frame is None:
                success = 0
        else:
            success = 0
        
        # If the frame is successfully loaded, convert it to a format we can
        # handle with either PsychoPy or PyGame.
        if success:
            if DISPTYPE == 'psychopy':
                # Convert the frame from BGR to RGB.
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert the frame form unsigned integers between 0 and 255
                # to floats between 0 and 1.
                frame = frame / 255.0
                # Flip the frame upside-up.
                frame = numpy.flipud(frame)
            elif DISPTYPE == 'pygame':
                # Convert the frame from BGR to RGB.
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # First mirror and then rotate the frame.
                frame = numpy.fliplr(frame)
                frame = numpy.rot90(frame)
                # Make a PyGame Surface out of the NumPy array.
                frame = pygame.surfarray.make_surface(frame)

        # If loading fails, generate a black frame instead.
        if not success:
            if DISPTYPE == 'psychopy':
                frame = numpy.zeros((height, width, 3), dtype=float)
            elif DISPTYPE == 'pygame':
                frame = pygame.Surface((width,height))

        if DISPTYPE == 'psychopy':
            # Set the ImageStim's image to the loaded frame.
            stimscr.screen[stim_index].setImage(frame)
        elif DISPTYPE == 'pygame':
            # Draw the Surface (automatically detected format by draw_image).
            stimscr.draw_image(frame)

        # Present the new frame. The disp.show call will block until the start
        # of the next refresh cycle.
        disp.fill(stimscr)
        frametime = disp.show()
        pc_frametime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
        tracker.log("FRAMENR %d; TIME %.3f; PCTIME %s" % \
            (framenr, frametime, pc_frametime))

        # Compute the loading duration.
        loaddur = frametime - loadstart

        # Wait for the frame duration (corrected for the load duration, and
        # including 10 milliseconds of buffer time).
        timer.pause(int(framedur - (loaddur +5)))
    
    # Log the end of the trial.
    tracker.log("TRIALSTOP")
    
    # Clear the display (showing the background colour).
    disp.fill()
    disp.show()
    
    # Stop recording eye movements.
    tracker.stop_recording()


# # # # #
# CLOSE

# Flush the keyboard.
kb.get_key(keylist=None, timeout=1, flush=True)

# Present a message during the transferring of data (only really applicable on
# systems where the data is transferred on calling tracker.close).
textscr.clear()
textscr.draw_text("Processing data, don't press anything!", fontsize=24)
disp.fill(textscr)
disp.show()

# Close the log file.
log.close()

# Close the connection to the eye tracker.
tracker.close()

# Present a thank-you message.
textscr.clear()
textscr.draw_text("That's all, folks! Press any key to exit.", fontsize=24)
disp.fill(textscr)
disp.show()
# Wait for a key press.
kb.get_key(keylist=None, timeout=None, flush=True)

# Close the display.
disp.close()
