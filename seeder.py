import time
from django.contrib.auth.models import User
from backend.models import Profile, Course, Group, SurveyAnswers, Survey
from random import randint, choice, choices, sample


def seed_profiles(num_entries=10, overwrite=False):
    """
    Creates num_entries new profiles
    """
    if overwrite:
        Profile.objects.all().delete()

    users = User.objects.all()
    for user in users:

        # profe sera teacher de los cursos
        if user.first_name == "Rodrigo" or user.last_name == "Ruz":
            p_teacher = Profile.objects.create(
                is_teacher=True,
                active=True,
                student_number=None,
                user=user
            )
        else:
            student_number = randint(15620000, 20000000)
            p = Profile.objects.create(
                is_teacher=False,
                active=True,
                student_number=student_number,
                user=user
            )


def seed_users(num_entries=10, overwrite=False):
    """
    Creates num_entries new users
    """
    if overwrite:
        print("Cleaning Users Table")
        User.objects.all().delete()
    count = 0
    usernames = ["janosiegel", "jpsiegel", "elJano", "janomaster", "januel", "manteca", "nicobro", "maxs", "maxi",
                 "elmax", "maxUndurraga", "CristobalR", "crisR", "cristoBall", "Chelo", "elChelo", "Nico2",
                 "DiegoNavarro", "iLoveMate"]
    lastnames = ["Siegel", "Undurraga", "Vargas", "Reyes", "Navarro", "Sepulveda", "Sanchez", "Turing", "Espindola"]
    firstnames = ["Jan", "Max", "Nicolas", "Nico", "Cristobal", "Marcelo", "Diego"]
    email_endings = ["yahoo.cl", "gmail.com", "uc.cl", "hotmail.com", "mate.cl", "outlook.com", "applemail.us",
                     "mailer.com"]

    # hacemos dos teachers
    u1 = User.objects.create_user(
        email="rodrigo_sandoval@ing.puc.cl",
        first_name="Rodrigo",
        last_name="Sandoval",
        username="ProfesorSandoval",
    )

    u2 = User.objects.create_user(
        email="cristian_ruz@ing.puc.cl",
        first_name="Crisitan",
        last_name="Ruz",
        username="ProfesorRuz",
    )

    # hacemos num_entries students
    for _ in range(num_entries):
        username = choice(usernames) + str(randint(0, 100))
        first_name = choice(firstnames)
        last_name = choice(lastnames)
        email = first_name + last_name + str(randint(0, 100)) + "@" + choice(email_endings)

        u = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )

        count += 1
        percent_complete = count / num_entries * 100
        print("Seeding {} Users: {:.2f}%".format(num_entries, percent_complete), end='\r', flush=True)
    print()


def seed_courses(num_entries=10, overwrite=False):
    """
    Creates num_entries new courses
    """
    if overwrite:
        print("Cleaning Courses Table")
        Course.objects.all().delete()
    count = 0

    names = ["Desarrollo de Software", "Programacion Avanzada", "Ingenieria de Software", "Bases de Datos",
             "Inteligencia Artificial", "Intro a la Programacion", "Mecanica de Fluidos", "Modelos Estocasticos",
             "Desafios de la Ingenieria", "Termodinamica", "Ecuaciones Diferenciales", "Etica", "Estructuras de Datos",
             "Deep Learning", "Quimica General", "Calculo III", "Optimizacion", "Innovacion", "Calculo I", "Calculo II"]
    tags = ["IIC", "ING"]

    teacher = choice(User.objects.filter(profile__is_teacher=True))  # random teacher selected
    students = User.objects.filter(profile__is_teacher=False)
    amount_ = randint(2, len(students))

    # hacemos num_entries cursos
    for _ in range(num_entries):
        some_students = sample([student for student in students], k=amount_)  # elegimos muestra sin repeticion
        name = names.pop()
        tag = choice(tags) + str(randint(1100, 3600))

        c = Course.objects.create(
            name=name,
            tag=tag,
            teacher_fk=teacher,
            active=True,
        )
        c.students.add(*some_students)

        count += 1
        percent_complete = count / num_entries * 100
        print("Seeding {} Courses: {:.2f}%".format(num_entries, percent_complete), end='\r', flush=True)
    print()


def seed_groups(num_entries=10, overwrite=False):
    """
    Creates num_entries new groups
    """
    if overwrite:
        print("Cleaning Groups Table")
        Group.objects.all().delete()
    count = 0

    courses = Course.objects.all()
    students = User.objects.filter(profile__is_teacher=False)
    names = ["MATE", "Hackermen", "LosDropTables", "LosAnonymous", "MakeDCCGreatAgain", "DockerFans", "LosRezagados",
             "AboveAverage", "Full-Stackers", "TheMVPs", "The3W", "Meit", "Maxs", "DCCabros", "EasyPeasy", "SpaceZ",
             "TheBestGroup", "Grupazo", "AsadoProfesional", "Ingecabros", "LasProgrammers", "HTTPower"]

    for course in courses:
        numbers = [num for num in range(num_entries)]
        course_students = [student for student in course.students.all()]

        # hacemos num_entries grupos de amount students cada uno pa cada curso
        amount_ = randint(2, len(course_students))
        for _ in range(num_entries):
            some_members = sample(course_students, k=amount_)  # elegimos alumnos del curso
            name = choice(names)

            g = Group.objects.create(
                name=name,
                number=numbers.pop(),
                course_fk=course,
                active=True,
            )
            g.members.add(*some_members)

        count += 1
        percent_complete = count / len(courses) * 100
        print("Seeding {} Groups: {:.2f}%".format(len(courses) * num_entries, percent_complete), end='\r', flush=True)
    print()


def seed_surveys(num_entries=10, overwrite=False):
    """
    Creates num_entries new surveys
    """
    pass


def seed_all(num_entries=10, overwrite=False):
    """
    Runs all seeder functions.
    Passes value of overwrite to all seeder function calls.
    """
    start_time = time.time()
    # run seeds
    seed_users(num_entries=num_entries, overwrite=overwrite)
    seed_profiles(num_entries=num_entries, overwrite=overwrite)
    seed_courses(num_entries=num_entries, overwrite=overwrite)
    seed_groups(num_entries=num_entries, overwrite=overwrite)
    seed_surveys(num_entries=num_entries, overwrite=overwrite)

    # get time
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print("Seeding took: {} minutes {} seconds".format(minutes, seconds))
