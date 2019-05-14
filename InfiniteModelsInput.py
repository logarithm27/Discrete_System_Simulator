from utility import *


class InfiniteModelInput:
    def __init__(self):
        self.contents = asking_for_input_infinite_models()
        is_valid_description = False
        if self.contents:
            is_valid_description = self.check_description_from_file()
        while self.contents is None or not is_valid_description:
            self.contents = asking_for_input_infinite_models()
            is_valid_description = self.check_description_from_file()
        if is_valid_description:
            self.events = self.extracting_data_from_description_file("E")
            self.states = self.extracting_data_from_description_file("X")
            self.state_machine = {}
            self.set_of_durations = self.get_durations()
            self.transitions = self.extracting_data_from_description_file("T")
        print("Events : " + str(self.events))
        print("States : " + str(self.states))
        print("Durations : " + str(self.set_of_durations))
        print("Transition : " + str(self.transitions))

    def check_description_from_file(self):
        # the skeleton of model should contain E for the set of events,
        # X for set of states, and V's (sets of clocks) consistent with the corresponding given E
        # and n for the number of states in the model
        skeleton_of_model = []
        how_many_durations = 0
        for single_content in self.contents:
            if single_content[0] == "#":
                pass
            # data may represents the character 'E' or 'X' or 'n' or 'V(a)' ...
            data = ""
            for single_character in single_content:
                if single_character != "=":
                    data += str(single_character)
                    skeleton_of_model.append(data)
                elif single_character == "=":
                    break
        if not self.invalid_description_error_message():
            return False
        if "V" in skeleton_of_model or "v" in skeleton_of_model:
            for element_of_model in skeleton_of_model:
                if element_of_model.casefold().__eq__("V".casefold()):
                    how_many_durations += 1
            if "E" in skeleton_of_model or "e" in skeleton_of_model:
                if len(self.extracting_data_from_description_file("E")) != how_many_durations:
                    print("Invalid description, you should put the set of clocks that are consistent with the set of events")
                    return False
        return True

    def invalid_description_error_message(self):
        number_of_state = self.extracting_data_from_description_file("N")
        if number_of_state is None:
            print("Invalid description, put number of states of your model and try again")
            return False
        elif not number_of_state is None:
            if number_of_state == 1 or number_of_state == 0:
                print("Invalid number of states, shouldn't be less or equal to 1, try again")
                return False
        if self.extracting_data_from_description_file("X") is None:
            print("Invalid description, put the set states X of your model and try again")
            return False
        if self.extracting_data_from_description_file("E") is None:
            print("Invalid description, put the set of events of your model and try again")
            return False
        if self.extracting_data_from_description_file("V") is None:
            print("Invalid description, enter the set of clocks 'V' and try again")
            return False
        if self.extracting_data_from_description_file("T") is None:
            print("Invalid description, enter the set Transitions and try again")
            return False
        if self.get_durations() is None:
            return False
        return True

    def extracting_data_from_description_file(self, character):
        data = []
        invalid_characters = [',','-','_','/','.','~']
        for single_content in self.contents:
            if single_content[0].casefold().__eq__(character.casefold()):
                split_string = single_content.replace("{","").replace("}","").replace(character,"").replace(character.lower(),"").replace("=","").replace("[","").replace("]","").replace(" ","")
                if character.casefold() == "X".casefold():
                    data = replacing_delimiter(split_string, ",", ";")
                    for tup in data:
                        if tup.__eq__('..') or tup.__eq__('...'):
                            data.remove(tup)
                    for index,tup in enumerate(data):
                        data[index] = transform_to_tuple(data[index])
                elif character.casefold().__eq__("T".casefold()):
                    return from_string_to_dict_transitions(split_string,self.extracting_data_from_description_file("E"))
                else:
                    data = split_string.split(",")
            if character.casefold().__eq__("N".casefold()) and data  and single_content[0].__eq__(character.casefold()):
                number = ""
                for char in data:
                    number += str(char)
                for invalid_character in invalid_characters:
                    if invalid_character in number:
                        print("You've put an invalid number to represent the number of states, fix it and try again")
                        return None
                return int (number)
        if data:
            return data
        return None

    def get_durations(self):
        durations = {}
        for single_content in self.contents:
            if "V" in single_content or "v" in single_content:
                split_string = ""
                for element in single_content:
                    if element != "=":
                        split_string += str(element)
                if split_string[2] not in self.extracting_data_from_description_file("E"):
                    print("can't handle V("+ split_string[2] +"), the following event {"+split_string[2]+"} doesn't exist, fix it and try again")
                    return None
                elif split_string[2] in self.extracting_data_from_description_file("E"):
                    clocks = split_string[4::].replace(";",",").replace("-",",").replace("~",",").replace(" ",',').replace("\n","").split(',')
                    try:
                        durations[split_string[2]] = list(map(float,clocks))
                    except None or SyntaxError or ValueError:
                        print("Invalid list of clocks, try again")
                        return None
        return durations


if __name__ == "__main__":
    start = InfiniteModelInput()