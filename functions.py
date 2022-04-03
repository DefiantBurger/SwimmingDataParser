import json
from copy import copy

from classes import Swimmer


def remove_prefixes(text: str, prefix: str):
    while text.startswith(prefix):
        text = text.removeprefix(prefix)
    return text


def remove_suffixes(text: str, suffix: str):
    while text.endswith(suffix):
        text = text.removesuffix(suffix)
    return text


def remove_consecutive_duplicates(s):
    if len(s) < 2:
        return s
    if s[0] != s[1]:
        return s[0] + remove_consecutive_duplicates(s[1:])
    return remove_consecutive_duplicates(s[1:])


with open('swim_data.json', 'r') as f:
    swim_dict = json.load(f)

swimmers = [Swimmer(swim_dict[i]["name"]["first"],
                    swim_dict[i]["name"]["last"],
                    swim_dict[i]["grade"],
                    swim_dict[i]["school"],
                    swim_dict[i]["events"])
            for i in swim_dict]

swimmers.sort(key=lambda s: s.last_name)


def get_swim_times(first_name, last_name, event):
    to_return = {}
    for sw in swimmers:
        if sw.first_name == first_name and sw.last_name == last_name:
            events = sw.events

            if event not in events:
                return {"formatted_times": None,
                        "seconds_times": None,
                        "average_change": None,
                        "formatted_estimate": None,
                        "seconds_estimate": None,
                        "seconds_best_time": None}

            times = events[event]
            to_return["formatted_times"] = copy(times)
            while "DQ" in times:
                times.remove("DQ")

            if len(times) < 1:
                return {"formatted_times": None,
                        "seconds_times": None,
                        "average_change": None,
                        "formatted_estimate": None,
                        "seconds_estimate": None,
                        "seconds_best_time": None}

            for i in range(len(times)):
                time_split = str(times[i]).split(":")
                try:
                    times[i] = sum(
                        [float(time_split[t]) * (60 ** (len(time_split) - t - 1)) for t in range(len(time_split))])
                except ValueError:
                    times[i] = sum(
                        [float(time_split[t].replace("J", "")) * (60 ** (len(time_split) - t - 1)) for t in
                         range(len(time_split))])
            to_return["seconds_times"] = times
            diff = 0

            for i in range(len(times) - 1):
                diff += times[i + 1] - times[i]
            try:
                diff /= len(times) - 1
            except ZeroDivisionError:
                diff = 0

            minutes = int((times[-1] + diff) // 60)
            seconds = round((times[-1] + diff) % 60, 2)
            to_return["average_change"] = diff
            to_return["formatted_estimate"] = \
                f'{minutes}:{"0" * (2 - int(len(str(seconds).split(".")[0]))) + str(seconds)}'
            to_return["seconds_estimate"] = round((times[-1] + diff), 2)
            to_return["seconds_best_time"] = min(times)

            return to_return


def format_swim_time(seconds):
    if seconds // 60 >= 1:
        return f'{int(seconds // 60)}:' \
               f'{"0" * (2 - int(len(str(round(seconds % 60, 2)).split(".")[0]))) + str(round(seconds % 60, 2))}'
    else:
        return f'{"0" * (2 - int(len(str(round(seconds % 60, 2)).split(".")[0]))) + str(round(seconds % 60, 2))}'
