from enum import IntEnum, Enum

class Room:
    def __init__(self, number, capacity):
        self.number = number
        self.capacity = capacity

    def __str__(self):
        return f'{self.number}'


class Schedule:
    def __init__(self, disciplines):
        self.disciplines = disciplines

    def __str__(self):
        res = ""
        for d in self.disciplines:
            res += str(d)
            res += '\n'
        return res


class Discipline:
    def __init__(self, type, name, teacher, students, day, time, room):
        self.type = type
        self.name = name
        self.teacher = teacher
        self.students = students
        self.day = day
        self.time = time
        self.room = room

    def __str__(self):
        return f'{self.day.name} | {self.time.value} | {self.room} | {self.name} | {self.type} | {self.teacher} | {len(self.students)}'


class Day(IntEnum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5


class Time(Enum):
    FIRST = "08:30-09:50"
    SECOND = "10:00-11:20"
    THIRD = "11:40-13:00"
    FOURTH = "13:30-14:50"
    FIFTH = "15:00-16:20"
    SIXTH = "16:30-17:50"
    SEVENTH = "18:00-19:20"

    def __lt__(self, other):
        return self.value < other.value
