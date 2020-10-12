import random
from model import *

DISCIPLINES = ["Intro to Computer Science", "Databases", "Linear Algebra", "Calculus", "Algorithms"]
TEACHERS = ["John Doe", "Ed Sheeran", "LeBron James", "Donald Trump", "Petro Poroshenko"]
ROOMS = [Room(303, 50), Room(113, 30), Room(404, 50), Room(119, 30), Room(313, 60)]


def can_fit_lecture(room):
    return room.capacity >= 45


def generate_population():
    return [generate_schedule() for _ in range(0, 10)]


def generate_schedule():
    disciplines = []
    for i in range(0, 10):
        type = random.choice(["lecture", "practice"])
        teacher = random.choice(TEACHERS)
        name = random.choice(DISCIPLINES)
        students = random.randrange(15, 50)
        day = random.choice(["sun", "mon", "tue", "wed", "thu", "fri", "sat"])
        time = random.choice([8.30, 10, 11.40, 13.30, 15, 16.30, 18])
        room = random.choice(ROOMS)
        disciplines.append(Discipline(type, name, teacher, students, day, time, room))
    return Schedule(disciplines)


def score(schedule):
    capacity_penalty = -len([disc for disc in schedule.disciplines
                             if disc.type == "lecture" and disc.room.capacity < 45])

    return capacity_penalty


if __name__ == '__main__':
    population_rank = [(None, -1)]
    while population_rank[0][1] < 0:
        population = generate_population()
        scored_population = list(map(lambda schedule: (schedule, score(schedule)), population))
        population_rank = sorted(scored_population, key=lambda schedule: schedule[1], reverse=True)
    print(population_rank[0][0])
