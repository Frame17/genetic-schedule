# Schedule Generation

This repo uses genetic and heuristic(CSP, MRV, LCV) algorithms to create schedule according to next rules:
* Courses have lectures and practices
* Restrictions to the rooms (lecture can't be in room with less than 15 seats)
* Practice lessons could be taught by different teachers
* One teacher can't have 2 lessons at the same time
* One student can't be at 2 lessons at the same time
* Schedule depends on working days/hours on the faculty (Mon-Fri, [8:30-9:50, 10:00-11:20, 11:40-13:00, 13:30-14:50, 15:00-16:20, 16:30-17:50, 18:00-19:20])