from utility import asking_for_input_infinite_models


class InfiniteModelInput:
    def __init__(self):
        self.contents = asking_for_input_infinite_models()
        while self.contents is None:
            self.contents = asking_for_input_infinite_models()
        self.events = []
        self.states = []
        self.state_machine = {}
        self.set_of_durations = {}

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

        if "V" in skeleton_of_model or "v" in skeleton_of_model:
            for element_of_model in skeleton_of_model:
                if element_of_model.casefold().__eq__("V".casefold()):
                    how_many_durations += 1
            if "E" in skeleton_of_model or "e" in skeleton_of_model:
                if len(self.extracting_data_from_description_file("E")) != how_many_durations:
                    print("Invalid description, you should put the set of clocks that are consistent with the set of events")


    def extracting_data_from_description_file(self, character):
        data = []
        for single_content in self.contents:
            if character.casefold() in single_content.casefold():
                split_string = single_content.replace("{","").replace("}","").replace(character,"").replace(character.lower(),"").replace("=","").replace(",","").replace("\n","").replace("[","").replace("]","")
                for event in split_string:
                    data.append(event)
        if data:
            return data
        return None

    def invalid_description_error_message(self):
        if self.extracting_data_from_description_file("N").__eq__(None):
            print("Invalid description, put states of your model and try again")
        if self.extracting_data_from_description_file("X").__eq__(None):
            print("Invalid description, put states of your model and try again")
        if self.extracting_data_from_description_file("E").__eq__(None):
            print("Invalid description, put events of your model and try again")


if __name__ == "__main__":
    start = InfiniteModelInput()