from Input import Input
from Simulator import *
from Utility import *


class Model:
    def __init__(self):
        self.steps = []
        self.user_input = Input()
        self.lambdas = self.user_input.lambdas
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
        self.debits = {}
        self.sigma_debits = {}
        self.state_probabilities = {}
        self.sigma_probabilities = {}
        for event in self.events:
            self.debits[event] = 0
            self.sigma_debits[event] = 0
        for state in self.states:
            self.state_probabilities[state] = 0
            self.sigma_probabilities[state] = 0
        self.last_clock_pop = {}
        self.number_of_experiences = self.user_input.number_of_simulation
        self._y_s = {}
        self.time_interval = self.user_input.time_interval
        which_method = self.user_input.method_input()
        if which_method == "simple":
            self.simulate_simple_way()
        elif which_method == "hard":
            self.simulate()
        self.x_axis_data = None
        self.y_axis_data = None
        for c in self.calendar:
            print(c)
        print(self.debits)

    # method useful only when we want to simulate using the calculation of y*
    # this method is called from simulate method
    def get_min_y_star_and_arg_event(self, active_events):
        ordered_events_by_clock_value = {}
        for event in active_events:
            if self.durations[event]:
                v = self.durations[event].pop(0)
                # get the first value in the set of clocks for each event
                ordered_events_by_clock_value[event] = v
                self.last_clock_pop[event] = v
        return sorted(ordered_events_by_clock_value.items(), key=lambda event__y_star: (event__y_star[1], event__y_star[0]))  #sort by y*

    # without updating the clock value each time
    def simulate_simple_way(self):
        simulator = None
        if len(self.lambdas) > 0:
            for counter in range(self.number_of_experiences):
                simulator = Simulator(self.transitions['initial_state'], self.durations, self.gamma, self.transitions['transitions'], RANDOM,self.time_interval[1],self.events,self.lambdas)
                simulator.simulate()
                self.calendar = simulator.calendar
                # call the analysis function to make calculations linked to probabilities and debits
                analyse = analysis(self.calendar, self.time_interval, self.debits, self.sigma_debits,
                                   self.sigma_probabilities, self.state_probabilities)
                self.debits = analyse[0]
                self.sigma_debits = analyse[1]
                self.sigma_probabilities = analyse[2]
                self.state_probabilities = analyse[3]
            # by the end of all simulations
            analysis_output_values = analysis_output(self.debits, self.sigma_debits, self.sigma_probabilities,
                                                     self.state_probabilities, self.time_interval,
                                                     self.number_of_experiences)
            self.debits = analysis_output_values[0]
            self.sigma_debits = analysis_output_values[1]
            self.sigma_probabilities = analysis_output_values[2]
            self.state_probabilities = analysis_output_values[3]
            self.x_axis_data = analysis_output_values[4]
            self.y_axis_data = analysis_output_values[5]
            simulator.output_simulation_details()
        else:
            simulator = Simulator(self.transitions['initial_state'], self.durations, self.gamma, self.transitions['transitions'], NON_RANDOM, None, None, None)
            simulator.simulate()
            self.calendar = simulator.calendar
            analyse = analysis(self.calendar, [self.calendar[0]['date'], self.calendar[-1]['date']], self.debits, self.sigma_debits,
                               self.sigma_probabilities, self.state_probabilities)
            self.debits = analyse[0]
            self.sigma_debits = analyse[1]
            self.sigma_probabilities = analyse[2]
            self.state_probabilities = analyse[3]
            # by the end of all simulations
            analysis_output_values = analysis_output(self.debits, self.sigma_debits, self.sigma_probabilities,
                                                 self.state_probabilities, [self.calendar[0]['date'], self.calendar[-1]['date']],
                                                 self.number_of_experiences, self.x_axis_data,self.y_axis_data)
            self.debits = analysis_output_values[0]
            self.sigma_debits = analysis_output_values[1]
            self.sigma_probabilities = analysis_output_values[2]
            self.state_probabilities = analysis_output_values[3]
            self.x_axis_data = analysis_output_values[4]
            self.y_axis_data = analysis_output_values[5]
            print(self.y_axis_data)
            simulator.output_simulation_details()

    # updating the clock value each time and searching for y* and the arg of y*
    def simulate(self):
        self.calendar.append(
            {'event': "Beginning", 'next_state': self.user_input.state_machine['initial_state'],
             'clock': 0.0, 'date': self.initial_event_date_t_previous})
        for event in self.events:
            self._y_s[event] = 0
        while still_more_clocks(self.durations,NON_RANDOM,None,None):
            active_events_that_poped_clocks = []
            current_state = self.calendar[-1]['next_state']
            active_events = self.gamma[current_state]
            get_y_star_and_arg = None
            if len(active_events) == len(self.user_input.events):
                get_y_star_and_arg = self.get_min_y_star_and_arg_event(self.user_input.set_of_durations)
            if len(self.user_input.events) > len(active_events) :
                get_y_star_and_arg = self.get_min_y_star_and_arg_event(active_events)
            for index,element in enumerate(get_y_star_and_arg):
                active_events_that_poped_clocks.append(get_y_star_and_arg[index][0])
            self.min_clock_y_star = get_y_star_and_arg[0][1]  # get value which is a y*
            self.next_event_e_prime = get_y_star_and_arg[0][0]  # get key (arg which is an event )
            self.next_state_x_prime = next_state(current_state, self.next_event_e_prime,self.user_input.state_machine['transitions'])
            self.next_event_date_t_prime = self.initial_event_date_t_previous + self.min_clock_y_star
            self.initial_event_date_t_previous = self.next_event_date_t_prime
            next_possible_events = self.gamma[self.next_state_x_prime]
            for possible_event in next_possible_events:
                if possible_event != self.next_event_e_prime and still_active(possible_event, current_state,self.gamma):
                    if len(self.durations[possible_event]) == 0:
                        if possible_event in active_events_that_poped_clocks:
                            self.durations[possible_event].append(self.last_clock_pop[possible_event] - self.min_clock_y_star)
                    elif len(self.durations[possible_event]) > 0:
                        self.durations[possible_event][0] -= self.min_clock_y_star
            self.calendar.append({'event':  self.next_event_e_prime,
                                  'next_state': self.next_state_x_prime,
                                  'clock': self.min_clock_y_star,
                                  'date': self.next_event_date_t_prime})


if __name__ == '__main__':
    model = Model()

