import tkinter
import motionindexthreshold
import motionindexgenerator
import stepthroughupdated

def main():
    top=tkinter.Tk()
    top.geometry("300x350")
    top.config(background='black')
    top.title('Locomouseion')
    top.resizable(height=False, width=False)

    

    M = tkinter.Message(top, text='Locomouseion v1.1', width=280, background='black', foreground='white', font=('Courier', 28))
    B = tkinter.Button(top,text="Define Motion Index Threshold",command=motionindexthreshold.main)
    C = tkinter.Button(top,text="Autoremove Nonmovement Video Segments",command=motionindexgenerator.main)
    D = tkinter.Button(top,text="Tag Video Frames",command=stepthroughupdated.main)
    E = tkinter.Button(top,text="Quit", command=top.destroy)
   

    B.config(height=5, width=80, background='red')
    C.config(height=5, width=80, background='blue', foreground='white')
    D.config(height=5, width=80, background='yellow')
    E.config(height=5, width=80, background='green')

    M.pack()
    B.pack()
    C.pack()
    D.pack()
    E.pack()
    top.mainloop()

if __name__ == '__main__':
    main()
