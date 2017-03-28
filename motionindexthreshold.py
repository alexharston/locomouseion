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


def moving_average(MIList, n=30):
    ret = np.cumsum(MIList, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def main():

	MIList =[]
	root = tk.Tk()
	root.withdraw()
	selectedvideo = askopenfilename()
	cap = cv2.VideoCapture(selectedvideo)
	length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
	intlength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	currentframenumber = cap.get(cv2.CAP_PROP_POS_FRAMES)
	intcurrentframenumber = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
	scaling_factor = 1
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
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
			# print(differencesquared)
			interframedifference = np.sum(differencesquared)
			MIList.append(interframedifference)
			print(interframedifference)
			key = cv2.waitKey(1)
			if key == ord('q'):
				break
		except:
			break


	print(MIList)
	plt.plot(MIList)
	plt.ylabel('Motion Index')
	
	MIaverage = moving_average(MIList)
	plt.plot(MIaverage)

	print("click to input first point and again to list second point")
	startinput = plt.ginput(2)
	print("clicked", startinput)
	startinputxs = [x[0] for x in startinput]
	print(startinputxs)
	x1 = startinputxs[0]
	print(x1)
	x2 = startinputxs[1]
	print(x2)
	subMIList = (MIaverage[int(x1):int(x2)])
	print(subMIList)
	plt.plot(subMIList)
	arr = np.array(MIaverage)
	newthreshold = (np.mean(subMIList) + (np.std(subMIList) * 3))
	plt.axhline(y=newthreshold)
	print(newthreshold)
	with open((selectedvideo + 'threshold' + '.txt'), 'w') as f:
		f.write(str(newthreshold))
	plt.show()


	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
    # this is called if this code was not imported ... ie it was directly run
    # if this is called, that means there is no GUI already running, so we need to create a root
    root = tk.Tk()
    root.withdraw()
    main()
