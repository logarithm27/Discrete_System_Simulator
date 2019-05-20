from utility import *
MAX_DIMENSION = 3
MAX_N = 15
INVALID_MAX_N_ERROR = [-2,-1,0,1]
INVALID_NUMBER_EXPERIENCE_ERROR = -100


class InfiniteModelInput:
    def __init__(self):
        self.contents = asking_for_input_infinite_models()
        self.number_of_states = MAX_N
        is_valid_description = False
        if self.contents:
            is_valid_description = self.check_description_from_file()
        while self.contents is None or not is_valid_description:
            self.contents = asking_for_input_infinite_models()
            is_valid_description = self.check_description_from_file()
        if is_valid_description:
            self.events = sorted(list(dict.fromkeys(self.extracting_data_from_description_file("E"))))
            self.states = sorted(list(dict.fromkeys(self.extracting_data_from_description_file("X"))))
            self.state_machine = {}
            self.lambdas = self.get_lambda()
            self.events_description = self.extracting_data_from_description_file("D")
            self.number_of_states = self.max_n_number_checker()
            self.max_bounds = self.get_bounds("max")
            self.min_bounds = self.get_bounds("min")
            if self.number_of_states in INVALID_MAX_N_ERROR:
                self.number_of_states = MAX_N

    def check_description_from_file(self):
        # the skeleton of model should contain E for the set of events,
        # X for set of states, and V's (sets of clocks) consistent with the corresponding given E
        # and n for the number of states in the model
        skeleton_of_model = []
        how_many_durations = 0
        for single_content in self.contents:
            if single_content[0] == "/" and single_content[1]=="/":
                pass
            # data may represents the character 'E' or 'X' or 'n' or 'V(a)' ...
            data = ""
            data += str(single_content[0])
        if not self.invalid_description_error_message():
            return False
        if "L" in skeleton_of_model or "l" in skeleton_of_model:
            for element_of_model in skeleton_of_model:
                if element_of_model.casefold().__eq__("L".casefold()):
                    how_many_durations += 1
            if "E" in skeleton_of_model or "e" in skeleton_of_model:
                if len(self.extracting_data_from_description_file("E")) != how_many_durations:
                    print("Invalid description, you should put the set of clocks that are consistent with the set of events")
                    return False
        return True

    def invalid_description_error_message(self):
        if self.extracting_data_from_description_file("X") is None:
            print("Invalid description, put the set states X of your model and try again")
            return False
        if self.extracting_data_from_description_file("E") is None:
            print("Invalid description, put the set of events of your model and try again")
            return False
        if self.extracting_data_from_description_file("L") is None:
            print("Invalid description, lambdas")
            return False
        if self.extracting_data_from_description_file("D") is None:
            print("Invalid description, enter the set of events descriptions and try again")
            return False
        if self.extracting_data_from_description_file("D") is TYPO_ERROR:
            print("Your set of transition is invalid, maybe a typo error in your file, fix it and try again")
            return False
        # if self.get_lambda() is None:
        #     return False
        if self.get_bounds("max") is None:
            print("Put the maximum bounds and try again")
            return False
        if self.get_bounds("min") is None:
            print("Put the maximum bounds and try again")
            return False
        return True

    def extracting_data_from_description_file(self, character):
        data = []
        for single_content in self.contents:
            if single_content[0].casefold().__eq__(character.casefold()):
                single_content = single_content.strip(single_content[0])
                split_string = pass_commentaries(single_content.replace("{","").replace("}","").replace("=","").replace("[","").replace("]","").replace(" ",""))
                if character.casefold() == "X".casefold():
                    data = replacing_delimiter(split_string, ",", ";")
                    for tup in data:
                        if tup.__eq__('..') or tup.__eq__('...'):
                            data.remove(tup)
                    for index,tup in enumerate(data):
                        data[index] = transform_to_tuple(data[index])
                        if data[index] is None:
                            return None
                    if not check_dimension_consistency(data) or len(data[0]) > MAX_DIMENSION:
                        print("all states should be under the same dimension, and cannot exceed 3 Dimensions, fix it and try again")
                        return None
                elif character.casefold().__eq__("D".casefold()):
                    descriptions = from_string_to_dict_transitions(split_string,self.extracting_data_from_description_file("E"))
                    if descriptions is not None :
                        for description in descriptions:
                            if len(descriptions[description]) > MAX_DIMENSION or len(descriptions[description]) == 0 or len(self.extracting_data_from_description_file("X")[0]) != len(descriptions[description]):
                                print("Inconsistent dimensions between states in the set of events description 'D' and the set of states 'X' ")
                                return None
                    return descriptions
                else:
                    data = split_string.split(",")
        if data:
            return data
        return None

    def max_n_number_checker(self):
        for single_content in self.contents:
            if single_content[0].casefold().__eq__("N".casefold()):
                split_string = pass_commentaries(single_content.replace("{","").replace("}","").replace("N","").replace("N".lower(),"").replace("=","").replace("[","").replace("]","").replace(" ",""))
                try:
                    return int (split_string)
                except ValueError or SyntaxError or TypeError:
                    print("Invalid Maximum Number, the number will be set to "+ str(MAX_N) +" by default")
                    return -1
        return -2

    def get_bounds(self, max_or_min):
        for single_content in self.contents:
            if single_content[0].casefold().__eq__(max_or_min[0].casefold()) and single_content[1].casefold().__eq__(max_or_min[1].casefold()) and single_content[2].casefold().__eq__(max_or_min[2].casefold()):
                split_string = pass_commentaries(single_content.replace("{","").replace("}","").replace(max_or_min+"_bounds","").replace(max_or_min.upper()+"_BOUNDS","").replace("=","").replace("[","").replace("]","").replace(" ","").replace("(","").replace(")",""))
                bound = split_string.split(",")
                for index, coordinate in enumerate(bound):
                    if coordinate == "N":
                        max_num = self.max_n_number_checker() # check if the user have put N in description file
                        if max_num not in INVALID_MAX_N_ERROR:
                            bound[index] = str(max_num)
                        else:
                            bound[index] = str(MAX_N)
                try:
                    bound = tuple(map(int,bound))
                except ValueError or SyntaxError or TypeError:
                    print("Invalid description, put the "+ max_or_min+ " bounds properly and try again")
                    return None
                if len(bound) > MAX_DIMENSION and len(bound) != len(self.extracting_data_from_description_file("X")[0]):
                    print("Inconsistent dimensions in maximum bounds, try again")
                    return None
                else:
                    return bound
        return None


    def get_lambda(self):
        durations = {}
        for single_content in self.contents:
            if "L".casefold() == single_content[0].casefold() and (single_content[1].__eq__("(") or single_content[1].__eq__("[")):
                split_string = ""
                for element in single_content:
                    if element != "=":
                        split_string += str(element)
                if split_string[2] not in self.extracting_data_from_description_file("E"):
                    print("can't handle l("+ split_string[2] +"), the following event {"+split_string[2]+"} doesn't exist, fix it and try again")
                    return None
                elif split_string[2] in self.extracting_data_from_description_file("E"):
                    clocks = split_string[4::].replace(";",",").replace("-",",").replace("~",",").replace(" ",'').replace("\n","").replace("{","").replace("}","").replace("[","").replace("]","")
                    clocks = pass_commentaries(clocks).split(",")
                    try:
                        durations[split_string[2]] = list(map(float,clocks))
                    except None or SyntaxError or ValueError:
                        print("Invalid rate, try again")
                        return None
        return durations


    def get_number_of_experience(self):
        for single_content in self.contents:
            if "M".casefold() == single_content[0] and single_content[1] == "=":
                split_string = pass_commentaries(single_content.replace("{","").replace("}","").replace("M","").replace("M".lower(),"").replace("=","").replace("[","").replace("]","").replace(" ",""))
                try:
                    return int (split_string)
                except ValueError or TypeError or SyntaxError:
                    print("Invalid number of experiences, must be an integer, try again")

if __name__ == "__main__":
    start = InfiniteModelInput()