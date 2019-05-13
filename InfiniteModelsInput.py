from utility import asking_for_input_infinite_models


class InfiniteModelInput:
    def __init__(self):
        self.contents = asking_for_input_infinite_models()
        is_valid_description = self.check_description_from_file()
        while self.contents is None or not is_valid_description:
            self.contents = asking_for_input_infinite_models()
        if is_valid_description:
            self.events = self.extracting_data_from_description_file("E")
            self.states = self.extracting_data_from_description_file("X")
            self.state_machine = {}
            self.set_of_durations = self.extracting_data_from_description_file("V")
        print("Events : " + str(self.events))
        print("States : " + str(self.states))

    def check_description_from_file(self):
        # the skeleton of model should contain E for the set of events,
        # X for set of states, and V's (sets of clocks) consistent with the corresponding given E
        # and n for the number of states in the model
        skeleton_of_model = []
        how_many_durations = 0
        for single_content in self.contents:
            if "#" in single_content:
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
        return True

    def extracting_data_from_description_file(self, character):
        data = []
        invalid_characters = [',','-','_','/','.','~']
        split_string = ""
        for single_content in self.contents:
            if character.casefold() in single_content.casefold():
                if character.casefold().__eq__("V".casefold()):
                    for element in single_content:
                        if element != "=":
                            split_string += str(element)
                split_string = single_content.replace("{","").replace("}","").replace(character,"").replace(character.lower(),"").replace("=","").replace(",","").replace("\n","").replace("[","").replace("]","")
                for v in split_string:
                    data.append(v)
        if character.casefold().__eq__("N".casefold()) and data:
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



if __name__ == "__main__":
    start = InfiniteModelInput()