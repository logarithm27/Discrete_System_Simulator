from InfiniteModel import *
from Model import *
from javascript_generator import *
import datetime

INFINITE = 0
FINITE = 1


class Engine:

    def __init__(self):
        print("1- Simulate finite automaton")
        print("2- Simulate Infinite automaton")
        choice_automaton = input("option 1 or 2 : ")
        x_axes_prob = []
        y_axes_prob = []
        calendar = []
        debits = ""
        date_simulation = datetime.datetime.now()
        plot_title = str(date_simulation.strftime('Timing graph simulation of %d, %b %Y, %X'))
        if int(choice_automaton) == 2:
            model = InfiniteModel()
            calendar = model.calendar
            x_axes_prob = model.x_axis_data
            y_axes_prob = model.y_axis_data
        elif int(choice_automaton) == 1:
            model = Model()
            calendar = model.calendar
            x_axes_prob = model.x_axis_data
            y_axes_prob = model.y_axis_data
        for event in model.debits:
            debits += "N("+str(event)+") = " + str(model.debits[event])+"  |  "

        HTML[6] = HTML[6].replace("DEBITS","Debits : "+ debits)

        calendar_without_collisions = []
        for index, c in enumerate(calendar[:-1]):
            if calendar[index]['date'] == calendar[index + 1]['date']:
                pass
            calendar_without_collisions.append(calendar[index])

        calendar_without_collisions.append(calendar[-1])

        calendar = calendar_without_collisions
        x_axes_states = []
        y_axes_states = []
        probabilities = None
        states = []
        if len(x_axes_prob) == 0  and len(y_axes_prob) == 0:
            HTML[8] = HTML[8].replace("SIMUL", "There's no probabilities chart to show")
        if len(x_axes_prob) > 0  and len(y_axes_prob) > 0:
            if len(model.time_interval) == 0:
                model.time_interval = [calendar[0]['date'],calendar[-1]['date']]
            HTML[8] = HTML[8].replace("SIMUL", "Probabilities of states' activeness in the interval " + str(model.time_interval)+" under " + str(model.number_of_experiences) + " simulation")
            x_axes_to_string_prob = []
            for state in x_axes_prob:
                x_axes_to_string_prob.append("'state = "+str(state)+"'")
            HTML.append("var probabilities = \n")
            probabilities = {
                'x': x_axes_to_string_prob,
                'y': y_axes_prob,
                'type': '|scatter|'
            }
            probabilities = str(probabilities).replace("'", "")
            probabilities = probabilities.replace("|", "'")
            HTML.append(probabilities)
            HTML.append(";\n")
            HTML.append("var data2 = [probabilities];")

        x_axes_date_event_triggering = []
        x_axes_dates = []
        annotations = []
        for element in calendar:
            states.append(element['next_state'])
            x_axes_date_event_triggering.append({element['event']: element['date']})
            x_axes_dates.append(element['date'])
            y_axes_states.append(0)

        for index, element in enumerate(calendar[:-1]):
            if calendar[index]['date'] == 0:
                pass
            x_position = (calendar[index]['date'] + calendar[index + 1]['date']) / 2
            if round(calendar[index + 1]['date'] - calendar[index + 1]['date'], 1) == 0.1:
                x_axes_states.append(round(x_position, 1))
            else:
                x_axes_states.append(round(x_position, 2))
            y_axes_states.append(0)

        x_axes_states.append(round(calendar[-1]['date'] + 0.5, 1))  # the last state

        string_states = []
        for state in states:
            string_states.append("'state = " + str(state) + "'")

        states_positions = {
            'x': x_axes_states,
            'y': y_axes_states,
            'hoverinfo': "|x|",
            'mode': '|text|',
            'name': '|state|',
            'text': string_states,
            'textposition': '|top|',
            'textfont': {
                'family': '|Candara Bold Italic|',
                'size': 20,
                'color': '|#000000|'
            },
            'type': '|scatter|'
        }
        events_positions = {
            'x': x_axes_dates,
            'y': y_axes_states,
            'hoverinfo': "|x|",
            'type': '|scatter|'
        }
        HTML.append("var states_positions = \n")
        states_positions = str(states_positions).replace("'", "")
        states_positions = states_positions.replace("|", "'")
        HTML.append(states_positions)
        HTML.append(";\n")

        HTML.append("var events_positions = \n")
        events_positions = str(events_positions).replace("'", "")
        events_positions = events_positions.replace("|", "'")
        HTML.append(events_positions)
        HTML.append(";\n")

        for element in x_axes_date_event_triggering:
            event = list(element.keys())[0]
            annotations.append(
                {
                    'x': element[event],
                    'y': 1,
                    'xref': "|x|",
                    'yref': "|y|",
                    'text': "|event = " + str(event) + "|",
                    'arrowhead': 3,
                    'arrowcolor': '|#636363|',
                    'ax': 0,
                    'ay': -255,
                    'bordercolor': "|#c7c7c7|",
                    'borderwidth': 2,
                    'bgcolor': "|#f4c9ba|",
                    'textfont': {
                        'family': "|Calibri Italic|",
                        'size': 18,
                        'color': "|#1f77b4|"},
                }
            )
        first_date = str(calendar[1]['date'])
        second_date = str(calendar[2]['date'])
        file = open(str(os.path.dirname(os.path.realpath(__file__))) + "/timing_graph_"+str(datetime.datetime.now()).replace("-","_").replace(":","_")+".html", "w")
        HTML.append("var data = [states_positions,events_positions];\nvar layout = { title:{text:'" + str(
            plot_title) + "',font:{family:'Candara Bold Italic', size:28}, xref: 'paper', x: 0.05,},hovermode: 'x', xaxis: { autorange:false, range: [" + first_date + "," + second_date + "]},yaxis: { autorange: true, showgrid: false, zeroline: false, showline: false, autotick: true, ticks: '', showticklabels: false}, showlegend: false,\n")
        HTML[-1] = HTML[-1] + "annotations:["
        for c in annotations:
            c = str(c).replace("\'", "")
            c = c.replace("|", "'")
            HTML[-1] = HTML[-1] + c + ",\n"
        HTML[-1] = HTML[
                       -1] + "]};\nPlotly.newPlot('timing_graph', data, layout,{displaylogo: false}, {showSendToCloud:true});\n"
        if probabilities is not None:
            HTML[-1] = HTML[-1] + "Plotly.newPlot('probabilities', data2,{displaylogo: false}, {showSendToCloud:true});\n"
        HTML[-1] = HTML[-1] + "function hideLogo() { document.getElementById('symbol').style.visibility = 'hidden';}</script>\n</body>"

        for line in HTML:
            file.write(line)
        file.close()
        file_steps = open(str(os.path.dirname(os.path.realpath(__file__))) + "/steps"+str(datetime.datetime.now()).replace("-","_").replace(":","_")+"txt", "w")
        file_calendar = open(str(os.path.dirname(os.path.realpath(__file__))) + "/calendar" + +str(datetime.datetime.now()).replace("-","_").replace(":","_")+"txt", "w")
        # write the date (help to know the time of program execution )
        file_calendar.write(str(datetime.datetime.now()) + "\n")
        file_steps.write(str(datetime.datetime.now()) + "\n")
        # each element in the steps list represent a step or a line
        for s in model.steps:
            # write steps line by line
            file_steps.write(s)
        file_steps.close()
        for c in calendar:
            file_calendar.write(str(c) + "\n")
        file_calendar.close()

def main():
    engine = Engine()

if __name__ == '__main__':

    main()