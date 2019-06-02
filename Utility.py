# Utility class offers a number of functions
# each function has it's own task and runs a particular algorithm useful in another class
import datetime
import os
import random
import math
MAX_DIMENSION = 3
TYPO_ERROR = 27
NON_RANDOM = 0
RANDOM = 1

# this function is responsible for asking the user to enter the necessary input
# it's useful for FINITE MODEL'S SIMULATION ONLY
# because we're asking the user to give multiple information about the model he wants to simulate
# we'll call this function multiple times in the Model class,
# hence, instead of repeating the code, we'll use this function with two parameters
# the first parameter is the string message which should be displayed to ask the user of the number of states or the number of events in his model
# the second parameter asks the user to enter the enter the data related to the model, i.e : enter the names of the events, or the name of states
# note that because we're asking the user of the number of states and events, we're about simulating a FINITE AUTOMATON, the input of the Infinite systems
# is on the InfiniteModelsInput Class

def asking_for_input(ask_for_number_of_data, ask_for_data):
    # Handling particular exceptions that may occurs if the user enters an invalid input
    try:
        # ask the user to put the number of states or events and convert it to an integer because it's a number
        number_of_data = int(input(ask_for_number_of_data))
        # because we use this function multiple times depending on the type of data we're asking the user to put,
        # we check if we're asking the user about the states or events
        # so if we're asking about the number of states in the user's model
        if "states" in ask_for_number_of_data:
            # if the number of states entered previously by the user is less than or equal to 1
            while number_of_data <= 1:
                # we ask the user to put a valid number over and over again until he enter a valid number of states
                # for example : we can't have an automaton with one state (maybe we can but it's useless)
                print("invalid model, try again")
                number_of_data = int(input(ask_for_number_of_data))
        # if we're asking the user about the events
        if "events" in ask_for_number_of_data:
            # if the user has entered a number of events that equal to 0
            while number_of_data == 0:
                # we ask again until he enter a valid number
                # automaton with 0 event seems to be useless
                print("invalid model, try again")
                number_of_data = int(input(ask_for_number_of_data))
        # data is a variable that represents the user's input after providing the number of data, it may be states or  events
        # data is converted to a list, i.e : if the user provides 3 as number of states, then data will hold 3 elements ( if of course the user puts consistent input )
        # sorting the input in natural order, then convert the input to a list, then remove duplicate values ( because an automaton has unique states and unique events)
        data = sorted(list(dict.fromkeys(input(ask_for_data).split(','))))
        # check if the user have a consistent input
        # i.e : if the given number of events was 3 (a,b,c) and the user has provided only two events (a,b), or the user
        # has provided an empty string by hitting enter
        # then the statement below is true
        while len(data) < number_of_data or len(data) > number_of_data or "" in data or " " in data:
            # as we do every time, we ask for a valid input while the user's provided a wrong input
            print('invalid input, try again')
            data = sorted(list(dict.fromkeys(input(ask_for_data).split(','))))
    # catch the eventual exception that we may encounter ( ValueError exception for eventual non integer input in when asking for number of data )
    # i.e : the user gave a comma ',', the program tries to cast it into an integer, it will fails and rise a ValueError Exception
    except None or ValueError or SyntaxError:
        print('invalid input, try again')
        return None
    # return the data (list of states or events ) to the calling function
    return data

# sorting the dictionary that contains events and its corresponding dates by dates
# keys are events, dates are values
# i.e : { 'a':0.5, 'b':1.5 }
def sort_by_date(dictionary):
    ordered = sorted(dictionary.items(), key = lambda event__date: (event__date[1], event__date[0]))
    dictionary = {}
    for tup in ordered:
        dictionary[tup[0]] = tup[1]
    return dictionary


# this is the function that helps us
def asking_for_input_infinite_models():
    ask_for_file = input("Put the file that contains model description : ")
    try:
        with open(ask_for_file) as file:
            contents = file.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
        contents = [line for line in contents if line]
        for single_content in contents:
            if len(single_content.strip()) == 0: # skip the empty lines
                contents.remove(single_content)
        return contents
    except IOError:
        print("file doesn't exists, try again")
        return None

# replacing a specific character by another inside a given string to make the process of making a list easier
def replacing_delimiter(string, current_char, new_char):
    string = list(string)
    for index, char in enumerate(string[:-1]):
        if char == current_char and (string[index+1] == "(" or string[index-1] == ")" or string[index+1] == "."):
            string[index]= new_char
    return "".join(string).split(new_char)

