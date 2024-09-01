from mock_data_generator import *
from content_based_filtering import *
from rest import *
from semantic_text_similarity.models import WebBertSimilarity
from constants import *
import numpy as np
from sklearn import preprocessing as pre
from utils import *


web_model = WebBertSimilarity(device='cpu', batch_size=10)  # defaults to GPU prediction

recommendation_buckets = []
def get_recommended_courses(token, student_id, use_test_report_flag, use_student_preferences, num_recommendations):
    try:
        student = get_student(token, student_id)
        # student = {'studentPrefrences': ['maths', 'coding'], 'name': 'Benjamin Taylor', 'stream': 'Science'}
    except:
        return "Error while fetching student"

    try:
         course_data = get_courses_data()
    except:
        return "Error while getting all courses"


    similarities = []
    for i in range(0, len(course_data)):
        if use_test_report_flag == 'True' and use_student_preferences == 'False':

            similarities.append(get_psycometric_similarity(get_mock_psycometric_object(), course_data[i]))
        elif use_test_report_flag == 'False' and use_student_preferences == 'True':

            if len(student['studentPrefrences']) > 0:
                similarities.append(
                    get_cumulative_similarity_for_course(course_data[i], " ".join(student['studentPrefrences']),
                                                         COURSE_FIELDS_WEIGHTS_DICT, VENDOR_FIELDS_WEIGHTS_DICT))
            else:
                similarities.append(get_cumulative_similarity_for_course(course_data[i], get_comparison_string(student),
                                                                         COURSE_FIELDS_WEIGHTS_DICT,
                                                                         VENDOR_FIELDS_WEIGHTS_DICT))
        elif use_test_report_flag == 'True' and use_student_preferences == 'True':
            similarities.append(get_psycometric_similarity(get_mock_psycometric_object(),
                                                           course_data[i]) + get_cumulative_similarity_for_course(
                course_data[i], " ".join(student['studentPrefrences']),
                COURSE_FIELDS_WEIGHTS_DICT, VENDOR_FIELDS_WEIGHTS_DICT))

    max_value = max(similarities)
    index = similarities.index(max_value)
    initial_course = course_data[index]
    similar_cpourse_indices = get_content_based_filtered_course(initial_course['courseName'], course_data,
                                                                num_recommendations)
    recommendatons = [course_data[index]]
    for similar_index in similar_cpourse_indices:
        recommendatons.append(course_data[similar_index])
    return recommendatons

def get_school_recommended_courses(token,num_recommendations, use_students_flag, buckets):
    try:
        course_data = get_courses_data()
    except:
        return "Error while getting all courses"

    if use_students_flag == 'True':
        try:
            students = get_students_of_school(token)

        except:
            return "Error while fething student list"
    else:
        courses = modidy_courses(course_data)
        recommendation_object = dict()
        for bucket in buckets['buckets']:
            if bucket == 'most_popular':
                sorted_lst = sorted(courses, key=lambda x: x['clicks'], reverse=True)
                recommendation_object[bucket] = sorted_lst[0:num_recommendations]

            if bucket == 'high_rating':
                sorted_lst = sorted(courses, key=lambda x: x['rating'], reverse=True)
                recommendation_object[bucket] = sorted_lst[0:num_recommendations]

            if bucket == 'most_enrolled':
                sorted_lst = sorted(courses, key=lambda x: x['enrolled'], reverse=True)
                recommendation_object[bucket] = sorted_lst[0:num_recommendations]

            if bucket == 'best_academic':
                sorted_lst = sorted(list(filter(lambda x: (x['types']=='academic'), courses)) , key=lambda x: x['rating'], reverse=True).reverse()
                recommendation_object[bucket] = sorted_lst[0:num_recommendations]

            if bucket == 'best_non_academic':
                sorted_lst = sorted(list(filter(lambda x: (x['types'] == 'non-academic'), courses)),
                                    key=lambda x: x['rating'], reverse=True).reverse()
                recommendation_object[bucket] = sorted_lst[0:num_recommendations]

        return recommendation_object

def get_comparison_string(student):
    comparison_string = ""
    for value in list(student.values()):
        if type(value) == str:
            comparison_string = comparison_string + " " + value
    return comparison_string


def get_psycometric_similarity(psycometric_result, course):
    indicator_words = list(psycometric_result.keys())
    x = np.asarray(list(psycometric_result.values()))
    x = x.reshape(-1, 1)
    x_norm = pre.MinMaxScaler().fit_transform(x)
    similarity = 0
    print(x_norm)
    for i in range(0, len(indicator_words)):
        word_sim = web_model.predict(
            [(" ".join(course['tags']), " ". join(TEST_INDICATOR_INTEREST_DICT[indicator_words[i]]))])
        similarity = similarity + word_sim * x_norm[i]

    return similarity


def get_cumulative_similarity_for_course(course, student_comparison_string, course_fields_weight_dict,
                                         vendor_fields_weight_dict):
    similarity = 0
    for the_key, the_value in course_fields_weight_dict.items():
        similarity = similarity + the_value * web_model.predict(
            [(course[the_key], student_comparison_string)])

    for the_key, the_value in vendor_fields_weight_dict.items():
        similarity = similarity + the_value * web_model.predict(
            [(course['vendorDetail'][the_key], student_comparison_string)])

    return similarity



