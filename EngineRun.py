from tkinter import Tk, Canvas, Frame, BOTH
import tkinter as tk

from InfiniteModel import InfiniteModel
from model import Model


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Calender")
        self.pack(fill=BOTH, expand=1)
        print("1- Simulate finite automaton")
        print("2- Simulate Infinite automaton")
        choice_automaton = input("option 1 or 2 : ")
        calendar = []
        model = None
        if int(choice_automaton) == 2:
            model = InfiniteModel()
            calendar = model.calendar
        elif int(choice_automaton) == 1:
            model = Model()
            calendar = model.calendar
        canvas = Canvas(self)
        steps = {}
        canvas.create_line(20, 200, 1070, 200)
        i = 20
        step = -0.1
        while i <= 80700:
            step +=0.1
            # checker = step/0.5
            # if step >= 1:
            #         if round(checker,2) % int(checker) == 0: # draw step only if it's one step or half step
            #             canvas.create_line(i,205,i,195)
            if step == 0.0 or step == 0.5:
                canvas.create_line(i,205,i,195)
            steps[round(step,1)] = [i,205,195]
            i += 5

        for i,c in enumerate(calendar):
                current_event_date = calendar[i]['date']
                if i+1 < len(calendar):
                    next_event_date = calendar[i+1]['date']
                    state_x_position = (steps[current_event_date][0] + steps[next_event_date][0])/2
                else:
                    state_x_position = (steps[current_event_date][0] + 35)
                state_y_position = 185
                canvas.create_text(state_x_position, state_y_position, text = str(c['next_state']), font='Helvetica 8 bold')
                if c['event'] is not None :
                    canvas.create_line(steps[current_event_date][0],190,steps[current_event_date][0],160, arrow = tk.FIRST)
                    canvas.create_text(steps[current_event_date][0],150, text= str(c['event']), font='Helvetica 8 bold')
                    canvas.create_text(steps[current_event_date][0],215, text = str(current_event_date), font ='Helvetica 8 bold')
                    canvas.create_line(steps[current_event_date][0],205,steps[current_event_date][0],195)
        y = 360
        for state in model.gamma:
            canvas.create_text(50,y, text = "\u0393" + "(" +str(state)+ ") = "+"{"+str(model.gamma[state]).replace('[','').replace(']','')+"}",
                               font = 'Helvetica 10 bold' )
            y += 18
        y +=18
        canvas.create_text(90, y, text= "E (set of events) = "+ str(model.events).replace('[','').replace(']',''),
                           font = 'Helvetica 10 bold')
        y +=18
        canvas.create_text(90, y, text= "X (set of states) = " + str(model.states).replace('[','').replace(']',''),
                           font = 'Helvetica 10 bold')

        canvas.pack(fill=BOTH, expand=1)


def main():

    root = Tk()
    ex = Example()
    root.geometry("1600x600")
    root.mainloop()


if __name__ == '__main__':

    main()