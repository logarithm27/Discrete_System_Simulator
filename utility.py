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

# sorting the dictionary that contains events and its corresponding dates by dates
# keys are events, t are values
# i.e : { 'a':0.5, 'b':1.5 }
def sort_by_date(dictionary):
    ordered = sorted(dictionary.items(), key = lambda event__date: (event__date[1], event__date[0]))
    dictionary = {}
    for tup in ordered:
        dictionary[tup[0]] = tup[1]
    return dictionary


def asking_for_input_infinite_models():
    ask_for_file = input("Put the file that contains model description : ")
    try:
        with open(ask_for_file) as file:
            contents = file.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
        contents = [line.strip() for line in contents]
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
    typo_error = 27
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
        return typo_error
    return transitions

# this function skip the commentaries that are between the the lines or at the end of the line
def pass_commentaries(string):
    for index,c in enumerate(string[:-1]):
        if string[index].__eq__("/") and string[index+1].__eq__("/") :
            string = string[slice(index)]
            break
    return "".join(string)