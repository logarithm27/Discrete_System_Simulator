from Input import Input


class Simulator:
    def __init__(self):
        self.user_input = Input()
        self.sigma = self.user_input.sigma
        self.current_state = self.user_input.state_machine['initial_state']
        self.next_state_x_prime = None
        self.current_event = None
        self.next_event_e_prime = None
        self.min_clock_y_star = 0
        self.initial_event_date_t_previous = 0
        self.next_event_date_t_prime = 0
        self.next_clock_value = 0
        self.duration = self.user_input.set_of_durations
        self.duration_buffer = self.duration
        self.min_clock_for_event = {}
        self.calender = []
        self.last_clock_pop = {}
        self.simulate()
        for c in self.calender:
            print(c)

    def next_state(self, current_state, next_event):
        for transition in self.user_input.state_machine['transitions']:
            if transition['event'] == next_event and transition['source'] == current_state:
                return transition['destination']

    def still_active(self, event, state):
        return event in self.sigma[state]

    def get_min_y_star_and_arg_event(self):
        for event in self.user_input.set_of_durations:
            v = self.duration[event].pop(0)
            self.min_clock_for_event[event] = v  # get the first value in the set of clocks for each event
            self.last_clock_pop[event] = v
        return sorted(self.min_clock_for_event.items(), key=lambda event_y_star: (event_y_star[1], event_y_star[0]))  #sort by y*

    def get_min_y_star_and_arg_event_2(self, active_events):
        for event in active_events:
            v = self.duration[event].pop(0)
            self.min_clock_for_event[event] = v # get the first value in the set of clocks for each event
            self.last_clock_pop[event] = v
        return sorted(self.min_clock_for_event.items(), key=lambda event_y_star: (event_y_star[1], event_y_star[0]))  #sort by y*

    def simulate(self):
        counter = 0
        self.calender.append(
            {'event': None, 'next_state': self.user_input.state_machine['initial_state'],
             'clock': 0.0, 'date': self.initial_event_date_t_previous})
        occurrence = int(sum(self.user_input.set_of_durations[next(iter(self.user_input.set_of_durations))]))
        print(occurrence)
        while counter < occurrence:
            print(counter)
            last_state = self.calender[-1]['next_state']
            active_events = self.sigma[last_state]
            get_y_star_and_arg = None
            if len(active_events) == len(self.user_input.events):
                get_y_star_and_arg = self.get_min_y_star_and_arg_event()
            if len(self.user_input.events) > len(active_events) :
                get_y_star_and_arg = self.get_min_y_star_and_arg_event_2(active_events)
            self.min_clock_y_star = get_y_star_and_arg[0][1]  # get value which is a y*
            self.next_event_e_prime = get_y_star_and_arg[0][0]  # get key (arg which is an event )
            self.next_state_x_prime = self.next_state(last_state, self.next_event_e_prime)
            next_possible_events = self.sigma[self.next_state_x_prime]
            for possible_event in next_possible_events:
                if possible_event != self.next_event_e_prime and self.still_active(possible_event, last_state):
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




