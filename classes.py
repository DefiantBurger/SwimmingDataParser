class Event:
    def __init__(self, event_name: str, swimmer_name: str, time: str):
        self.name = event_name
        self.swimmer = swimmer_name
        self.time = time

    def get_seconds_time(self):
        pass


class Swimmer:
    def __init__(self, first_name: str, last_name: str, grade: int, school: str, events=None):
        if events is None:
            events = {}
        self.first_name = first_name
        self.last_name = last_name
        self.grade = grade
        self.school = school
        self.events = events

    def __eq__(self, other):
        return isinstance(other, Swimmer) \
               and self.first_name == other.first_name \
               and self.last_name == other.last_name \
               and self.grade == other.grade \
               and self.school == other.school

    def __repr__(self):
        return f"{self.first_name}-{self.last_name}-{self.grade}-{self.school}"
