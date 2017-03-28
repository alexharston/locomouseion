import cv2
import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np 
import os
import matplotlib.pyplot as plt 

def frame_diff(prev_frame, cur_frame, next_frame):
	diff_frames1 = cv2.absdiff(next_frame, cur_frame)
	
	diff_frames2 = cv2.absdiff(cur_frame, prev_frame)
	
	return cv2.bitwise_and(diff_frames1, diff_frames2)

def get_frame(cap):
	ret, frame = cap.read()
	if ret == True:
		scaling_factor = 1
		frame = cv2.resize(frame, None, fx = scaling_factor, fy = scaling_factor, interpolation = cv2.INTER_AREA)
		return cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

def main():

	root = tk.Tk()
	root.withdraw()

	MIList = []
	VideoFlag = []
	count = 1
	selectedvideo = askopenfilename()
	cap = cv2.VideoCapture(selectedvideo)
	length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
	intlength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	currentframenumber = cap.get(cv2.CAP_PROP_POS_FRAMES)
	intcurrentframenumber = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
	scaling_factor = 1
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter((selectedvideo + 'motionindexed.avi'),fourcc, 60.0, (640,478), isColor=False)
	with open((selectedvideo + 'threshold' + '.txt'), 'r') as readthreshold:
		threshold = float(readthreshold.readline())
	
	prev_frame = get_frame(cap)
	cur_frame = get_frame(cap)
	next_frame = get_frame(cap)

	while (cap.isOpened()):

		try:
			cv2.imshow("Object Movement", frame_diff(prev_frame, cur_frame, next_frame))
			prev_frame = cur_frame
			cur_frame = next_frame
			next_frame = get_frame(cap)
			differencesquared = (next_frame-cur_frame)**2
			interframedifference = np.sum(differencesquared)
			MIList.append(interframedifference)
			print(interframedifference)
			if interframedifference >= threshold:
				out.write(cur_frame)
				VideoFlag.append((str(count) + ' ' + '|' + ' ' + '1' + '\n' ))
				
			
			elif interframedifference < threshold:
			 	VideoFlag.append((str(count) + ' ' + '|' + ' ' + '0' + ' \n'))
			
			count = count + 1

			key = cv2.waitKey(1)
			if key == ord('q'):
				break
		except:
			break

	with open((selectedvideo + 'flag' + '.txt'), 'w') as f:
		for item in VideoFlag:
			f.write((str(item) + '\n'))
		print(VideoFlag)


	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
    # this is called if this code was not imported ... ie it was directly run
    # if this is called, that means there is no GUI already running, so we need to create a root
    root = tk.Tk()
    root.withdraw()
    main()
