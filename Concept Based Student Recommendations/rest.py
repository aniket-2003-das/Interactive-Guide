import requests
import json



def get_courses_data():
    response_API = requests.get('https://demo-partner.ed2100.com/api2/user/getAllCoursesListForUsers')
    return json.loads(response_API.text)['response']



def get_student(token, student_id):
    headers = {'Authorization': token}
    response_API = requests.get(f'https://demo-partner.ed2100.com/api2/user/retrieveStudentProfile/{student_id}'.format(student_id=student_id), headers=headers)
    return json.loads(response_API.text)['Body']


def get_students_of_school(token):
    headers = {'Authorization': token}
    response_API = requests.get(
        'https://demo-partner.ed2100.com/api2/school/get-all-students-of-school',
        headers=headers)
    return json.loads(response_API.text)['response']['studentsList']