from flask import Flask
from flask import request
from recommendation import *
app = Flask(__name__)


@app.route("/test")
def hello_world():
    return "peace"


@app.route("/student/recommend", methods=['GET'])
def get_recommendations():
    num_recommendations = request.args.get('count')
    student_id = request.args.get('student_id')
    use_test_report_flag = request.args.get('use_test_report_flag')
    token = request.headers.get('Authorization')
    use_student_preferences = request.args.get('use_student_preferences')

    recommended_course = get_recommended_courses(token,student_id, use_test_report_flag,use_student_preferences, num_recommendations)
    return recommended_course


@app.route("/school/recommend", methods=['POST'])
def get_school_recommendations():
    num_recommendations = request.args.get('count')
    use_students_flag = request.args.get('use_students_flag')
    buckets = request.get_json()
    token = request.headers.get('Authorization')
    recommended_course = get_school_recommended_courses(token,int(num_recommendations), use_students_flag, buckets)
    return recommended_course

if __name__ == "__main__":
    app.run()