


class InfiniteModelInput:
    def __init__(self):
        self.ask_for_file = input("Put the file that contains model description : ")
        self.events = []
        try:
            file = open(self.ask_for_file,"r")
            contents = file.readlines()
            for c in contents:
                if "E" in c or "e" in c:
                    splited_string = c.replace("{","").replace("}","").replace("E","").replace("e","").replace("=","").replace(",","").replace("\n","").replace("[","").replace("]","")
                    for event in splited_string:
                        self.events.append(event)
                print(c)
            print("set of events in that model : " + str(self.events))
            print(len(contents))
        except IOError:
            print("file doesn't exists, try again")

if __name__ == "__main__":
    start = InfiniteModelInput()