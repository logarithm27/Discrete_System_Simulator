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
        how_many_durations = []
        for single_content in self.contents:
            if "#" in single_content:
                pass
            # data may represents the character 'E' or 'X' or 'n' or 'V(a)' ...
            data = ""
            for single_character in single_content:
                if single_character != "=":
                    data += single_character
                    skeleton_of_model.append(data)
                elif single_character == "=":
                    break
        if "X" not in skeleton_of_model or "x" not in skeleton_of_model:
            print("Invalid description, put states of your model and try again")
        if "E" not in skeleton_of_model or "e" not in skeleton_of_model:
            print("Invalid description, put events of your model and try again")


    def extracting_description_from_file(self):
        for single_content in self.contents:
            if "E".casefold() in single_content.casefold():
                split_string = single_content.replace("{","").replace("}","").replace("E","").replace("e","").replace("=","").replace(",","").replace("\n","").replace("[","").replace("]","")
                for event in split_string:
                    self.events.append(event)

if __name__ == "__main__":
    start = InfiniteModelInput()