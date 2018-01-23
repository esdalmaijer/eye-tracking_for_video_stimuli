Example experiment: Eye tracking with video stimuli
===================================================

Version: 1 (23-Jan-2018)

Author: Edwin Dalmaijer


ABOUT
-----

Sometimes you want to present videos while tracking people's eye movements. This is an example of an experiment script that can do that. It's programmed in Python, using the PyGaze toolbox, and OpenCV.

DEPENDENCIES
------------
For this to work, you need to have a working installation of Python, including several external packages. These include NumPy, PyGame, and PyGaze. Instead of PyGame, you can also choose PsychoPy, which requires further external packages. In addition, you need a working installation of OpenCV (tested on version 2.4.10).


IMPORTANT
---------

The RUNME.bat file needs to be changed to point to your own Python installation. In the example, the installed distribution is Anaconda, installed in `C:\Anaconda`. If you have a different version, simply find out where your `python.exe` is. This will usually be in `C:\Python27\python.exe` or someplace similar.


DOWNLOAD
--------

1) Go to: [https://github.com/esdalmaijer/eye-tracking_for_video_stimuli](https://github.com/esdalmaijer/eye-tracking_for_video_stimuli)

2) Click 'clone or download', and then 'download ZIP'. Or click this [direct link](https://github.com/esdalmaijer/eye-tracking_for_video_stimuli/archive/master.zip).

3) Extract the ZIP archive you just downloaded.

4) Copy the folder `experiment` to where you want it to be.


HOW TO RUN
----------

On Windows, change the code in RUNME.bat to your own Python installation, and then double-click it.

On Linux and OS X, open a terminal, make sure you're in the `experiment` directory, and run `python experiment.py`.