def transform_to_tuple(string):
    try:
       return tuple(map(int,string.replace("(","").replace(")","").split(',')))
    except ValueError or SyntaxError:
        print("Can't handle states, fix it and try again")
        return None

# this function allow to transform the string that contains transitions to a dictionary
# the keys are the events, the values are the points i.e : to make the event b possible, we should add (x',y') to the source state (x,y)
def from_string_to_dict_transitions(split_string,events):
    transitions= {}
    try:
        string = list(split_string)
        for index, char in enumerate(string[:-1]):
            if char == "," and (string[index - 1] in events):
                string[index]= ":"
        string = "".join(string)
        string = replacing_delimiter(string, ",", ";")
        for index,c in enumerate(string):
            string[index] = c.split(":")
        for c in string:
            if c[0] in events:
                transitions[c[0]]= transform_to_tuple(c[1])
            elif c[0] not in events:
                return 27
    except None or Exception or IndexError:
        return TYPO_ERROR
    return transitions

# this function skip the commentaries that are between the the lines or at the end of the line
def pass_commentaries(string):
    for index,c in enumerate(string[:-1]):
        if string[index].__eq__("/") and string[index+1].__eq__("/") :
            string = string[slice(index)]
            break
    return "".join(string)

def check_dimension_consistency(states):
    len_state_tuple = len(states[0])
    for state in states:
        if len(state) != len_state_tuple:
            return False
    return True

def tuple_sum(tuple_1, tuple_2):
    next_state = []
    for index, coordinate in enumerate(tuple_1):
        next_state.append(tuple_1[index]+ tuple_2[index])
    return tuple(map(int,next_state))

def check_valid_state(min_bound, max_bound, tuple_to_check):
    for index, point in enumerate(tuple_to_check):
        if tuple_to_check[index] < min_bound[index] or tuple_to_check[index] > max_bound[index]:
            return False
    return True

def set_of_possible_events_of_all_states(states, transitions):
    # gamma is a dictionary : keys are states, and values are possible events that can go in or out that corresponding state
    gamma = {}
    for state in states:
        # each state has a list of events
        gamma[state] = []
    for transition in transitions:
        # adding events that can go from the state
        gamma[transition['source']].append(transition['event'])
        # adding events that can left or goes into the state
        # gamma[transition['destination']].append(transition['event'])
    for state in gamma:
        # removing duplicate events added in the list, so we can have a list of unique events that can be triggered from the
        # corresponded state
        gamma[state] = sorted(list(dict.fromkeys(gamma[state])))  # remove duplicates
    return gamma

def next_state(current_state, next_event, transitions):
    for transition in transitions:
        if transition['event'] == next_event and transition['source'] == current_state:
            return transition['destination']

def still_active(event, state, gamma):
    return event in gamma[state]


def random_durations_generator(events, lambdas):
    durations = {}
    for event in events:
        durations[event] = []
    for event in events:
        v = -(1/lambdas[event][0])* math.log(1-random.uniform(0,1))
        durations[event].append(round(v,1))
    return durations

def still_more_clocks(duration, random_or_not, date, limit_time):
    if random_or_not == NON_RANDOM:
        for event in duration:
            if duration[event]:
                return True
    if random_or_not == RANDOM:
        if date < limit_time:
            return True
    return False

def replace(string, characters):
    while characters:
        string = string.replace(characters.pop(0),"")
    return pass_commentaries(string)

def get_event_from_lambdas(line_string):
    event =""
    for i, c1 in enumerate(list(line_string)):
        if c1=="(":
            for j,c2 in enumerate(list(line_string)[i+1::]):
                if c2 == ")":
                    break
                event+=c2
    return event

def get_value_from_lambdas(line_string):
    event =""
    for i, c1 in enumerate(list(line_string)):
        if c1==")":
            for j,c2 in enumerate(list(line_string)[i+1::]):
                event+=c2
    return event

def check_consistent_events(event, list_of_events):
    for single_event in list_of_events:
        if single_event == event:
            return True
    return False


