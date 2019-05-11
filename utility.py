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
        return contents
    except IOError:
        print("file doesn't exists, try again")
        return None