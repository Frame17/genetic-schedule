from model import *
import names
import random

DISCIPLINES = ["Intro to Computer Science", "Databases", "Linear Algebra", "Calculus", "Algorithms", "System Theory"]
TEACHERS = ["John Doe", "Ed Sheeran", "LeBron James", "Donald Trump", "Petro Poroshenko"]
LESSON_TYPES = ["lecture", "practice"]
STUDENTS = list(dict.fromkeys([names.get_full_name() for _ in list(range(120))]))
ROOMS = [Room(110, 10), Room(303, 50), Room(113, 30), Room(404, 50), Room(119, 30), Room(313, 60)]


def generate_discipline():
    lesson_type = random.choice(LESSON_TYPES)
    teacher = random.choice(TEACHERS)
    name = random.choice(DISCIPLINES)
    students = random.sample(STUDENTS, random.randrange(10, 40))

    return Discipline(lesson_type, name, teacher, students, None, None, None)


def run_schedule(heuristics):
    X = [(day, time, room, lesson_type) for day in list(map(lambda x: x, Day)) for time in list(map(lambda x: x, Time))
         for room in ROOMS for lesson_type in LESSON_TYPES]

    disciplines = [generate_discipline() for _ in range(0, 10)]
    for i in range(0, len(disciplines)):
        spot = heuristics(X, disciplines[:i])
        disciplines[i].day = spot[0]
        disciplines[i].time = spot[1]
        disciplines[i].room = spot[2]
        disciplines[i].type = spot[3]
    return Schedule(disciplines)


def on_spot(discipline, spot):
    return (discipline.day == spot[0] and discipline.time == spot[1] and discipline.room == spot[2]) \
           or (discipline.day == spot[0] and discipline.time == spot[1] and discipline.room == spot[2]
               and discipline.type != spot[3])


def mrv(X, disciplines):
    return sorted(X, key=lambda spot: len(list(filter(lambda disc: on_spot(disc, spot), disciplines))))[0]


if __name__ == '__main__':
    print(run_schedule(mrv))