def analysis(simulator_calendar, time_interval, debits, sigma_debits, sigma_probabilities, state_probabilities):
    # each time we simulate, we get the calendar generated after the simulation
            calendar = simulator_calendar
            for index,c in enumerate(calendar[:-1]):
                # if the date that corresponds to the activation of an event is between the given date interval
                if time_interval[0] < c['date'] < time_interval[1]:
                    # increment the occurrence counter
                    debits[c['event']] += 1
                # -------calculating probabilities of each state being active in the given interval--------
                # initialize the variable that will be used to calculate the time interval where each state is active
                interval_state_active = 0
                # if the state is active between an interval ot time that began with a value less than the minimum value
                # or the minimum bound given in the interval ot time and a value less than or equal to the maximum bound or value in the time interval
                if calendar[index]['date'] <= time_interval[0] < calendar[index + 1]['date'] <= time_interval[1]:
                    # the state is active between [ the minimum value given in the time interval - the date when the state is no longer active ]
                    interval_state_active = calendar[index + 1]['date'] - time_interval[0]
                # if the state is active between the given time interval
                if time_interval[0]<= calendar[index]['date'] < calendar[index +1]['date'] <= time_interval[1]:
                    interval_state_active = calendar[index + 1]['date'] - calendar[index]['date']
                # if the state is active between a date greater than the minimum bound or value and a value that's greater
                # than the maximum bound of the given time interval
                if time_interval[0] <= calendar[index]['date'] <= time_interval[1] < calendar[index + 1]['date']:
                    # state is active on [ the start date when the state is being active - maximum bound ]
                    interval_state_active = time_interval[1] - calendar[index]['date']
                # each state has it's own probability, each time we face that state, with add the corresponding interval time of being active
                # we add that date as long as we're going until the end of the simulation
                # this is not the real probability for now, it will be calculated later, for now we're using the same variable for adding the dates
                state_probabilities[c['next_state']] += interval_state_active
            # after collecting data and counting the probabilities of state activity status
            for state in state_probabilities:
                # we now calculate the probabilities, by dividing each value calculated previously ( sum intervals where each state was active ) by the
                # subtracting the max bound by the min bound
                state_probabilities[state] = state_probabilities[state]/(time_interval[1] - time_interval[0])
                # for statistical use, as long as we go through the number of simulation, we add the calculated probability
                # i.e : we have 100 simulation, the sigma ( sum of probabilities ) will be the sum of probabilities 100 times
                # note that each state has it's own probability
                sigma_probabilities[state] += state_probabilities[state]
            # still inside the simulation, iterating through calculated occurrence of each event
            for event in debits:
                # calculate the debit by dividing number of occurrence of each event by T2 - T1
                debits[event] = debits[event] / (time_interval[1] - time_interval[0])
                # while we're inside the main loop ( number of experiences, simulations ) we add the calculated debit
                # that corresponds to a particular event to the new one ( we build a sum of debits for each event)
                sigma_debits[event] += debits[event]
            return debits, sigma_debits,sigma_probabilities, state_probabilities

# by the end of all simulations
def analysis_output(debits, sigma_debits, sigma_probabilities, state_probabilities, time_interval, number_of_experiences):
    for state in sigma_probabilities:
        # we calculate the final probability of each state by dividing the sigma by the number of simulations
        state_probabilities[state] = round((sigma_probabilities[state] / number_of_experiences), 4)
    # by the end the simulations
    for single_sigma_debit in sigma_debits:
        # dividing the sum of debits of each event by the number of experiences to get a new debit
        debits[single_sigma_debit] = round(sigma_debits[single_sigma_debit] / number_of_experiences, 3)
    # get current directory path and write a file of the name probability.txt to show the calculated probabilities
    file_output = open(str(os.path.dirname(os.path.realpath(__file__))) + "/probability.txt", "w")
    file_output.write(str(datetime.datetime.now()) + "\n" + "P[ T1 < t < T2] (State X) = Probability" + "\n")
    # initializing this list that represent the x_axis of the chart ( x axis will holds the set of states )
    x_axis_data = []
    # each state has it's own probability, and this probability will be held by the y axis
    y_axis_data = []
    # showing the probabilities in two different ways :
    # first way : display it in a nice graphical chart by generating an html file
    # second way : write probabilities in an output file
    for state in state_probabilities:
        # add each state to the x axis
        x_axis_data.append(state)
        # add the corresponding probability of that state to the y axis
        y_axis_data.append(state_probabilities[state])
        # write the probabilities on the probability.txt output file
        file_output.write(
            "P[" + str(time_interval[0]) + " < t < " + str(time_interval[1]) + "] (" + str(state) + ") = " + str(
                state_probabilities[state]) + "\n")
    return debits, sigma_debits, sigma_probabilities, state_probabilities, x_axis_data,y_axis_data