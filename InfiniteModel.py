import timeit
from Simulator import *
from InfiniteModelsInput import *
from Utility import *
import datetime
import plotly
import plotly.graph_objs as go

# noinspection PyUnboundLocalVariable
# the Infinite Model class allow us to build the infinite model and make simulation and create the timing graph
# and this is after having the file input which we extracted data from and analyzed in the Infinite Model Input class
# note that the respect of the order of calling methods inside the constructor is forced , i.e : you must call build_infinite_state method
# before calling build_state_machine, because we can't build a state machine without having the entire necessary list of states
class InfiniteModel:
    def __init__(self):
        # when we call the constructor of this class outside, we begin by instantiating the Infinite Model Input Class
        # which is responsible for the showing messages and interacting with the user on the console
        # after interacting with the user, he normally should gave a file to the program
        self.start = InfiniteModelInput()
        # get events
        self.events = self.start.events
        # get states
        self.states = self.start.states
        # get lambdas (used to generate random clocks in Poissonian distribution)
        self.lambdas = self.start.lambdas
        # get events' descriptions
        self.events_description = self.start.events_description
        # get the maximum bound ( useful to generate infinite or bounded number of states in the infinite model )
        self.max_number = self.start.number_of_states
        # get the max bounds ( each state should not be above it )
        self.max_bounds = self.start.max_bounds
        # get the min bounds (each state shouldn't be below it )
        self.min_bounds = self.start.min_bounds
        # get number of experience of number of simulations to do ( useful for calculating debits and probabilities )
        self.number_of_experiences = self.start.number_of_experiences
        # get the time interval which will be useful to calculate states' activity probability in that interval
        self.time_interval = self.start.time_interval
        # call it to generate states
        self.build_infinite_states()
        # building the infinite automaton and memorizing the transitions of that infinite model in self.transitions variable
        self.transitions = self.build_state_machine()
        # convert states from tuples to string list
        self.states = list(map(str,self.states))
        # get gamma
        self.gamma = set_of_possible_events_of_all_states(self.states, self.transitions)
        # field to memorize events debit
        self.debits = {}
        # field able to make the sum of debits through the number of simulation ( at the end this sigma or sum that corresponds to a particular
        # event will be divided by the number of simulation done)
        # it's a dictionary, each key is an event and each value is a sum of debits of that event
        self.sigma_debits = {}
        # field (also a dictionary) able to memorize the probabilities of each state
        self.state_probabilities = {}
        # sigma is the sum of probabilities of each event ( it's a dictionary, the keys are states, the values are the sum )
        self.sigma_probabilities = {}
        # get the calendar
        self.calendar = []
        # begin the simulation
        self.simulate()

    # function to build the infinite automaton after generating the infinite states in
    # the build_infinite_states function
    def build_state_machine(self):
        transitions = []
        # for every state in states list, we make nested loop to make a matrix
        # i.e : columns are states and lines are also states to know links ( or transitions between states )
        for source_state in self.states:
            for destination_state in self.states:
                # for every element in the event description
                for event in self.events_description: # O(n x m x l) exponential
                    # make a sum of two points ( the first point is the source state ( state from which we go ) the second point
                    # is the event description )
                    # i.e : the event 'arrive" have the description (0,1) and we are in the (1,2) state, so from that state
                    # if we trigger the (0,1) event we will go to a new state (0+1,2+1,) = (1,3)
                    state = tuple_sum(self.events_description[event], source_state)
                    # if state corresponds to a valid destination
                    if state == destination_state:
                        # we add the transition to this form source----event---->destination
                        # i.e : (0,1)STATE -----ARRIVE EVENT------>(1,3) STATE
                        transitions.append({'event': event, 'source':str(source_state), 'destination':str(destination_state)})
        return transitions

    # generating infinite states ( bounded by a given maximum number N )
    # we build this states under particular rules designated by the user in the input file like ( minimum bounds, maximum bounds )
    def build_infinite_states(self):
        # variable used as a counter the make a limit to the while loop
        max_n = 0
        # while we're not reaching yet the maximum number ( or maximum bound )
        while max_n < self.max_number:
            # converting the list of the states into a list that contains unique states
            # i.e we may generate a state reachable from two or three states, so the behaviour of the algorithm
            # will add this state three times to the list, and to prevent this redundancy and because a model contains unique
            # states, we convert this list into a sorted list without double elements
            states = sorted(list(dict.fromkeys(self.states)))
            # looping through the states
            for state in states:
                # for each state looping through an event description
                for event in self.events_description:
                    # generate a new state by making the sum of state and the description
                    new_state = tuple_sum(self.events_description[event], state)
                    # if the new generated state is not already added on the list of states
                    # and the state is not violating the rules ( min_bounds <= new state <= max_bounds )
                    # then we add this state to the list of states
                    # i.e : [ (0,0) < (1,5) < (1,8) ] (1,5) is a valid state; [(0,0) # (-1,18) # (1,8)] (-1,18) is not a valid state
                    if new_state not in self.states and check_valid_state(self.min_bounds,self.max_bounds,new_state):
                        self.states.append(new_state)
            max_n += 1

    # begin the simulation
    def simulate(self):
        # initializing variables that will be used to calculate event's debits and states's probabilities
        for event in self.events:
            self.debits[event] = 0
            self.sigma_debits[event] = 0
        for state in self.states:
            self.state_probabilities[state] = 0
            self.sigma_probabilities[state] = 0
        print("Simulating ...")
        # looping until we reach the maximum number of simulation we want to do
        for counter in range(self.number_of_experiences):
            # begin the simulation that help us to generate the timing graph by instantiate a Simulator Object
            simulator = Simulator(self.states[0], None, self.gamma, self.transitions, RANDOM, self.time_interval[1], self.events, self.lambdas)
            # calling simulate function (the engine of the simulation) from the Simulator class after it was instantiated
            simulator.simulate()
            # each time we simulate, we get the calendar generated after this simulation
            self.calendar = simulator.calendar
            for index,c in enumerate(self.calendar[:-1]):
                # if the date that corresponds to the activation of an event is between the given date interval
                if self.time_interval[0] < c['date'] < self.time_interval[1]:
                    # increment the occurrence counter
                    self.debits[c['event']] += 1
                # -------calculating probabilities of each state being active in the given interval--------
                # initialize the variable that will be used to calculate the time interval where each state is active
                interval_state_active = 0
                # if the state is active between an interval ot time that began with a value less than the minimum value
                # or the minimum bound given in the interval ot time and a value less than or equal to the maximum bound or value in the time interval
                if self.calendar[index]['date'] <= self.time_interval[0] < self.calendar[index + 1]['date'] <= self.time_interval[1]:
                    # the state is active between [ the minimum value given in the time interval - the date when the state is no longer active ]
                    interval_state_active = self.calendar[index + 1]['date'] - self.time_interval[0]
                # if the state is active between the given time interval
                if self.time_interval[0]<= self.calendar[index]['date'] < self.calendar[index +1]['date'] <= self.time_interval[1]:
                    interval_state_active = self.calendar[index + 1]['date'] - self.calendar[index]['date']
                # if the state is active between a date greater than the minimum bound or value and a value that's greater
                # than the maximum bound of the given time interval
                if self.time_interval[0] <= self.calendar[index]['date'] <= self.time_interval[1] < self.calendar[index + 1]['date']:
                    # state is active on [ the start date when the state is being active - maximum bound ]
                    interval_state_active = self.time_interval[1] - self.calendar[index]['date']
                # each state has it's own probability, each time we face that state, with add the corresponding interval time of being active
                # we add that date as long as we're going until the end of the simulation
                # this is not the real probability for now, it will be calculated later, for now we're using the same variable for adding the dates
                self.state_probabilities[c['next_state']] += interval_state_active
            # after collecting data and counting the probabilities of state activity status
            for state in self.state_probabilities:
                # we now calculate the probabilities, by dividing each value calculated previously ( sum intervals where each state was active ) by the
                # subtracting the max bound by the min bound
                self.state_probabilities[state] = self.state_probabilities[state]/(self.time_interval[1] - self.time_interval[0])
                # for statistical use, as long as we go through the number of simulation, we add the calculated probability
                # i.e : we have 100 simulation, the sigma ( sum of probabilities ) will be the sum of probabilities 100 times
                # note that each state has it's own probability
                self.sigma_probabilities[state] += self.state_probabilities[state]
            # still inside the simulation, iterating through calculated occurrence of each event
            for event in self.debits:
                # calculate the debit by dividing number of occurrence of each event by T2 - T1
                self.debits[event] = self.debits[event] / (self.time_interval[1] - self.time_interval[0])
                # while we're inside the main loop ( number of experiences, simulations ) we add the calculated debit
                # that corresponds to a particular event to the new one ( we build a sum of debits for each event)
                self.sigma_debits[event] += self.debits[event]
        # by the end of all simulations
        for state in self.sigma_probabilities:
            # we calculate the final probability of each state by dividing the sigma by the number of simulations
            self.state_probabilities[state] = round((self.sigma_probabilities[state]/self.number_of_experiences),4)
        # by the end the simulations
        for single_sigma_debit in self.sigma_debits:
            # dividing the sum of debits of each event by the number of experiences to get a new debit
            self.debits[single_sigma_debit] = round(self.sigma_debits[single_sigma_debit]/self.number_of_experiences,3)
        # get current directory path and write a file of the name probability.txt to show the calculated probabilities
        file = open(str(os.path.dirname(os.path.realpath(__file__)))+"/probability.txt","w")
        file.write(str(datetime.datetime.now())+"\n"+"P[ T1 < t < T2] (State X) = Probability" + "\n")
        # initializing this list that represent the x_axis of the chart ( x axis will holds the set of states )
        x_axis_data = []
        # each state has it's own probability, and this probability will be held by the y axis
        y_axis_data = []
        # showing the probabilities in two different ways :
        # first way : display it in a nice graphical chart by generating an html file
        # second way : write probabilities in an output file
        for state in self.state_probabilities:
            # add each state to the x axis
            x_axis_data.append(state)
            # add the corresponding probability of that state to the y axis
            y_axis_data.append(self.state_probabilities[state])
            # write the probabilities on the probability.txt output file
            file.write("P["+str(self.time_interval[0])+" < t < "+str(self.time_interval[1])+"] ("+str(state)+") = " +str(self.state_probabilities[state]) + "\n")
        # generating the file and open it automatically by setting up the auto_open to True
        plotly.offline.plot({
            "data": [go.Scatter(x=x_axis_data, y=y_axis_data)],
            "layout": go.Layout(title="Probability that each state was active between the time interval : " + str(self.start.time_interval))
        }, auto_open=True)
        # output steps of simulation in a file
        simulator.output_simulation_details()

        for transition in self.transitions:
            print(transition)
        for element in self.gamma:
            print(str(element) + ": " + str(self.gamma[element]))
        for c in self.calendar:
            print(c)


if __name__ == "__main__":
    execution_time = float(timeit.timeit(lambda: InfiniteModel(), number=1))
    print("exec time : " + str(round(execution_time,6)))