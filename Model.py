from Input import Input
from Simulator import *
from Utility import *


class Model:
    def __init__(self):
        self.steps = []
        self.user_input = Input()
        self.gamma = self.user_input.gamma
        self.next_state_x_prime = None
        self.next_event_e_prime = None
        self.min_clock_y_star = 0
        self.initial_event_date_t_previous = 0.0
        self.next_event_date_t_prime = 0
        self.durations = self.user_input.set_of_durations
        self.events = self.user_input.events
        self.states = self.user_input.states
        self.transitions = self.user_input.state_machine
        self.calendar = []
        self.last_clock_pop = {}
        which_method = self.user_input.method_input()
        if which_method == "simple":
            self.simulate_simple_way()
        elif which_method == "hard":
            self.simulate()
        for c in self.calendar:
            print(c)

    def get_min_y_star_and_arg_event(self, active_events):
        ordered_events_by_clock_value = {}
        for event in active_events:
            if self.durations[event]:
                v = self.durations[event].pop(0)
                ordered_events_by_clock_value[event] = v # get the first value in the set of clocks for each event
                self.last_clock_pop[event] = v
        return sorted(ordered_events_by_clock_value.items(), key=lambda event__y_star: (event__y_star[1], event__y_star[0]))  #sort by y*

    # without updating the clock value each time
    def simulate_simple_way(self):
        simulator = Simulator(self.transitions['initial_state'], self.durations, self.gamma, self.transitions['transitions'], FINITE, None, None, None)
        simulator.simulate()
        simulator.output_simulation_details()
        self.calendar = simulator.calendar

    # updating the clock value each time and searching for y* and the arg of y*
    def simulate(self):
        self.calendar.append(
            {'event': None, 'next_state': self.user_input.state_machine['initial_state'],
             'clock': 0.0, 'date': self.initial_event_date_t_previous})
        while still_more_clocks(self.durations):
            current_state = self.calendar[-1]['next_state']
            active_events = self.gamma[current_state]
            get_y_star_and_arg = None
            if len(active_events) == len(self.user_input.events):
                get_y_star_and_arg = self.get_min_y_star_and_arg_event(self.user_input.set_of_durations)
            if len(self.user_input.events) > len(active_events) :
                get_y_star_and_arg = self.get_min_y_star_and_arg_event(active_events)
            self.min_clock_y_star = get_y_star_and_arg[0][1]  # get value which is a y*
            self.next_event_e_prime = get_y_star_and_arg[0][0]  # get key (arg which is an event )
            self.next_state_x_prime = next_state(current_state, self.next_event_e_prime,self.user_input.state_machine['transitions'])
            next_possible_events = self.gamma[self.next_state_x_prime]
            for possible_event in next_possible_events:
                if possible_event != self.next_event_e_prime and still_active(possible_event, current_state,self.gamma):
                    if len(self.durations[possible_event]) == 0:
                        self.durations[possible_event].append(self.last_clock_pop[possible_event] - self.min_clock_y_star)
                    elif len(self.durations[possible_event]) > 0:
                        self.durations[possible_event][-1] -= self.min_clock_y_star
            self.next_event_date_t_prime = self.initial_event_date_t_previous + self.min_clock_y_star
            self.initial_event_date_t_previous = self.next_event_date_t_prime
            self.calendar.append({'event':  self.next_event_e_prime,
                                  'next_state': self.next_state_x_prime,
                                  'clock': self.min_clock_y_star,
                                  'date': self.next_event_date_t_prime})




