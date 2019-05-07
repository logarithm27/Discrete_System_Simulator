from utility import asking_for_input


class Input:

    def __init__(self):
        self.states = asking_for_input("How many states in the model :  ", "Put your states separated by semicolon : ")
        while self.states is None:
            self.states = asking_for_input("How many states in the model :  ", "Put your states separated by semicolon : ")
        self.events = asking_for_input("How many events : ", "Put events separated by semicolon : ")
        while self.events is None:
            self.events = asking_for_input("How many events : ", "Put events separated by semicolon : ")
        self.state_machine = self.build_state_machine()
        self.gamma = {}
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
            self.gamma[state] = []
        for transition in self.state_machine['transitions']:
            self.gamma[transition['source']].append(transition['event'])
            self.gamma[transition['destination']].append(transition['event'])
        for state in self.gamma:
            self.gamma[state] = sorted(list(dict.fromkeys(self.gamma[state])))  # remove duplicates

    def durations_input(self, random):
        if not random:
            for event in self.events:
                try:
                    self.set_of_durations[event] = list(map(float, input("Put the set of durations of the [" + event + "] event : ").split(',')))
                except None or SyntaxError or ValueError:
                    self.durations_input(random)

    def method_input(self):
        simple_way_or_other_way = input("Simulate by using calculation (enter y ) or without (enter n): ")
        if simple_way_or_other_way == "y".lower():
            return "hard"
        else:
            return "simple"
    def print_data(self):
        print(self.states)
        print(self.events)
        print(self.gamma)
        print(self.set_of_durations)