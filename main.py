import random


class Discipline:
    def __init__(self, type, students, day, time):
        self.type = type
        self.students = students
        self.day = day
        self.time = time


class Room:
    def __init__(self, capacity):
        self.capacity = capacity


def can_fit_lecture(room):
    return room.capacity >= 45


def generate_population():
    population = []
    for i in range(0, 10):
        type = random.choice(["lecture", "practice"])
        students = random.randrange(15, 60)
        day = random.choice(["sun", "mon", "tue", "wed", "thu", "fri", "sat"])
        time = random.choice([8.30, 10, 11.40, 13.30, 15, 16.30, 18])
        population.append(Discipline(type, students, day, time))
    return population


if __name__ == '__main__':
    population = generate_population()
    print()
