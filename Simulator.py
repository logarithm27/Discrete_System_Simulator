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
        # the clock is used only if use the method where we're updating the clock by doing some calculations
        # the clock is None or null if we use the simple method, where we stock and order events in a list by their dates
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
        # initializing the steps list with and introduction string
        self.init_steps()
        # this variable is a dictionary that contains events ordered by their date
        # i.e {(arrive,1),(leave,2)...}
        # this data structure help us to build the timing after the simulation by memorising the order temporarily
        # because the calendar is the data structure used to build the timing graph
        ordered_events_by_date = {}
        # this is the initial date where the simulation is starting from
        initial_event_date_t_previous = 0.0
        # initialize the calendar with initial values
        self.calendar.append({'event': "Beginning", 'next_state': self.initial_state,
                 'clock': None, 'date': initial_event_date_t_previous})
        # still more clocks has two features depending on the type of generating the clocks ( random or not )
        # if we generate clocks randomly, then we should have the last date reached in the simulation by having ( self.calendar[-1]['date'] )
        # and the time limit ( the date which represents the max bounds in the given interval )
        # Normally, self.durations is useless, but we still need it as a parameter to run the function properly
        # because we may not generate clocks randomly, and instead of that we'll need a given list of durations, and at that time
        # self.durations become extremely useful
        # in summary, if we generate clocks randomly, we will need all parameters except the self.durations will be None
        # if we have a given list of durations, we will need self.durations and self.random_or_not variables
        # and we're no longer needing the other variables
        # And instead of creating different functions and doing the boring job by repeating the code,
        # I prefer to use the same function for both kind of options ( there's other smarter ways to do it ) ,
        # so notice that all parameters are useful and useless depending on the situation
        # note that when we're calling the constructor we can designate the useless parameters by putting None keyword
        # don't put None Keyword on a parameter that's paramount and useful i.e : don't put None keyword in the parameter
        # time_limit when you're generating clocks randomly
        while still_more_clocks(self.durations, self.random_or_not, self.calendar[-1]['date'], self.time_limit):
            # while we're not reaching the end of the simulation we check if we generate clocks randomly
            # note that when we generate clocks randomly, we need to generate it each time for each event
            if self.random_or_not == RANDOM:
                # generate random clocks for that iteration
                self.durations = random_durations_generator(self.events, self.lambdas)
            self.steps.append(str(counter) + " iteration :"+"\n"+"-------------"+"\n")
            # get the current state from the last added state from the calender dictionary
            current_state = self.calendar[-1]['next_state']
            # get the possible active events by passing the current state inside the gamma function
            active_events = self.gamma[current_state]
            self.steps.append("("+str(current_state)+")" +
                     "is the current state"+'\n')
            self.steps.append("active events for current state : "+"Gamma"+"("+str(current_state)+")=" +
                     str(active_events)+'\n')
            # looping through the active events
            for event in active_events:
                if not self.durations[event]:
                    self.steps.append("the {"+event+"}" +
                             " event is active, but all corresponding clocks are already used "+'\n')
                # if the event is not already on the ordered list ( we will not update the date to an existing event in the ordered list)
                if event not in ordered_events_by_date:
                    # we won't use the list that holds clocks that corresponds to a particular event if and only if it have
                    # an item ( clock )
                    # i.e : the event arrive have the list of clocks [1.6,2], the event leave have an empty list []
                    # so if we encounter the arrive event we will pop 1.6 as the clock and we will use it to update the time
                    # but if we encounter the leave event, we will not pop any item because of the emptiness of the it's duration list
                    if self.durations[event]:
                        clock = self.durations[event].pop(0)
                        # update the date that corresponds to an event by adding the clock from the list duration
                        ordered_events_by_date[event] = initial_event_date_t_previous + clock
                        self.steps.append("{"+str(event)+"}" +
                                 " event is active, "+"the corresponding clock '"+
                                 str(clock) +"' will be used and added to the date " +
                                 str(initial_event_date_t_previous)+ '\n')
            for event in self.durations:
                self.steps.append("clock list for the {"+str(event)+"} "+" event : " +str(self.durations[event])+"\n")
            # ordering the list of events by their dates i.e : {'arrive': 1.6, 'leave':2 ...}
            ordered_events_by_date = sort_by_date(ordered_events_by_date)
            self.steps.append("ordered list " +str(ordered_events_by_date) + '\n')
            # the event that will be added to the calendar is the first element of the ordered list ( the event who have the smallest date value )
            next_event_e_prime = list(ordered_events_by_date.keys())[0]
            self.steps.append("the {"+str(next_event_e_prime)+"}"+" event is the trigger event, it well be removed from the ordered list\n")
            # get the corresponding date of the trigger event (next_event_e_prime) and round it to 1 digit after the comma ( floating number )
            next_event_date_t_prime = round(ordered_events_by_date[next_event_e_prime],1)
            # updating the date that will be used next time and added to a clock
            # i.e the event arrive happens at the 1.5 date, and the next event will be the leave event and it has a clock of 0.5
            # so the next date will be 0.5+1.5 = 2 , then the leave event will happen at a date 't' equals to 2
            initial_event_date_t_previous = next_event_date_t_prime
            self.steps.append("t' = " + str(initial_event_date_t_previous)+"\n")
            # get the next state by knowing the current state we're in and next event that will be triggered starting from this current state
            next_state_x_prime = next_state(current_state, next_event_e_prime, self.transitions)
            # after memorizing the event in the next_event_e_prime variable
            # and the date in the next_event_date_t_prime that will be used as the next event that will be triggered
            # we don't no longer need this information, then we will pop or remove this events and it's corresponding date from the
            # ordered list
            ordered_events_by_date.pop(next_event_e_prime)
            # get all events except the trigger event (because it was removed) that are available on the ordered list
            events = list(ordered_events_by_date.keys())
            # for every active events in the current state, test if this will be active on the next state, if it's not then remove it
            for event in events:
                if not still_active(event,next_state_x_prime, self.gamma):
                    ordered_events_by_date.pop(event)
                    self.steps.append("the event {" +str(event) +"} will be removed because it's not active in the next state"+ '\n')
            # the calendar will hold and memorize all the variable used above (trigger event, next state , date ..)
            self.calendar.append(
                {'event': next_event_e_prime, 'next_state': next_state_x_prime,
                'clock': None, 'date': next_event_date_t_prime})
            counter +=1
            # sometimes we have two events that may occur at the same time
            # we don't want that, so we will sacrifice by removing one of them
            # such that way we will have only one event that is occurring at that time


    # initializing the string that will be the first line in our output file after the simulation
    def init_steps(self):
        if self.durations is not None:
            for event in self.durations:
                self.steps.append("initial clock list for the {" + event +"}" +" event : " + str(self.durations[event]) + "\n")
                self.steps.append("t' = " + str(0)+'\n')
        else :
            self.steps.append("Clocks are generated randomly" + "\n")

    # function responsible of output steps and details after end of simulation
    def output_simulation_details(self):
        # open the current program directory and create a file of the name steps.txt with 'w' mode which stand for create a file if
        # doesn't exist, or overwrite it if it already exist
        file = open(str(os.path.dirname(os.path.realpath(__file__)))+"/steps.txt","w")
        # write the date (help to know the time of program execution )
        file.write(str(datetime.datetime.now())+"\n")
        # each element in the steps list represent a step or a line
        for s in self.steps:
            # write steps line by line
            file.write(s)
        file.close()
