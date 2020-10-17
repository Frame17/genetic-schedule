import random
import names
import numpy as np
from model import *

MAX_ITERATIONS = 100
MIN_LECTURE_ROOM_CAPACITY = 15

DISCIPLINES = ["Intro to Computer Science", "Databases", "Linear Algebra", "Calculus", "Algorithms", "System Theory"]
TEACHERS = ["John Doe", "Ed Sheeran", "LeBron James", "Donald Trump", "Petro Poroshenko"]
STUDENTS = list(dict.fromkeys([names.get_full_name() for _ in list(range(120))]))
ROOMS = [Room(110, 10), Room(303, 50), Room(113, 30), Room(404, 50), Room(119, 30), Room(313, 60)]


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


def pick_room(lesson_type, rooms, students_number):
    # filter out rooms that are too small for this number of students
    if lesson_type == "lecture":
        rooms = list(filter(lambda room: room.capacity >= students_number, rooms))

    return random.choice(rooms)


def generate_discipline():
    lesson_type = random.choice(["lecture", "practice"])
    teacher = random.choice(TEACHERS)
    name = random.choice(DISCIPLINES)
    students = random.sample(STUDENTS, random.randrange(10, 40))
    day = random.choice([Day.MON, Day.TUE, Day.WED, Day.THU, Day.FRI])
    time = random.choice([Time.FIRST, Time.SECOND, Time.THIRD, Time.FOURTH, Time.FIFTH, Time.SIXTH, Time.SEVENTH])
    room = pick_room(lesson_type, ROOMS, len(students))

    return Discipline(lesson_type, name, teacher, students, day, time, room)


def overlapping_rooms_penalty(discs):
    return overlapping_penalty(discs, lambda i, j: discs[i].room == discs[j].room, 5)


def overlapping_teachers_penalty(discs):
    return overlapping_penalty(discs, lambda i, j: discs[i].teacher == discs[j].teacher, 10)


def overlapping_students_penalty(discs):
    return overlapping_penalty(discs, lambda i, j: list(set(discs[i].students) & set(discs[j].students)), 3)


def overlapping_penalty(discs, predicate, penalty_value):
    penalty = 0
    for i in range(0, len(discs)):
        for j in range(i + 1, len(discs)):
            if predicate(i, j) and discs[i].day == discs[j].day and discs[i].time == discs[j].time:
                penalty -= penalty_value  # overlapping disciplines for teachers are unacceptable

    return penalty


def score(schedule):
    capacity_penalty = -len([disc for disc in schedule.disciplines
                             if disc.room.capacity < len(disc.students)])

    return capacity_penalty + overlapping_teachers_penalty(schedule.disciplines) + \
           overlapping_students_penalty(schedule.disciplines) + overlapping_rooms_penalty(schedule.disciplines)


if __name__ == '__main__':
    population_rank = [(None, -1)]
    population = generate_population()
    iterations = 0
    while population_rank[0][1] < 0 and iterations < MAX_ITERATIONS:
        iterations += 1
        scored_population = list(map(lambda schedule: (schedule, score(schedule)), population))
        population_rank = sorted(scored_population, key=lambda schedule: schedule[1], reverse=True)
        population = new_gen(population_rank)

    population_rank[0][0].disciplines.sort(key=lambda discipline: (discipline.day, discipline.time))
    print(f'Iterations: {iterations}')
    print(population_rank[0][0])
    print(f'score: {population_rank[0][1]}')
