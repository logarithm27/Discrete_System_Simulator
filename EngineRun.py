from tkinter import *
import tkinter as tk

from InfiniteModel import InfiniteModel
from Model import Model


class Example(Frame):

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        self.initUI()


    def initUI(self):
        self.master.title("Calender")
        self.pack(fill=BOTH, expand=1)


        print("1- Simulate finite automaton")
        print("2- Simulate Infinite automaton")
        choice_automaton = input("option 1 or 2 : ")
        calendar = []
        choice = ""
        if int(choice_automaton) == 2:
            model = InfiniteModel()
            calendar = model.calendar
            choice = "infinite"
        elif int(choice_automaton) == 1:
            model = Model()
            calendar = model.calendar
            choice = "finite"

        scrollbar=Scrollbar(self,orient= HORIZONTAL)
        scrollbar.pack(side=BOTTOM,fill= X)
        canvas = Canvas(self, bd=0, highlightthickness=0, xscrollcommand=scrollbar.set)
        steps = {}
        steper = 15.5
        max_x = 970
        if len(calendar) > 10:
            max_x = 807000
            canvas.create_line(20, 200, max_x, 200)
            steper = 45
        else:
            canvas.create_line(20, 200, max_x, 200)
        i = 15
        step = -0.1
        while i <= max_x:
            step +=0.1
            canvas.create_line(i,205,i,195)
            if round(step,1) == 0.0 or round(step,1) == 0.5:
                canvas.create_line(i,205,i,195)
            steps[round(step,1)] = [i,205,195]
            canvas.create_text(i,215, text= str(round(step,1)), font='Helvetica 6 ')
            i += steper

        for i,c in enumerate(calendar):
                current_event_date = calendar[i]['date']
                if i+1 < len(calendar):
                    next_event_date = calendar[i+1]['date']
                    state_x_position = int((steps[current_event_date][0] + steps[next_event_date][0])/2)
                else:
                    state_x_position = (steps[current_event_date][0] + 35)
                state_y_position = 185
                canvas.create_text(state_x_position, state_y_position, text = str(c['next_state']), font='Helvetica 10 bold')
                if c['event'] is not None :
                    canvas.create_line(steps[current_event_date][0],190,steps[current_event_date][0],160, arrow = tk.FIRST)
                    canvas.create_text(steps[current_event_date][0],150, text= str(c['event']), font='Helvetica 10 bold')
                    canvas.create_text(steps[current_event_date][0],225, text = str(current_event_date), font ='Helvetica 8 bold')
                    canvas.create_line(steps[current_event_date][0],205,steps[current_event_date][0],195)
        y = 360
        if choice == "infinite":
            for event in model.debits:
                canvas.create_text(50,y, text = "N" + "(" +str(event)+ ") = "+str(model.debits[event]),
                                   font = 'Helvetica 10 bold' )
                y += 18

        canvas.pack(fill=BOTH, expand=1)
        scrollbar.config(command=canvas.xview)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        frame = Frame(canvas)
        canvas.create_window((500,500),window=frame,anchor= CENTER)
        canvas.config(scrollregion=canvas.bbox("all"))


def main():
    root = Tk()
    root.geometry("800x500")
    root.configure(background="red")
    frame = Example(root)
    frame.pack()
    root.mainloop()

if __name__ == '__main__':

    main()