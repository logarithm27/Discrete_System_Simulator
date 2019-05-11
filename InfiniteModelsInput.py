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
        # X for states, and V's (set of clocks) consistent with the corresponding given E
        # and n for the number of states in the model
        skeleton_of_model = []
        for single_content in self.contents:
            if "#" in single_content:
                pass
            skeleton_of_model.append(single_content.pop(0))
        

    def extracting_description_from_file(self):
        for single_content in self.contents:
            if "E" in single_content or "e" in single_content:
                split_string = single_content.replace("{","").replace("}","").replace("E","").replace("e","").replace("=","").replace(",","").replace("\n","").replace("[","").replace("]","")
                for event in split_string:
                    self.events.append(event)

if __name__ == "__main__":
    start = InfiniteModelInput()