import csv

from .student import Student


def parse_homeroom(path):
    """
    Path must be pathlib Path object.
    """
    teacher = path.stem[2:]
    grade_level = path.stem[1]

    # assign indicies of id and name rows to variables "id_index" and "name
    # index."
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            for index, item in enumerate(row):
                if item.lower() == 'id':
                    id_index = index
                if item.lower() == 'name':
                    name_index = index
        if not id_index or not name_index:
            raise Exception('Appropriate headers not found.')

    # instantiate a student for every student in the csv
    students = []
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        reader.__next__()
        for row in reader:
            inverted_name = row[1]
            flip_index = inverted_name.index(',')
            last_name = inverted_name[:flip_index]
            first_name = inverted_name[(flip_index + 2):]

            context = {
                'first_name': first_name,
                'last_name': last_name,
                'student_id': row[0],
                'email': None,
                'homeroom': teacher,
                'grade_level': grade_level,
            }

            student = Student(context)
            students.append(student)

    return teacher, grade_level, students


def parse_group(path):
    """
    path must be a pathlib Path object.
    """
    group_name = path.stem[2:]
    grade_level = path.stem[1]
    students = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            nm = row[0].split(' ')
            context = {
                'first_name': nm[0],
                'last_name': nm[1],
                'student_id': None,
                'email': None,
                'homeroom': None,
                'groups': [group_name],
                'grade_level': grade_level,
            }
            students.append(Student(context))

        return group_name, grade_level, students
