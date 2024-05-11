import prettytable as prettytable
from random import randint
from random import random

allInstructor = []
class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name


    def get_id(self): return self._id

    def get_name(self): return self._name

    def __str__(self): return self._name


class Room:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity

    def get_number(self): return self._number

    def get_seatingCapacity(self): return self._seatingCapacity


class TimeAvilable:
    def __init__(self, id, time):
        self.id = id
        self.time = time

    def get_id(self): return self.id

    def get_time(self): return self.time


class Courses:
    def __init__(self, number, name, instructors, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._instructors = instructors
        self.maxNumbOfStudents = maxNumbOfStudents

    def get_number(self): return self._number

    def get_name(self): return self._name

    def get_instructors(self): return self._instructors

    def get_maxNumbOfStudents(self): return self.maxNumbOfStudents

    def __str__(self): return self._name


class Department:
    def __init__(self, name, Courses):
        self._name = name
        self._Courses = Courses

    def get_name(self): return self._name

    def get_Courses(self): return self._Courses


class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._TimeAvilable = None
        self._room = None

    def get_id(self): return self._id

    def get_dept(self): return self._dept

    def get_course(self): return self._course

    def get_instructor(self): return self._instructor

    def get_TimeAvilable(self): return self._TimeAvilable

    def get_room(self): return self._room

    def set_instructor(self, instructor): self._instructor = instructor

    def set_TimeAvilable(self, TimeAvilable): self._TimeAvilable = TimeAvilable

    def set_room(self, room): self._room = room

    def __str__(self):
        return "{" + str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + \
               str(self._room.get_number()) + "," + str(self._instructor.get_id()) + "," + str(
            self._TimeAvilable.get_id()) + "}"


class Data:
    ROOMS = [["R1", 25], ["R2", 45], ["R3", 35]]
    Time_Avilable = [["MT1", "MWF 09:00 - 10:00"],
                     ["MT2", "MWF 10:00 - 11:00"],
                     ["MT3", "TTH 09:00 - 10:30"],
                     ["MT4", "TTH 10:30 - 12:00"]]

    def __init__(self, all_courses, all_depts, all_instructors):
        self._rooms = []
        self._TimeAvilable = []
        for i in range(0, len(self.ROOMS)):
            self._rooms.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))
        for i in range(0, len(self.Time_Avilable)):
            self._TimeAvilable.append(TimeAvilable(self.Time_Avilable[i][0], self.Time_Avilable[i][1]))
        self._instructors = all_instructors
        self.courses = all_courses
        self.depts = all_depts
        self.numberOfClasses = 0
        for i in range(0, len(self.depts)):
            self.numberOfClasses += len(self.depts[i].get_Courses())

    def get_rooms(self):
        return self._rooms

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self.courses

    def get_depts(self):
        return self.depts

    def get_TimeAvilable(self):
        return self._TimeAvilable

    def get_numberOfClasses(self):
        return self.numberOfClasses


class schedule:
    def __init__(self):
        self.data = data
        self.classes = []
        self.num_of_conflict = 0
        self.fitness = -1
        self.classesNumb = 0
        self.isFitnesschanged = True  # ********

    def initialize(self):
        depts = self.data.get_depts()
        # print(depts[2].get_name())
        # print(depts[1].get_Courses)
        #  print(len(depts))
        for i in range(0, len(depts)):
            #  print(i)
            courses = depts[i].get_Courses()
            # for k in range(0, len(courses)):
            #      print(courses[k].get_name())
            # print("-------------")
            # print(courses[i].get_name())
            for j in range(0, len(courses)):
                new_class = Class(self.classesNumb, depts[i], courses[j])
                self.classesNumb += 1
                new_class.set_TimeAvilable(data.get_TimeAvilable()[randint(0, len(data.get_TimeAvilable()) - 1)])
                new_class.set_room(data.get_rooms()[randint(0, len(data.get_rooms()) - 1)])
                new_class.set_instructor(
                    courses[j].get_instructors()[randint(0, len(courses[j].get_instructors()) - 1)])
                self.classes.append(new_class)
                # print(courses[j].get_name())
                # print("-------------")

        return self

    def get_classes(self):
        self.isFitnesschanged = True
        return self.classes

    def get_number_Of_conflict(self):
        return self.num_of_conflict

    def calculate_fit(self):
        self.num_of_conflict = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):

            if (classes[i].get_room().get_seatingCapacity() < int(classes[i].get_course().get_maxNumbOfStudents())):
                self.num_of_conflict += 1
            for j in range(0, len(classes)):
                if (j >= i):
                    if (classes[i].get_TimeAvilable() == classes[j].get_TimeAvilable() and classes[i].get_id() !=
                            classes[j].get_id()):
                        if (classes[i].get_room() == classes[j].get_room()): self.num_of_conflict += 1
                        if (classes[i].get_instructor() == classes[j].get_instructor()): self.num_of_conflict += 1
        return 1 / ((1.0 * self.num_of_conflict) + 1)  # *1.0 to convert int to float

    def get_fitness(self):
        if (self.isFitnesschanged == True):
            self.fitness = self.calculate_fit()
            self.isFitnesschanged = False
        return self.fitness

    def __str__(self):
        pharse = ""
        for i in range(0, len(self.classes)):
            pharse += str(self.classes[i]) + ","

        return pharse


