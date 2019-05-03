from tkinter import Tk, Canvas, Frame, BOTH
import tkinter as tk
from model import Simulator


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Calender")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        simulator = Simulator()
        calender = simulator.calender
        steps = {}
        canvas.create_line(20, 200, 970, 200)

        i = 20
        step = -0.1
        while i <= 970:
            step +=0.1
            checker = step/0.5
            if step >= 1:
                    if round(checker,2) % int(checker) == 0: # draw step only if it's one step or half step
                        canvas.create_line(i,205,i,195)
            if step == 0.0 or step == 0.5:
                canvas.create_line(i,205,i,195)
            steps[round(step,1)] = [i,205,195]
            i += 15.5

        for i,c in enumerate(calender):
                current_event_date = calender[i]['date']
                if i+1 < len(calender):
                    next_event_date = calender[i+1]['date']
                    state_x_position = (steps[current_event_date][0] + steps[next_event_date][0])/2
                else:
                    state_x_position = (steps[current_event_date][0] + 35)
                state_y_position = 185
                canvas.create_text(state_x_position, state_y_position, text = 'state = ' + str(c['next_state']), font='Helvetica 9 bold')
                if c['event'] is not None :
                    canvas.create_line(steps[current_event_date][0],190,steps[current_event_date][0],160, arrow = tk.FIRST)
                    canvas.create_text(steps[current_event_date][0],150, text= 'event ' + str(i) +" = " + str(c['event']), font='Helvetica 9 bold')
                    canvas.create_text(steps[current_event_date][0],215, text = str(current_event_date), font ='Helvetica 9 bold')
                    canvas.create_line(steps[current_event_date][0],205,steps[current_event_date][0],195)
        y = 360
        for state in simulator.gamma:
            canvas.create_text(50,y, text = "\u0393" + "(" +str(state)+ ") = "+"{"+str(simulator.gamma[state]).replace('[','').replace(']','')+"}",
                               font = 'Helvetica 10 bold' )
            y += 18
        y +=18
        canvas.create_text(90, y, text= "E (set of events) = "+ str(simulator.user_input.events).replace('[','').replace(']',''),
                           font = 'Helvetica 10 bold')
        y +=18
        canvas.create_text(90, y, text= "X (set of states) = " + str(simulator.user_input.states).replace('[','').replace(']',''),
                           font = 'Helvetica 10 bold')

        canvas.pack(fill=BOTH, expand=1)


def main():

    root = Tk()
    ex = Example()
    root.geometry("1000x600")
    root.mainloop()


if __name__ == '__main__':

    main()