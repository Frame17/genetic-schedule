import random
import names
import numpy as np
from model import *

MAX_ITERATIONS = 100

DISCIPLINES = ["Intro to Computer Science", "Databases", "Linear Algebra", "Calculus", "Algorithms"]
TEACHERS = ["John Doe", "Ed Sheeran", "LeBron James", "Donald Trump", "Petro Poroshenko"]
STUDENTS = [names.get_full_name() for _ in list(range(120))]
ROOMS = [Room(303, 50), Room(113, 30), Room(404, 50), Room(119, 30), Room(313, 60)]


def generate_population():
    return [generate_schedule() for _ in range(0, 10)]


def new_gen(old_gen):
    new_gen = []
    p = np.array([1 / (k + 1) for k in range(len(old_gen))])
    p /= p.sum()  # normalize probabilities
    for _ in old_gen:
        ind1 = np.random.choice(a=list(map(lambda ind: ind[0], old_gen)), size=1, p=p)[0]
        ind2 = np.random.choice(a=list(map(lambda ind: ind[0], old_gen)), size=1, p=p)[0]
        child = breed(ind1, ind2)
        mutate(child)
        new_gen.append(child)

    return new_gen


def breed(ind1, ind2):
    ratio = 1 + random.randrange(len(ind1.disciplines) - 1)  # ratio Є [1, 9]
    return Schedule(ind1.disciplines[:ratio] + ind2.disciplines[ratio:])


def mutate(schedule):
    i = random.randrange(0, len(schedule.disciplines))
    schedule.disciplines[i] = generate_discipline()


def generate_schedule():
    return Schedule([generate_discipline() for _ in range(0, 10)])


def generate_discipline():
    type = random.choice(["lecture", "practice"])
    teacher = random.choice(TEACHERS)
    name = random.choice(DISCIPLINES)
    students = random.sample(STUDENTS, random.randrange(30, 70))
    day = random.choice(["mon", "tue", "wed", "thu", "fri"])
    time = random.choice([8.30, 10, 11.40, 13.30, 15, 16.30, 18])
    room = random.choice(ROOMS)
    return Discipline(type, name, teacher, students, day, time, room)


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
    population = generate_population()
    iterations = 0
    while population_rank[0][1] < 0 and iterations < MAX_ITERATIONS:
        iterations += 1
        scored_population = list(map(lambda schedule: (schedule, score(schedule)), population))
        population_rank = sorted(scored_population, key=lambda schedule: schedule[1], reverse=True)
        population = new_gen(population_rank)

    print(f'Iterations: {iterations}')
    print(population_rank[0][0])
    print(f'score: {population_rank[0][1]}')
