from fysom import Fysom


def asking_for_input(ask_for_number_of_data, ask_for_data):
    try:
        number_of_data = int(input(ask_for_number_of_data))
        if "states" in ask_for_number_of_data:
            while number_of_data <= 1:
                print("invalid model, try again")
                number_of_data = int(input(ask_for_number_of_data))
        if "events" in ask_for_number_of_data:
            while number_of_data == 0:
                print("invalid model, try again")
                number_of_data = int(input(ask_for_number_of_data))
        data = sorted(list(dict.fromkeys(input(ask_for_data).split(','))))  # sorting the input in natural order, then convert the input to a list, then remove duplicate values
        while len(data) < number_of_data or len(data) > number_of_data or "" in data or " " in data:
            print('invalid input, try again')
            data = sorted(list(dict.fromkeys(input(ask_for_data).split(','))))
    except None or ValueError or SyntaxError:
        print('invalid input, try again')
        return None
    return data


class Input:

    def __init__(self):
        self.states = asking_for_input("How many states in the model :  ", "Put your states separated by semicolon : ")
        while self.states is None:
            self.states = asking_for_input("How many states in the model :  ", "Put your states separated by semicolon : ")
        self.events = asking_for_input("How many events : ", "Put events separated by semicolon : ")
        while self.events is None:
            self.events = asking_for_input("How many events : ", "Put events separated by semicolon : ")
        self.state_machine = self.build_state_machine()
        self.sigma = {}
        self.set_of_possible_events_of_all_states()
        self.set_of_durations = {}  # may be random
        self.durations_input(False)

    def build_state_machine(self):
        transitions = []
        initial_state = input("What's the initial state : ")
        while initial_state not in self.states:
            print("Try to put one of the following states " + str(self.states) + " ! try again ")
            initial_state = input("What's the initial state : ")
        print("Put the transitions' sequence of your model i.e : event : "+ self.states[0]+" ---> "+
              self.states[1]+' : ' + self.events[0]+'\n' + "if there's no transition, hit Enter")
        for source_state in self.states:
            for destination_state in self.states:
                current_event = input(source_state + " ---> " + destination_state + " : ")
                while current_event not in self.events and current_event != "":
                    print("Invalid event, try again")
                    current_event = input(source_state + " ---> " + destination_state + ": ")
                if current_event == "":
                    pass
                else:
                    transitions.append({'event': current_event, 'source': source_state, 'destination': destination_state})
        return {'initial_state': initial_state, 'transitions': transitions}

    def set_of_possible_events_of_all_states(self):
        for state in self.states:
            self.sigma[state] = []
        for states in self.state_machine['transitions']:
            self.sigma[states['source']].append(states['event'])
            self.sigma[states['destination']].append(states['event'])
        for state in self.sigma:
            self.sigma[state] = sorted(list(dict.fromkeys(self.sigma[state])))  # remove duplicates

    def durations_input(self, random):
        if not random:
            for event in self.events:
                try:
                    self.set_of_durations[event] = list(map(float, input("Put the set of durations of the [" + event + "] event : ").split(',')))
                except None or SyntaxError or ValueError:
                    self.durations_input(random)

    def print_data(self):
        print(self.states)
        print(self.events)
        print(self.sigma)
        print(self.set_of_durations)


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






if __name__ == '__main__':
    simulator = Simulator()

