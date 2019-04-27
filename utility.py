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