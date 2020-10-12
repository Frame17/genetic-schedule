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
        return f'{self.day} | {self.time} | {self.room} | {self.name} | {self.type} | {self.teacher} | {self.students}'
