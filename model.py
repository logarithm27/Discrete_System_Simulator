from Input import Input


class Simulator:
    def __init__(self):
        self.user_input = Input()
        self.min_clock_y_star = 0
        self.next_event_e_prime = None
        self.next_state_x_prime = None
        self.initial_event_date_t_previous = 0
        self.next_event_date_t_prime = 0
        self.duration = self.user_input.set_of_durations
        self.min_clock_for_event = {}
        self.calender = []
        self.simulate()
        for c in self.calender:
            print(c)

    def next_state(self, current_state, next_event):
        for transition in self.user_input.state_machine['transitions']:
            if transition['event'] == next_event and transition['source'] == current_state:
                return transition['destination']

    def get_min_y_star_and_arg_event(self):
        for event in self.user_input.set_of_durations:
            self.min_clock_for_event[event] = self.duration[event].pop(0)  # get the first value in the set of clocks for each event
        return sorted(self.min_clock_for_event.items(), key=lambda event_y_star: (event_y_star[1], event_y_star[0]))  #sort by y*

    def simulate(self):
        active = []
        self.calender.append(
            {'event': None, 'next_state': self.user_input.state_machine['initial_state'],
             'clock': 0.0, 'date': self.initial_event_date_t_previous})
        for state in self.user_input.sigma:
            active_events = self.user_input.sigma[state]
            if len(active_events) > 1:
                get_y_star_and_arg = self.get_min_y_star_and_arg_event()
                self.min_clock_y_star = get_y_star_and_arg[0][1]  # get value which is a y*
                self.next_event_e_prime = get_y_star_and_arg[0][0]  # get key (arg which is an event )

            if len(active_events) == 1:  # one active event
                self.min_clock_y_star = self.duration[active_events[0]][0]  # all other states are deactivated except this one
                self.next_event_e_prime = active_events[0]
                self.duration[active_events[0]].pop(0)

            self.next_event_date_t_prime = self.initial_event_date_t_previous + self.min_clock_y_star
            self.initial_event_date_t_previous = self.next_event_date_t_prime
            self.next_state_x_prime = self.next_state(state, self.next_event_e_prime)
            self.calender.append({'event':  self.next_event_e_prime,
                             'next_state': self.next_state_x_prime,
                             'clock': self.min_clock_y_star,
                             'date': self.next_event_date_t_prime})

        for event in self.duration:
            if not self.duration[event]: # if there is no more durations
                pass
            if self.duration[event]:
                active.append(event)

        for active_event in active:
            self.min_clock_y_star = self.duration[active_event].pop(0)
            self.next_event_date_t_prime = self.initial_event_date_t_previous + self.min_clock_y_star
            self.next_event_e_prime = active_event
            self.next_state_x_prime = self.next_state(self.calender[-1]['next_state'], self.next_event_e_prime)
            self.calender.append({'event':  self.next_event_e_prime,
                                  'next_state': self.next_state_x_prime,
                                  'clock': self.min_clock_y_star,
                                  'date': self.next_event_date_t_prime})


