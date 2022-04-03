import datetime
import json
import os
import shutil
import time

import requests
from bs4 import BeautifulSoup

from classes import Swimmer
from functions import remove_prefixes, remove_suffixes

url = "http://www.fordswimdive.com/clswimdive.html"
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')


def request_data(years: list[int]):
    shutil.rmtree('data')
    os.mkdir('data')

    teams = ["HAV", "CON", "MN", "GAV", "LME", "HAR", "PNC", "UDA", "RAD", "SH", "RID", "SDC"]
    urls = []
    years = [str(y) for y in years]
    for year in years:
        for team1 in teams:
            for team2 in teams:
                req = requests.get(f'http://www.fordswimdive.com/CentralLeague/{year} Results/{team1}v{team2}.htm')
                if req.status_code == 200:
                    print(f"{year} {team1}v{team2} -> {req.url}")
                    urls.append(req.url)
                else:
                    print(f"{year} {team1}v{team2} -> Not Found")

    for u in urls:
        full_start = time.time()
        req_start = time.time()
        meet_req = requests.get(u)
        print(f"Connected to {meet_req.url} in {round((time.time() - req_start) * 1000, 3)}ms...")
        write_start = time.time()
        meet_soup = BeautifulSoup(meet_req.text, 'html.parser')
        meet_text = remove_prefixes(meet_soup.get_text(), "\n")
        meet_text = remove_suffixes(meet_text, "\n")
        meet_text = meet_text.replace("Garnet Valley", "Garnet_Valley")
        meet_text = meet_text.replace("Upper Darby", "Upper_Darby")
        meet_text = meet_text.replace("Lower Merion", "Lower_Merion")
        meet_text = meet_text.replace("Strath Haven", "Strath_Haven")
        meet_text = meet_text.replace("Marple Newtown", "Marple_Newtown")

        meet_text = meet_text.replace("CON", "Conestoga")
        meet_text = meet_text.replace("RAD", "Radnor")
        meet_text = meet_text.replace("GAV", "Garnet_Valley")
        meet_text = meet_text.replace("HAR", "Harriton")
        meet_text = meet_text.replace("HAV", "Haverford")
        meet_text = meet_text.replace("UDA", "Upper_Darby")
        meet_text = meet_text.replace("LME", "Lower_Merion")
        meet_text = meet_text.replace("SH", "Strath_Haven")
        meet_text = meet_text.replace("MN", "Marple_Newtown")
        meet_text = meet_text.replace("SDC", "Springfield")
        meet_text = meet_text.replace("RID", "Ridley")
        meet_text = meet_text.replace("PNC", "Penncrest")

        meet_text = meet_text.replace("Conestoga-MA", "Conestoga")
        meet_text = meet_text.replace("Radnor-MA", "Radnor")
        meet_text = meet_text.replace("Harriton-MA", "Harriton")
        meet_text = meet_text.replace("Garnet_Valley-MA", "Garnet_Valley")
        meet_text = meet_text.replace("Haverford-MA", "Haverford")
        meet_text = meet_text.replace("Upper_Darby-MA", "Upper_Darby")
        meet_text = meet_text.replace("Lower_Merion-MA", "Lower_Merion")
        meet_text = meet_text.replace("Strath_Haven-MA", "Strath_Haven")
        meet_text = meet_text.replace("Marple_Newtown-MA", "Marple_Newtown")
        meet_text = meet_text.replace("Springfield-MA", "Springfield")
        meet_text = meet_text.replace("Ridley-MA", "Ridley")
        meet_text = meet_text.replace("Penncrest-MA", "Penncrest")

        meet_text = meet_text.replace("Women", "Girls")
        meet_text = meet_text.replace("Men", "Boys")

        meet_text = meet_text.replace("-US", "")

        meet_lines = meet_text.split("\n")
        if "AM" in meet_lines[0]:
            meet_date = meet_lines[1].split()[-1]
        elif "PM" in meet_lines[0]:
            meet_date = meet_lines[1].split()[-1]
        else:
            meet_date = meet_lines[0].split()[-1]
        try:
            full_date = str(datetime.datetime.strptime(meet_date, "%m/%d/%Y")).split()[0]
        except ValueError:
            print("Date unknown: skipping file...")
            print()
            continue

        split_meet_text = meet_text.split("\n")
        if split_meet_text[0].startswith("Licensed"):
            split_meet_text.pop(0)
        meet_text = "\n".join(split_meet_text)

        with open(f'data/{full_date}.{u.split("/")[-1].removesuffix(".htm")}.txt', 'w') as f:
            f.write(meet_text)
        print(
            f"Wrote to data from {meet_req.url} to disk in {round((time.time() - write_start) * 1000, 3)}ms...")
        print(f"Total data gathering took {round((time.time() - full_start) * 1000, 3)} ms.")
        print()


def sort_data():
    swimmers = []

    files = []
    for filename in os.listdir('data'):
        files.append(filename)
    files.sort()

    for filename in files:
        print(f'Sorting file {filename}...')

        with open(f'data/{filename}', 'r') as f:
            full_text = f.read()
            all_events = full_text.split("\n \n")
            all_events.pop(0)
            all_events.pop(-1)
            all_events.pop(-1)
            all_events.pop(-1)
            all_events.pop(-1)

        for ae in all_events:
            full_event = ae.split("===============================================================================")
            event_name = full_event[0].removesuffix("\n")
            event_results = full_event[2].removeprefix("\n")
            if "Relay" not in event_name and "Diving" not in event_name:
                all_placements = event_results.split("\n")
                for ap in all_placements:
                    placement = ap.split()

                    if len(placement) == 0 or placement[0] == "--" or not placement[0].isdigit():
                        continue

                    if not placement[1][-1] == ",":
                        placement[1] = placement[1] + " " + placement[2]
                        placement.pop(2)

                    try:
                        try:
                            person = Swimmer(placement[2], placement[1].removesuffix(","), int(placement[3]),
                                             placement[4])
                        except ValueError:
                            person = Swimmer(placement[2], placement[1].removesuffix(","), int(placement[4]),
                                             placement[5])
                    except ValueError:
                        person = Swimmer(placement[2], placement[1], 9, placement[4])

                    for sw in swimmers:
                        if person.first_name == sw.first_name \
                                and person.last_name == sw.last_name \
                                and person.school == sw.school:
                            person = sw
                    if person not in swimmers:
                        swimmers.append(person)
                    if event_name not in person.events:
                        person.events[event_name] = []
                    for it in range(10):
                        if "NT" in placement[it] \
                                or "NP" in placement[it] \
                                or ":" in placement[it] \
                                or "." in placement[it]:
                            try:
                                person.events[event_name].append(placement[it + 1])
                            except IndexError:
                                print(f'Error loading {event_name} data for '
                                      f'{person.first_name} {person.last_name}: skipping...')
                            break

    swim_dict = {}
    for sw in swimmers:
        swim_dict[sw.__repr__()] = {
            "name": {
                "first": sw.first_name,
                "last": sw.last_name
            },
            "grade": sw.grade,
            "school": sw.school,
            "events": sw.events
        }

    with open('swim_data.json', 'w') as f:
        json.dump(swim_dict, f, indent=4)


request_data(years=[2022])
sort_data()
