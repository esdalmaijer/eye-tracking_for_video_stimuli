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
# - constants.py (this file)
# - experiment.py
# - videos
#   - documentary_coral_reef_adventure_1280x720.mp4
#   - sport_surfing_in_thurso_900x720.mp4
#   - sport_wimbledon_federer_final_1280x704.mp4
#
# Video credit: https://thediemproject.wordpress.com/

import os
import time


# DISPLAY SETTINGS
# The DISPTYPE determines what library will be used for the presentation of
# visual stimuli and for collecting user input. You can choose between
# PsychoPy ('psychopy') or PyGame ('pygame')
DISPTYPE = 'pygame'
# The DISPSIZE is the resolution of the monitor you run this experiment on.
# Make sure the DISPSIZE matches the resolution!
DISPSIZE = (1920, 1080)

# EYE TRACKING SETTINGS
# You can use the TRACKERTYPE constant to indicate what type of eye tracker
# you are using. The following option are currently (Jan 2018) supported:
#    'eyelink'      For SR Research EyeLink trackers, e.g. the EyeLink II and
#                   EyeLink 1000.
#   'eyetribe'      For the EyeTribe tracker.
#   'opengaze'      For trackers that support GazePoint's OpenGaze API, such as
#                   the GP3 and GP3 HD.
#   'smi'           For eye trackers made by SensoMotoric Instruments, such as
#                   the RED-m.
#   'tobii'         For eye trackers made by Tobii that support the new Tobii
#                   Pro SDK.
#   'tobii-legacy'  This is also for eye trackers made by Tobii, but uses the
#                   old Tobii SDK; useful for older models or for if you don't
#                   want to use the new Pro SDK.
TRACKERTYPE = 'eyelink'
# The DUMMYMODE constant can be used to set the eye tracker in DUMMYMODE,
# which will allow you to test your experiment without having an eye tracker
# attached. The mouse cursor will become visible between calls to
# start_recording and stop_recording, so you can simulate gaze interaction.
# Make sure to set DUMMYMODE to False if you actually want to run the
# experiment with eye tracking!
DUMMYMODE = True

# FILES AND FOLDERS
# This is where you can define paths to your stimuli and output files. The
# first thing to do, is detect the path to the directory that holds this file.
DIR = os.path.dirname(os.path.abspath(__file__))
# Now you can construct the name to the video directory, VIDDIR.
VIDDIR = os.path.join(DIR, 'videos')
# The safest thing to do before attempting to load videos, is to check whether
# the video directory actually exists where we expect it to be.
if not os.path.isdir(VIDDIR):
    # If it turns out that the video directory doesn't exist, you would
    # ideally notify the person who is running the experiment, so they can
    # fix the issue.
    raise Exception("ERROR: Video directory not found at '%s'" % (VIDDIR))
# Automatically detect all files in the video directory.
VIDEOS = os.listdir(VIDDIR)
# Sort the list of videos alphabetically.
VIDEOS.sort()

# You should also construct the path to the data directory, DATADIR.
DATADIR = os.path.join(DIR, 'data')
# Before writing anything to the data directory, you should check whether it
# exists. If it doesn't, this might be the first time this experiment is run,
# so you should create a new directory for the data.
if not os.path.isdir(DATADIR):
    print("MSG: Creating new directory for data files at '%s'" % DATADIR)
    os.mkdir(DATADIR)

# The data file will simply be the current data and time in a format that can
# easily be sorted: 'YYYY-MM-DD_hh-mm-ss'. The LOGFILENAME is the name of the
# log file, without any information about its path.
LOGFILENAME = time.strftime("%y-%m-%d_%H-%M-%S")
# Unfortunately, EyeLink does not allow names of more than 8 characters, so
# you should shorten the name on that platform. For example, to the day, hour,
# and minute info: 'DD_hh-mm'.
if TRACKERTYPE == 'eyelink':
    LOGFILENAME = time.strftime("%d_%H-%M")
# The LOGFILE constant is the path to the log file.
LOGFILE = os.path.join(DATADIR, LOGFILENAME)

# Before starting the experiment and potentially overwriting an existing file,
# you probably want to check whether the intended log file already exists.
if os.path.isfile(LOGFILE + '.txt'):
    # Throw an error to stop the file from being overwritten.
    raise Exception("ERROR: File '%s' already exists. Delete it before restarting." % \
        (LOGFILENAME))
