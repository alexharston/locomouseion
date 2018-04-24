import cv2
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt

def main():
    framevalues = []
    referenceframe =[]
    count = 1
    selectedvideo = askopenfilename()
    cap = cv2.VideoCapture(selectedvideo)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    currentframenumber = cap.get(cv2.CAP_PROP_POS_FRAMES)
    intcurrentframenumber = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    while (cap.isOpened()): 
        ret, frame = cap.read()

        # check if read frame was successful
        if ret == False:
                break
        # show frame first
        cv2.imshow('frame',frame)

        # then waitKey
        frameclick = cv2.waitKey(0) & 0xFF

        if frameclick == ord('a'):
            swingTag(cap, framevalues, length)

        elif frameclick == ord('r'):
            rewindFrames(cap, framevalues, length)

        elif frameclick == ord('s'):
            stanceTag(cap, framevalues, length)

        elif frameclick == ord('d'):
            unsureTag(cap, framevalues, length)

        elif frameclick == ord('q'):
            saveValues(selectedvideo, framevalues)
            saveFinalValues(selectedvideo)
            
            break

        else:
            pass

    saveValues(selectedvideo, framevalues)
    saveFinalValues(selectedvideo)


    cap.release()
    cv2.destroyAllWindows()

def saveFinalValues(selectedvideo):
    with open((selectedvideo.split('.')[0].split(os.sep)[-1] + ' flag.txt')) as aob, \
         open((selectedvideo.split('.')[0].split(os.sep)[-1] + '.txt')) as xyz, \
         open((selectedvideo.split('.')[0].split(os.sep)[-1] + ' outputfile.txt'), 'w') as outputfile:
        for line in aob:
            if line.startswith("above"):
                ab, c = line.split(" | ")
                d, _ = next(xyz, "UNKNOWN | 0").split(" | ")
                outputfile.write(" | ".join((d, c)))
            elif line.startswith("below"):
                outputfile.write(line)
                    
def saveValues(selectedvideo, framevalues):
    with open((selectedvideo.split('.')[0].split(os.sep)[-1] + '.txt'), 'w') as textfile:
                for item in framevalues:
                    textfile.write("{}\n".format(item))

def stanceTag(cap, framevalues, length):   
    framevalues.append('x' + ' ' + '|' + ' ' + str(int(cap.get(1))))  
    #print(framevalues)
    print (str(int(cap.get(1))), '/', length)

def swingTag(cap, framevalues, length):
    framevalues.append('y' + ' ' + '|' + ' ' + str(int(cap.get(1))))
    #print(framevalues) 
    print (str(int(cap.get(1))), '/', length)
    

def unsureTag(cap, framevalues, length):
    framevalues.append('z' + ' ' + '|' + ' ' + str(int(cap.get(1))))
    #print(framevalues)
    print (str(int(cap.get(1))), '/', length) 
    

def rewindFrames(cap, framevalues, length): 
    cap.set(1,((int(cap.get(1)) - 2)))
    framevalues.pop()
    print(framevalues) 
    print (int(cap.get(1)), '/', length) 
   
    

if __name__ == '__main__':
    # this is called if this code was not imported ... ie it was directly run
    # if this is called, that means there is no GUI already running, so we need to create a root
    root = tk.Tk()
    root.withdraw()
    main()
