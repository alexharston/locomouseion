#MotionIndexPythonPort

A small program to allow video tagging of rodent locomotion data and autoremoval of subthreshold video.

This program utilises OpenCV to compare pairwise frames and sum the pixel intensity matrices to produce a motion index value. This is then smoothed and a threshold produced to autoremove periods of non-motion from the video. 

Upon completion, videos are tagged by a user frame by frame, for future analysis.
