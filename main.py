import json

from classes import Swimmer
from functions import get_swim_times, format_swim_time

with open('swim_data.json', 'r') as f:
    swim_dict = json.load(f)

swimmers = [Swimmer(swim_dict[i]["name"]["first"],
                    swim_dict[i]["name"]["last"],
                    swim_dict[i]["grade"],
                    swim_dict[i]["school"],
                    swim_dict[i]["events"])
            for i in swim_dict]

team = []
for sw in swimmers:
    if sw.school == "Harriton":
        team.append(sw)

team.sort(key=lambda s: s.grade, reverse=True)
events = []
for p in team:
    for e in p.events.keys():
        if e not in events:
            events.append(e)

events.sort(key=lambda ev: int(ev.split()[1]))

event_dict = {}
for eve in events:
    times = []
    for sw in team:
        sw_times = get_swim_times(sw.first_name, sw.last_name, eve)
        my_estim_time = sw_times["seconds_estimate"]
        my_best_time = sw_times["seconds_best_time"]
        if my_estim_time and my_best_time:
            times.append(f'({sw.first_name} {sw.last_name}): {my_best_time}')
    times.sort(key=lambda t: float(str(t.split(": ")[1])))

    output_times = []
    for ti in times:
        t_split = ti.split(": ")
        output_times.append(f'{t_split[0]}: {format_swim_time(float(t_split[1]))}')

    event_dict[eve] = output_times

print(json.dumps(event_dict, indent=2, sort_keys=True))
