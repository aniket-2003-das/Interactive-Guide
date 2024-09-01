import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
from mock_data_generator import *

import pandas as pd


def     get_content_based_filtered_course(title, initial_data, num_recommendations):
    a_json = json.loads(json.dumps(initial_data))

    data = []
    for course in a_json:
        course_object = {}
        course_object['courseName'] = course['courseName']
        course_object['tags'] = " ".join(course['tags'])

        data.append(course_object)

    df = pd.DataFrame.from_dict(data)

    tfv = TfidfVectorizer(min_df=1, max_features=None,
                          strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                          ngram_range=(1, 3),
                          stop_words='english')

    tfv_matrix = tfv.fit_transform(df['tags'])
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
    indices = pd.Series(df.index, index=df['courseName']).drop_duplicates()

    # Get the index corresponding to given course
    idx = indices[title]

    # Get the pairwsie similarity scores with given course with every available course in the data set
    sig_scores = list(enumerate(sig[idx]))

    # Sort the recommended courses
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar courses
    sig_scores = sig_scores[1: int(num_recommendations)]

    # get courses indices for top 10 recommended courses
    course_indices = [i[0] for i in sig_scores]

    # Top 10 most similar courses
    return course_indices
