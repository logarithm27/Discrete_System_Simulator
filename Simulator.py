from utility import *

class Simulator:
    def __init__(self, initial_state, durations, gamma,transitions):
        self.calendar = []
        self.steps = []
        self.initial_state = initial_state
        self.durations = durations
        self.gamma = gamma
        self.transitions = transitions

    def simulate(self):
        counter = 1
        self.init_steps()
        ordered_events_by_date = {}
        initial_event_date_t_previous = 0.0
        self.calendar.append({'event': None, 'next_state': self.initial_state,
                 'clock': None, 'date': initial_event_date_t_previous})
        # if there we still have clock values on the durations list
        while still_more_clocks(self.durations):
            self.steps.append(str(counter) + " iteration :"+"\n"+"-------------"+"\n")
            # get the current state from the last added state from the calender dictionary
            current_state = self.calendar[-1]['next_state']
            # get the possible active events by passing the current state inside the gamma function
            active_events = self.gamma[current_state]
            # looping through the active events
            self.steps.append("("+str(current_state)+")" +
                     "is the current state"+'\n')
            self.steps.append("active events for current state : "+"Gamma"+"("+str(current_state)+")=" +
                     str(active_events)+'\n')
            for event in active_events:
                if not self.durations[event]:
                    self.steps.append("the {"+event+"}" +
                             " event is active, but all corresponding clocks are already used "+'\n')
                if event not in ordered_events_by_date: # if the event is not already on the ordered list
                    if self.durations[event]:
                        clock = self.durations[event].pop(0)
                        ordered_events_by_date[event] = initial_event_date_t_previous + clock
                        self.steps.append("{"+str(event)+"}" +
                                 " event is active, "+"the corresponding clock '"+
                                 str(clock) +"' will be used and added to the date " +
                                 str(initial_event_date_t_previous)+ '\n')
            for event in self.durations:
                self.steps.append("clock list for the {"+str(event)+"} "+" event : " +str(self.durations[event])+"\n")
            ordered_events_by_date = sort_by_date(ordered_events_by_date)
            self.steps.append("ordered list " +str(ordered_events_by_date) + '\n')
            next_event_e_prime = next(iter(ordered_events_by_date))
            self.steps.append("the {"+str(next_event_e_prime)+"}"+" event is the trigger event, it well be removed from the ordered list\n")
            next_event_date_t_prime = round(ordered_events_by_date[next_event_e_prime],1)
            initial_event_date_t_previous = next_event_date_t_prime
            self.steps.append("t' = " + str(initial_event_date_t_previous)+"\n")
            # print(current_state,next_event_e_prime)
            next_state_x_prime = next_state(current_state, next_event_e_prime, self.transitions)
            # print(next_state_x_prime)
            ordered_events_by_date.pop(next_event_e_prime)
            # get all events except the trigger event that are available on the ordered list
            events = list(ordered_events_by_date.keys())
            # for every active events in the current state, test if this will be active on the next state, if it's not then remove it
            for event in events:
                if not still_active(event,next_state_x_prime, self.gamma):
                    ordered_events_by_date.pop(event)
                    self.steps.append("the event {" +str(event) +"} will be removed because it's not active in the next state"+ '\n')
            self.calendar.append(
                {'event': next_event_e_prime, 'next_state': next_state_x_prime,
                'clock': None, 'date': next_event_date_t_prime})
            counter +=1

    def init_steps(self):
        for event in self.durations:
            self.steps.append("initial clock list for the {" + event +"}" +" event : " + str(self.durations[event]) + "\n")
            self.steps.append("t' = " + str(0)+'\n')

    def output_simulation_details(self):
        file = open("C:/Users/omarm/Desktop/output.txt","w")
        for s in self.steps:
            file.write(s)