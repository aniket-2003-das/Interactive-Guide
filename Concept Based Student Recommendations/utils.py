from random import randint

#Will be removed later when these fields start coming from api
def modidy_courses(courses):
    for course in courses:
        course['rating'] = randint(1, 5)
        course['clicks'] = randint(10,100)
        course['enrolled'] = randint(10,50)

    return courses


# Because you watch ______
# Most Popular
# Trending now
# Most enrolled
# Based on Psychometric Test
# Best Academic
# Best Non- Academic
# ed2100 picks
# Top Brands
# High Rating
# Top Simulations based Courses
# Top Video baed courses
# Top Games baed courses