import json
import os

def names_of_registered_students(input_json_path, course_name):
    """
    This function returns a list of the names of the students who registered for
    the course with the name "course_name".

    :param input_json_path: Path of the students database json file.
    :param course_name: The name of the course.
    :return: List of the names of the students.
    """
    with open(input_json_path, 'r') as f:
        loaded_dict=json.load(f)

    return [student_dict["student_name"] for student_dict in loaded_dict.values() if course_name in student_dict["registered_courses"]]



def enrollment_numbers(input_json_path, output_file_path):
    """
    This function writes all the course names and the number of enrolled
    student in ascending order to the output file in the given path.

    :param input_json_path: Path of the students database json file.
    :param output_file_path: Path of the output text file.
    """
    with open(input_json_path, 'r') as f:
        loaded_dict=json.load(f)
    
    output_file=open(output_file_path, 'w')

    courses_dict=[student_info["registered_courses"] for student_info in loaded_dict.values()]
    courses_set=set()
    for elem in courses_dict:
        courses_set=courses_set.union(elem)
    courses_and_students={course_name:len(names_of_registered_students(input_json_path, course_name)) for course_name in courses_set}
    courses_and_students=sorted(courses_and_students.items())
    for course_name, student_number in courses_and_students:
        s1='"{}" {}\n'.format(course_name, str(student_number))
        output_file.write(s1)
    output_file.close()



def courses_for_lecturers(json_directory_path, output_json_path):
    """
    This function writes the courses given by each lecturer in json format.

    :param json_directory_path: Path of the semsters_data files.
    :param output_json_path: Path of the output json file.
    """
    courses_and_lecturers={}
    for file in os.listdir(json_directory_path):
        file_path=os.path.join(json_directory_path, file)
        if os.path.splitext(file_path)[1]==".json":
            with open(file_path, 'r') as f:
                loaded_dict=json.load(f)
                for course_dict in loaded_dict.values():
                    for lecturer in course_dict["lecturers"]:
                        if lecturer in courses_and_lecturers.keys():
                            if course_dict["course_name"] not in courses_and_lecturers[lecturer]:
                                courses_and_lecturers[lecturer].append(course_dict["course_name"])
                        else:
                            courses_and_lecturers.update({lecturer:[course_dict["course_name"]]})

    with open(output_json_path, 'w') as output_file:
        json.dump(courses_and_lecturers, output_file, indent=4)