class Population:
    def __init__(self, size):
        self.size = size
        self.data = data
        self.schedules = []
        for i in range(0, size):
            self.schedules.append(schedule().initialize())

    def get_schedules(self):
        return self.schedules


class genatic_algorithm:

    def evolve(self, popu):
        return self.mutation(self.crossover(popu))

    def crossover(self, popu):
        crossover_pop = Population(0)
        for i in range(NUMB_OFELITE_SCHEDULES):
            crossover_pop.get_schedules().append(
                popu.get_schedules()[i])  # take a copy of population list not reference
        i = NUMB_OFELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self.select_tournament_population(popu).get_schedules()[0]
            schedule2 = self.select_tournament_population(popu).get_schedules()[1]
            crossover_pop.get_schedules().append(self.crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def mutation(self, popu):  # mutate every schedule in population
        for i in range(NUMB_OFELITE_SCHEDULES, POPULATION_SIZE):
            self.mutate_schedule(popu.get_schedules()[i])
        return popu

    def crossover_schedule(self, schedule1, schedule2):  # get new childe from restored  2 schduler parent
        crossoverSchedule = schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if (random() > 0.5):
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def mutate_schedule(self, mutate):  # mutate 1 schedule
        scheduler = schedule().initialize()
        for i in range(0, len(mutate.get_classes())):
            if (MUTATION_RATE > random()):
                mutate.get_classes()[i] = scheduler.get_classes()[i]
        return mutate

    def select_tournament_population(self, popu):  # to select parents
        tournament_pop = Population(0)
        i = 0
        while i < TORNAMENT_SELECTON_SIZE:
            tournament_pop.get_schedules().append(popu.get_schedules()[randint(0, POPULATION_SIZE - 1)])
            i += 1
        tournament_pop.get_schedules().sort(key=get_sort_key, reverse=True)
        print(len(tournament_pop.get_schedules()))
        return tournament_pop


class Display:
    def print_available_data(self, courses, deps, instructors):
        print("> ALL Available Data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor(courses, deps, instructors)
        self.print_Time_Avilable()

    def print_dept(self):
        depts = data.get_depts()
        print(len(depts))
        availableDeptsTable = prettytable.PrettyTable(['dept', 'course'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_Courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])

        print(availableDeptsTable)

    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructors'])
        courses = data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ","
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), tempStr])
        print(availableCoursesTable)

    def print_instructor(self, courses, deps, inst):
        data = Data(courses, deps, inst)
        availableInstructorsTable = prettytable.PrettyTable(['id', 'instructors'])
        instructors = data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorsTable.add_row([instructors[i].get_id(), instructors[i].get_name()])

        print(availableInstructorsTable)

    def print_room(self):
        availableRoomsTable = prettytable.PrettyTable(['room #', 'max seating capacity'])
        rooms = data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)

    def print_Time_Avilable(self):
        availableTimeAvilableTable = prettytable.PrettyTable(['id', 'Time Avilable'])
        timeAvilable = data.get_TimeAvilable()
        for i in range(0, len(timeAvilable)):
            availableTimeAvilableTable.add_row([timeAvilable[i].get_id(), timeAvilable[i].get_time()])
        print(availableTimeAvilableTable)

    def print_generation(self, population):
        table1 = prettytable.PrettyTable(
            ['schedule #', 'fitness', '# of conflicts', 'classes[dept,class,room,instructor]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row(
                [str(i), round(schedules[i].get_fitness(), 3), schedules[i].get_number_Of_conflict(), schedules[i]])
        print(table1)

    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(
            ['Class #', 'Dept', 'Course(number , max # of students)', 'Room (Capacity)', 'Instructor', 'TimeAvilable'])
        for i in range(0, len(classes)):
            table.add_row([str(i), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + " (" +
                           classes[i].get_course().get_number() + ", " + str(
                classes[i].get_course().get_maxNumbOfStudents()) + ")",
                           classes[i].get_room().get_number() + " (" + str(
                               classes[i].get_room().get_seatingCapacity()) + ")",
                           classes[i].get_instructor().get_name() + " (" + str(
                               classes[i].get_instructor().get_id()) + ")",
                           classes[i].get_TimeAvilable().get_time() + " (" + str(
                               classes[i].get_TimeAvilable().get_id()) + ")"])
        print(table)


POPULATION_SIZE = 10
NUMB_OFELITE_SCHEDULES = 1
TORNAMENT_SELECTON_SIZE = 2
MUTATION_RATE = 0.1

def take_input():
    # name_set = set()
    all_departments = []
    all_courses = []
    all_instructors = []
    print('*************************** Enter system data ***************************************')
    dep_nums = int(input("enter number of departments: "))
    for i in range(dep_nums):
        print('\n_____________________ department data __________________________________')
        dep_name = input(f"enter department{i + 1} name: ")
        courses_num = int(input(f"enter number of courses in {dep_name} department: "))
        courses_list = []
        for j in range(courses_num):
            print('\n_____________________ course data __________________________________')
            instructors = []
            c_name = input(f"enter course{j + 1} name: ")
            c_Capacity = int(input(f"enter {c_name} course capacity: "))
            inst_num = int(input("enter instructors numbers: "))
            print()
            for k in range(inst_num):
                i_name = input(f"enter instructor{k + 1} name: ")

                if i_name not in allInstructor:
                    instructors.append(Instructor(len(all_instructors)+1, i_name))
                    all_instructors.append(Instructor(len(all_instructors)+1, i_name))
                    allInstructor.append(i_name)
                else:
                    for obj in all_instructors:
                        name = getattr(obj, "_name")
                        if name == i_name:
                            instructors.append(obj)
                            break
            courses_list.append(Courses("C{}".format(len(all_courses) + 1), c_name, instructors, c_Capacity))
            all_courses.append(Courses("C{}".format(len(all_courses) + 1), c_name, instructors, c_Capacity))
        dep = Department(dep_name, courses_list)
        all_departments.append(dep)

    return all_courses, all_departments, all_instructors


courses, deps, instructors = take_input()
data = Data(courses, deps, instructors)
display = Display()
display.print_available_data(courses, deps, instructors)

generationNumber = 0
print("\n> Generation # " + str(generationNumber))
# instantiating the population
population = Population(POPULATION_SIZE)


# sort the schdules in the population
def get_sort_key(list):
    return list.get_fitness()


population.get_schedules().sort(key=get_sort_key, reverse=True)
# print generation ZERO
display.print_generation(population)
# print the fitness schudules in generation zero
# display.print_schedule_as_table(population.get_schedules()[0])
genatic = genatic_algorithm()

while (population.get_schedules()[0].get_fitness() != 1.0):
    if generationNumber == 100:
        break

    generationNumber += 1
    print("\n> Generation # " + str(generationNumber))
    population = genatic.evolve(population)
    population.get_schedules().sort(key=get_sort_key, reverse=True)
    display.print_generation(population)

print("\nThe  possible optimal scheduling table: ")
display.print_schedule_as_table(population.get_schedules()[0])

