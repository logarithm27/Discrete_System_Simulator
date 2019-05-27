import os

from Utility import *
import datetime

class Simulator:
    def __init__(self, initial_state, durations, gamma, transitions, random_or_not, time_limit, events, lambdas):
        # calendar is the data structure used to hold the timing information
        # each element in the calendar is a dictionary
        # each dictionary has four keys : event, next state, clock, date
        # the event key represent the event that's being triggered
        # the date key represent the date when the event is triggered
        # next state is the state that will be active starting from the corresponding date when the event is triggered to the next the date
        # event 1                                     event 2
        #   |                                           |
        #   |------------- STATE X ---------------------|
        # t=1                                          t=2
        # the date when an event is triggered is the start date when a state is being active, and the next date that corresponds to next event triggering
        # is corresponding to the end or the date when the state is no longer active ( or may be it will be active again )
        # each key contain a value, i.e 'event' : Arriving_event 'date': 2.3 ...
        self.calendar = []
        # steps is a list that collects information of steps that being used along each simulation in order to output it in file at the end
        self.steps = []
        # given initial state in order to start simulation from that state
        self.initial_state = initial_state
        # the list of durations given by the user if he don't want to generate it randomly
        self.durations = durations
        # gamma is a dictionary that contains states as keys, and values as list of events
        # gamma is used to look up for active events or possible events from a particular state
        # i.e : gamma(1)=[arrive, leave] ===> if we're on the state '1', we have then two possible events : arrive and leave
        self.gamma = gamma
        # transitions : is data structure used in order to represent the different transitions in a model
        # transitions id list of dictionaries, each element (dictionary) contain a particular transition,
        # each transition (element, dictionary) have 3 keys : event, source, destination
        # i.e event : arrive, source : X1, destination : X2 ---> it means from the state X1, if we trigger the 'arrive' event, we're going to the new state X2
        self.transitions = transitions
        # this variable is used to distinguish between the two types of durations used in the simulation
        # if it's random, then we can generate the clocks randomly
        # this will be used in still_more_clocks function inside the simulate function
        self.random_or_not = random_or_not
        # time limit is a variable used only if we simulate an infinite model from an input file
        # it's used in the still_more_clocks function inside the simulate function in order to determine if we stop the simulation at that
        # date limit or not, i.e : if we reach simulation at a date greater thant the time_limit, then we've reached the end of the simulation
        self.time_limit = time_limit
        # lambdas is a dictionary, the keys are the events, and the values are ordinary values
        # lambdas is used in order to generate random clocks in random_durations_generator function (Utility file)
        # each lambda is used in an exponential distribution equation (equation used to generate the random clocks )
        self.lambdas = lambdas
        # the events represents the list of events
        self.events = events

    def simulate(self):
        counter = 1
        self.init_steps()
        ordered_events_by_date = {}
        initial_event_date_t_previous = 0.0

        self.calendar.append({'event': None, 'next_state': self.initial_state,
                 'clock': None, 'date': initial_event_date_t_previous})
        # if there we still have clock values on the durations list
        while still_more_clocks(self.durations, self.random_or_not, self.calendar[-1]['date'], self.time_limit):
            if self.random_or_not == RANDOM:
                self.durations = random_durations_generator(self.events, self.lambdas)
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
            next_state_x_prime = next_state(current_state, next_event_e_prime, self.transitions)
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
        file = open(str(os.path.dirname(os.path.realpath(__file__)))+"/steps.txt","w")
        file.write(str(datetime.datetime.now())+"\n")
        for s in self.steps:
            file.write(s)
