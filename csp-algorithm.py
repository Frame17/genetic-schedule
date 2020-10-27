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
    X = [(day, time, room) for day in list(map(lambda x: x, Day)) for time in list(map(lambda x: x, Time))
         for room in ROOMS]

    disciplines = [generate_discipline() for _ in range(0, 10)]
    for i in range(0, len(disciplines)):
        spot = heuristics(X, disciplines, i)
        disciplines[i].day = spot[0]
        disciplines[i].time = spot[1]
        disciplines[i].room = spot[2]
    return Schedule(disciplines)


def on_spot(discipline, spot, disc):
    return discipline.day == spot[0] and discipline.time == spot[1] and discipline.room == spot[2] or \
           discipline.day == spot[0] and discipline.time == spot[1] and disc.teacher == discipline.teacher or \
           discipline.day == spot[0] and discipline.time == spot[1] and discipline.type != disc.type


def mrv(X, disciplines, i):
    return \
        sorted(X,
               key=lambda spot: len(list(filter(lambda disc: on_spot(disc, spot, disciplines[i]), disciplines[:i]))))[0]


# in our case, choosing a spot for a discipline, the discipline will be the one with the most constraints on other
# disciplines
def degree_evr(X, disciplines, discipline):
    return mrv(X, disciplines, discipline)


def conflicts(disc1, disc2):
    return disc1.name == disc2.name and disc1.type == disc2.type or disc1.teacher == disc2.teacher


def lcv(X, disciplines, i):
    current_disc = disciplines[i]

    def overlappings(x):
        current_disc.day = x[0]
        current_disc.time = x[1]
        current_disc.room = x[2]
        return len(list(filter(lambda disc: conflicts(current_disc, disc), disciplines[i:])))

    least = (overlappings(X[0]), X[0])
    for x in X:
        olp = overlappings(x)
        if olp < least[0]:
            least = (olp, x)
    return least[1]


def forward_checking():
    X = [(day, time, room) for day in list(map(lambda x: x, Day)) for time in list(map(lambda x: x, Time))
         for room in ROOMS]

    disciplines_spots = [(X.copy(), generate_discipline()) for _ in range(0, 10)]
    for i in range(0, len(disciplines_spots)):
        spot = random.choice(disciplines_spots[i][0])
        disciplines_spots[i][1].day = spot[0]
        disciplines_spots[i][1].time = spot[1]
        disciplines_spots[i][1].room = spot[2]
        for j in range(i + 1, len(disciplines_spots)):
            if conflicts(disciplines_spots[i][1], disciplines_spots[j][1]):
                disciplines_spots[j][0].remove(spot)

    return Schedule(map(lambda ds: ds[1], disciplines_spots))


if __name__ == '__main__':
    print(run_schedule(mrv))
    print(forward_checking())
