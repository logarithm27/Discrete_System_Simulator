from InfiniteModelsInput import *


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


if __name__ == "__main__":
    start_input = InfiniteModelSimulator()