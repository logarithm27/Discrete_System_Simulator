from InfiniteModelsInput import *
from utility import *

class InfiniteModelSimulator:
    def __init__(self):
        self.start = InfiniteModelInput()
        self.events = self.start.events
        self.states = self.start.states
        self.durations = self.start.set_of_durations
        self.events_description = self.start.events_description
        self.max_number = self.start.number_of_states
        self.max_bounds = self.start.max_bounds
        self.min_bounds = self.start.min_bounds
        self.build_infinite_states()
        self.transitions = self.build_state_machine()
        for transition in self.transitions:
            print(transition)

    def build_state_machine(self):
        transitions = []
        for source_state in self.states:
            for destination_state in self.states:
                for event in self.events_description:
                    state = tuple_sum(self.events_description[event], source_state)
                    if state == destination_state:
                        transitions.append({'event': event, 'source':source_state, 'destination':destination_state})
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



if __name__ == "__main__":
    start_input = InfiniteModelSimulator()