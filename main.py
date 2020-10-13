import random
import names
from model import *

MAX_ITERATIONS = 100

DISCIPLINES = ["Intro to Computer Science", "Databases", "Linear Algebra", "Calculus", "Algorithms"]
TEACHERS = ["John Doe", "Ed Sheeran", "LeBron James", "Donald Trump", "Petro Poroshenko"]
STUDENTS = [names.get_full_name() for _ in list(range(120))]
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
        students = random.sample(STUDENTS, random.randrange(30, 70))
        day = random.choice(["mon", "tue", "wed", "thu", "fri"])
        time = random.choice([8.30, 10, 11.40, 13.30, 15, 16.30, 18])
        room = random.choice(ROOMS)
        disciplines.append(Discipline(type, name, teacher, students, day, time, room))
    return Schedule(disciplines)


def overlapping_teachers_penalty(discs):
    predicate = lambda i, j: discs[i].teacher == discs[j].teacher \
                             and discs[i].day == discs[j].day \
                             and discs[i].time == discs[j].time

    return overlapping_penalty(discs, predicate, 10)


def overlapping_students_penalty(discs):
    predicate = lambda i, j: discs[i].day == discs[j].day \
                             and discs[i].time == discs[j].time \
                             and list(set(discs[i].students) & set(discs[j].students))

    return overlapping_penalty(discs, predicate, 3)


def overlapping_penalty(discs, predicate, penalty_value):
    penalty = 0
    for i in range(0, len(discs)):
        for j in range(i + 1, len(discs)):
            if predicate(i, j):
                penalty -= penalty_value  # overlapping disciplines for teachers are unacceptable

    return penalty


def score(schedule):
    capacity_penalty = -len([disc for disc in schedule.disciplines
                             if disc.room.capacity < len(disc.students)])

    return capacity_penalty + overlapping_teachers_penalty(schedule.disciplines) + \
           overlapping_students_penalty(schedule.disciplines)


if __name__ == '__main__':
    population_rank = [(None, -1)]
    iterations = 0
    while population_rank[0][1] < 0 and iterations < MAX_ITERATIONS:
        iterations += 1
        population = generate_population()
        scored_population = list(map(lambda schedule: (schedule, score(schedule)), population))
        population_rank = sorted(scored_population, key=lambda schedule: schedule[1], reverse=True)

    print(f'Iterations: {iterations}')
    print(population_rank[0][0])
    print(f'score: {population_rank[0][1]}')
