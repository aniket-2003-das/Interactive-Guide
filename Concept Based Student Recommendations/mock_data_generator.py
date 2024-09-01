from faker import Faker
from random import randint
import random

fake = Faker()

master_tag_list = ["Web Development" ,"Entrepreneurship" ,"Writing" ,"Blockchain" ,"Robotics" ,"AI" ,"IOT" ,"Management skills" ,"Guitar" ,"Singing" ,"Montessori" ,"Secondary School" ,"IIT" ,"SAT" ,"Salsa" ,"Backyard" ,"Ohms Law" ,"Total Internal Reflection" ,"Monument Types" ,"Integrated Circuit Design" ,"4 phase induction motor" ,"Ore" ,"metal" ,"Circuit Diagram" ,"Psychometric" ,"Multiple Intelligence" ,"Aptitude" ,"English Speaking" ,"Critical Thinking" ,"Life skills" ,"Media Literacy" ,"Graphic Designing" ,"Photoshop" ,"After Effects"]
master_preferences_list =["Cricket", "Dance", "Doctor", "Engineer", "Coding", "Entrepreneur", "Pilot"]


def get_mock_course_data():
    course_data = []
    for i in range(0, 100):
        course_obj = {'tags': random.sample(master_tag_list, randint(4, 9)), 'courseName': fake.name()}
        course_data.append(course_obj)
    return course_data


def get_student_mock_data():
    student_data = []
    for i in range(0, 100):
        student_obj = {'studentPrefrences': random.sample(master_preferences_list, randint(4, 7)), 'name': fake.name()}
        student_data.append(student_obj)
    return student_data


def get_mock_psycometric_object():
    obj = {}
    obj['Realistic'] = 10
    obj['Investigative'] = 10
    obj['Artistic'] = 90
    obj['Enterprising'] = 30
    obj['Conventional'] = 10
    obj['Social'] = 20
    return obj

