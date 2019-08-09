import timeit
from Simulator import *
from InfiniteModelsInput import *
from Utility import *


# noinspection PyUnboundLocalVariable
# the Infinite Model class allow us to build the infinite model and make simulation and create the timing graph
# and this is after having the file input which we extracted data from and analyzed in the Infinite Model Input class
# note that the respect of the order of calling methods inside the constructor is forced , i.e : you must call build_infinite_state method
# before calling build_state_machine, because we can't build a state machine without having the entire necessary list of states
class InfiniteModel:
    def __init__(self):
        self.steps = []
        # when we call the constructor of this class outside, we begin by instantiating the Infinite Model Input Class
        # which is responsible for showing messages and interacting with the user on the console
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
        self.finite_state_machine = self.build_state_machine()
        # convert states from tuples to string list
        self.states = list(map(str,self.states))
        # get gamma
        self.gamma = set_of_possible_events_of_all_states(self.states, self.finite_state_machine)
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
        self.x_axis_data = []
        self.y_axis_data = []
        # get the calendar
        self.calendar = []
        # begin the simulation
        self.simulate()
        self.time_execution = 0
        # attributes that will be useful for outputting probabilities charts


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
                # for each state looping through events' descriptions
                for event in self.events_description:
                    # generate a new state by making the sum of state and the description
                    new_state = tuple_sum(self.events_description[event], state)
                    # if the new generated state is not already added on the list of states
                    # and the state is not violating the rules ( min_bounds <= new state <= max_bounds )
                    # then we add this state to the list of states
                    # i.e : [ (0,0) < (1,5) < (1,8) ] (1,5) is a valid state; [(0,0) <||> (-1,18) <||> (1,8)] (-1,18) is not a valid state
                    if new_state not in self.states and check_valid_state(self.min_bounds,self.max_bounds,new_state):
                        self.states.append(new_state)
            max_n += 1

    # begin the simulation
    def simulate(self):
        for transition in self.finite_state_machine:
            print(transition)
        # initializing variables that will be used to calculate event's debits and states's probabilities
        for event in self.events:
            self.debits[event] = 0
            self.sigma_debits[event] = 0
        for state in self.states:
            self.state_probabilities[state] = 0
            self.sigma_probabilities[state] = 0
        # looping until we reach the maximum number of simulation we want to do
        for counter in range(self.number_of_experiences):
            # begin the simulation that help us to generate the timing graph by instantiate a Simulator Object
            simulator = Simulator(self.states[0], None, self.gamma, self.finite_state_machine, RANDOM, self.time_interval[1], self.events, self.lambdas)
            # calling simulate function (the engine of the simulation) from the Simulator class after it was instantiated
            simulator.simulate()
            # each time we simulate, we get the calendar generated after this simulation
            self.calendar = simulator.calendar
            # call the analysis function to make calculations linked to probabilities and debits
            analyse = analysis(self.calendar, self.time_interval, self.debits, self.sigma_debits, self.sigma_probabilities, self.state_probabilities)
            self.debits = analyse[0]
            self.sigma_debits = analyse[1]
            self.sigma_probabilities = analyse[2]
            self.state_probabilities = analyse[3]
        # by the end of all simulations
        analysis_output_values = analysis_output(self.debits,self.sigma_debits,self.sigma_probabilities,self.state_probabilities,self.time_interval,self.number_of_experiences, self.x_axis_data, self.y_axis_data)
        self.debits = analysis_output_values[0]
        self.sigma_debits = analysis_output_values[1]
        self.sigma_probabilities = analysis_output_values[2]
        self.state_probabilities = analysis_output_values[3]
        self.x_axis_data = analysis_output_values[4]
        self.y_axis_data = analysis_output_values[5]
        self.steps = simulator.steps
        for transition in self.finite_state_machine:
            print(transition)
        for element in self.gamma:
            print(str(element) + ": " + str(self.gamma[element]))
        for c in self.calendar:
            print(c)
        print(self.debits)



if __name__ == "__main__":
    execution_time = float(timeit.timeit(lambda: InfiniteModel(), number=1))
    print("exec time : " + str(round(execution_time,6)))
