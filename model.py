from Input import Input
from utility import sort_by_date


class Simulator:
    def __init__(self):
        self.user_input = Input()
        self.gamma = self.user_input.gamma
        self.next_state_x_prime = None
        self.next_event_e_prime = None
        self.min_clock_y_star = 0
        self.initial_event_date_t_previous = 0.0
        self.next_event_date_t_prime = 0
        self.duration = self.user_input.set_of_durations
        self.calender = []
        self.last_clock_pop = {}
        self.occurrence = int(sum(self.user_input.set_of_durations[next(iter(self.user_input.set_of_durations))]))
        self.simulate()
        for c in self.calender:
            print(c)

    def next_state(self, current_state, next_event):
        for transition in self.user_input.state_machine['transitions']:
            if transition['event'] == next_event and transition['source'] == current_state:
                return transition['destination']

    def still_active(self, event, state):
        return event in self.gamma[state]

    def get_min_y_star_and_arg_event(self, active_events):
        ordered_events_by_clock_value = {}
        for event in active_events:
            v = self.duration[event].pop(0)
            ordered_events_by_clock_value[event] = v # get the first value in the set of clocks for each event
            self.last_clock_pop[event] = v
        return sorted(ordered_events_by_clock_value.items(), key=lambda event__y_star: (event__y_star[1], event__y_star[0]))  #sort by y*

    def still_more_clocks(self):
        for event in self.duration:
            if self.duration[event]:
                return True
        return False

    # without updating the clock value each time
    def simulate_simple_way(self):
        counter = 0
        ordered_events_by_date = {}
        self.calender.append(
            {'event': None, 'next_state': self.user_input.state_machine['initial_state'],
             'clock': None, 'date': self.initial_event_date_t_previous})
        while self.still_more_clocks():
            current_state = self.calender[-1]['next_state']
            active_events = self.gamma[current_state]
            for event in active_events:
                if self.duration[event]:
                    ordered_events_by_date[event] = self.initial_event_date_t_previous + self.duration[event].pop(0)
            ordered_events_by_date = sort_by_date(ordered_events_by_date)
            for event in self.user_input.events:
                if not self.still_active(event,current_state):
                    ordered_events_by_date.pop(event)
            self.next_event_e_prime = next(iter(ordered_events_by_date))
            self.next_event_date_t_prime = ordered_events_by_date[self.next_event_e_prime]
            self.initial_event_date_t_previous = self.next_event_date_t_prime
            self.next_state_x_prime = self.next_state(current_state, self.next_event_e_prime)
            ordered_events_by_date.pop(self.next_event_e_prime)
            self.calender.append(
                {'event': self.next_event_e_prime, 'next_state': self.next_state_x_prime,
                 'clock': None, 'date': self.next_event_date_t_prime})
            counter +=1

    # updating the clock value each time and searching for y* and the arg of y*
    def simulate(self):
        counter = 0
        self.calender.append(
            {'event': None, 'next_state': self.user_input.state_machine['initial_state'],
             'clock': 0.0, 'date': self.initial_event_date_t_previous})
        while self.still_more_clocks():
            current_state = self.calender[-1]['next_state']
            active_events = self.gamma[current_state]
            get_y_star_and_arg = None
            if len(active_events) == len(self.user_input.events):
                get_y_star_and_arg = self.get_min_y_star_and_arg_event(self.user_input.set_of_durations)
            if len(self.user_input.events) > len(active_events) :
                get_y_star_and_arg = self.get_min_y_star_and_arg_event(active_events)
            self.min_clock_y_star = get_y_star_and_arg[0][1]  # get value which is a y*
            self.next_event_e_prime = get_y_star_and_arg[0][0]  # get key (arg which is an event )
            self.next_state_x_prime = self.next_state(current_state, self.next_event_e_prime)
            next_possible_events = self.gamma[self.next_state_x_prime]
            for possible_event in next_possible_events:
                if possible_event != self.next_event_e_prime and self.still_active(possible_event, current_state):
                    if len(self.duration[possible_event]) == 0:
                        self.duration[possible_event].append(self.last_clock_pop[possible_event] - self.min_clock_y_star)
                    elif len(self.duration[possible_event]) > 0:
                        self.duration[possible_event][-1] -= self.min_clock_y_star
            self.next_event_date_t_prime = self.initial_event_date_t_previous + self.min_clock_y_star
            self.initial_event_date_t_previous = self.next_event_date_t_prime
            self.calender.append({'event':  self.next_event_e_prime,
                                  'next_state': self.next_state_x_prime,
                                  'clock': self.min_clock_y_star,
                                  'date': self.next_event_date_t_prime})
            counter += 1




