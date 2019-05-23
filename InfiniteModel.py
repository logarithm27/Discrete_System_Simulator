import timeit
from Simulator import *
from InfiniteModelsInput import *
from utility import *

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
        self.durations = random_durations_generator(self.events, self.lambdas, self.start.number_of_states)
        self.time_interval = self.start.time_interval
        self.stats = {}
        self.stats_states = {}
        self.probabilities = {}
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
            self.stats[event] = 0
        for state in self.states:
            self.stats_states[state] = 0
            self.probabilities[state] = 0
        date_interval = 0
        print("Simulating ...")
        for counter in range(self.number_of_experiences):
            simulator = Simulator(self.states[0],random_durations_generator(self.events, self.lambdas, self.start.number_of_states),self.gamma,self.transitions)
            simulator.simulate()
            self.calendar = simulator.calendar
            if self.number_of_experiences != 1:
                for index,c in enumerate(self.calendar[:-1]):
                    if self.time_interval[0] < c['date'] < self.time_interval[1] and self.calendar[index-1]['event'] != self.calendar[index]['event']:
                        self.stats[c['event']] += 1
                    if self.time_interval[0] < c['date'] < self.time_interval[1] and self.calendar[index-1]['next_state'] != self.calendar[index]['next_state']:
                        self.stats_states[c['next_state']] += 1
            date_interval += self.calendar[-1]['date']
        date_interval = round(date_interval/self.number_of_experiences,1)
        if self.number_of_experiences != 1:
            for event in self.stats:
                self.stats[event] = round(self.stats[event]/(self.time_interval[1] - self.time_interval[0]),1)
                print(str(event)+" : "+str(self.stats[event]))
            for state in self.stats_states:
                # number of times that the state appeared in all experiments divided by the total number of experiments
                number_of_occurence = round(self.stats_states[state]/self.number_of_experiences,1)
                # rate, calculating lambda by dividing the number of of apparition
                lambda_state= round(self.stats_states[state]/date_interval,1)

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