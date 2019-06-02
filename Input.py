from Utility import *


class Input:

    def __init__(self):
        self.states = asking_for_input("How many states in the model :  ", "Put your states separated by semicolon : ")
        while self.states is None:
            self.states = asking_for_input("How many states in the model :  ", "Put your states separated by semicolon : ")
        self.events = asking_for_input("How many events : ", "Put events separated by semicolon : ")
        while self.events is None:
            self.events = asking_for_input("How many events : ", "Put events separated by semicolon : ")
        self.state_machine = self.build_state_machine()
        self.gamma = set_of_possible_events_of_all_states(self.states,self.state_machine['transitions'])
        self.set_of_durations = {}  # may be random
        self.random = False
        self.check_durations_input_option()
        self.lambdas= {}
        self.number_of_simulation = 1
        self.time_interval = []
        self.durations_input(self.random)

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

    def durations_input(self, random):
        if not random:
            for event in self.events:
                try:
                    self.set_of_durations[event] = list(map(float, input("Put the set of durations of the [" + event + "] event : ").split(',')))
                except None or SyntaxError or ValueError:
                    self.durations_input(random)
        if random:
            for event in self.events:
                self.lambdas[event] = []
            print("Enter the parameter Lambda for each event:")
            for event in self.events:
                try:
                    self.lambdas[event].append(float (input("Lambda("+str(event)+") : ")))
                except None or SyntaxError or ValueError or TypeError:
                    print("Invalid input, Try again")
                    self.durations_input(random)
            self.set_of_durations = random_durations_generator(self.events,self.lambdas)
            self.time_interval_input()
            try:
                self.number_of_simulation = int (input("Enter number of simulation you want to do : "))
                while self.number_of_simulation < 0 or self.number_of_simulation == 0:
                    print("Invalid number, try again")
                    self.number_of_simulation = int(input("Enter number of simulation you want to do : "))
            except None or SyntaxError or ValueError or TypeError:
                print("Invalid number, try again")
                self.number_of_simulation = int(input("Enter number of simulation you want to do : "))


    def method_input(self):
        if len(self.lambdas) == 0:
            simple_way_or_other_way = input("Simulate by using calculation (enter y ) or without (enter n): ")
            if simple_way_or_other_way == "y".lower():
                return "hard"
            else:
                return "simple"
        else:
            return "simple"

    def check_durations_input_option(self):
        random_or_not = input("Do you want to generate clocks automatically ( Y/N ) ? : ")
        if random_or_not == "N".casefold():
            self.random = False
        else:
            self.random = True

    def time_interval_input(self):
        try:
            self.time_interval = list(map(int,input("Enter a time interval i.e : 100,200").split(',')))
            while len(self.time_interval) != 2 :
                print("You must enter only two positive integer values, try again")
                self.time_interval = list(map(int, input("Enter a time interval i.e : 100,200")))
        except None or SyntaxError or ValueError or TypeError:
            print("Invalid input")
            self.time_interval_input()

    def print_data(self):
        print(self.states)
        print(self.events)
        print(self.gamma)
        print(self.set_of_durations)