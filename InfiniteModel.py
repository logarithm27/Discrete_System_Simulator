import os
import timeit
from Simulator import *
from InfiniteModelsInput import *
from Utility import *
import datetime
import plotly
import plotly.graph_objs as go

# noinspection PyUnboundLocalVariable
class InfiniteModel:
    def __init__(self):
        self.start = InfiniteModelInput()
        self.events = self.start.events
        self.states = self.start.states
        self.lambdas = self.start.lambdas
        self.events_description = self.start.events_description
        self.max_number = self.start.number_of_states
        self.max_bounds = self.start.max_bounds
        self.min_bounds = self.start.min_bounds
        self.number_of_experiences = self.start.number_of_experiences
        self.time_interval = self.start.time_interval
        self.build_infinite_states()
        self.transitions = self.build_state_machine()
        self.states = list(map(str,self.states))
        self.gamma = set_of_possible_events_of_all_states(self.states, self.transitions)
        self.time_interval = self.start.time_interval
        self.debits = {}
        self.sigma_debits = {}
        self.state_probabilities = {}
        self.sigma_probabilities = {}
        self.calendar = []
        self.simulate()


    def build_state_machine(self):
        transitions = []
        for source_state in self.states:
            for destination_state in self.states:
                for event in self.events_description: # O(n x m x l) exponential
                    state = tuple_sum(self.events_description[event], source_state)
                    if state == destination_state:
                        transitions.append({'event': event, 'source':str(source_state), 'destination':str(destination_state)})
        return transitions

    def build_infinite_states(self):
        max_n = 0
        while max_n < self.max_number:
            states = sorted(list(dict.fromkeys(self.states)))
            for state in states:
                for event in self.events_description:
                    new_state = tuple_sum(self.events_description[event], state)
                    if new_state not in self.states and check_valid_state(self.min_bounds,self.max_bounds,new_state):
                        self.states.append(new_state)
            max_n += 1

    def simulate(self):
        for event in self.events:
            self.debits[event] = 0
            self.sigma_debits[event] = 0
        for state in self.states:
            self.state_probabilities[state] = 0
            self.sigma_probabilities[state] = 0
        print("Simulating ...")
        for counter in range(self.number_of_experiences):
            simulator = Simulator(self.states[0], random_durations_generator(self.events, self.lambdas), self.gamma, self.transitions, RANDOM, self.time_interval[1], self.events, self.lambdas)
            simulator.simulate()
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
        # get current directory path
        file = open(str(os.path.dirname(os.path.realpath(__file__)))+"/probability.txt","w")
        file.write(str(datetime.datetime.now())+"\n"+"P[ T1 < t < T2] (State X) = Probability" + "\n")
        x_axis_data = []
        y_axis_data = []
        for state in self.state_probabilities:
            x_axis_data.append(state)
            y_axis_data.append(self.state_probabilities[state])
            file.write("P["+str(self.time_interval[0])+" < t < "+str(self.time_interval[1])+"] ("+str(state)+") = " +str(self.state_probabilities[state]) + "\n")
        plotly.offline.plot({
            "data": [go.Scatter(x=x_axis_data, y=y_axis_data)],
            "layout": go.Layout(title="Probability that each state was active between the time interval : " + str(self.start.time_interval))
        }, auto_open=True)
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