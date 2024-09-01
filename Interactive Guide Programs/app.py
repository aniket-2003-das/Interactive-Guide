from flask import Flask, request,jsonify
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from google_images_search import GoogleImagesSearch
import wolframalpha
from googleapiclient.discovery import build
# from utils import *
# from url_main import *
# from webquery import *
from webquery import *



# Load environment variables from .env file
load_dotenv()

# Access environment variables perplexity
ppxl_api_key = os.getenv("ppxl_api_key")
url_ppxl = os.getenv("url_ppxl")


#  google image search
api_key_gsi = os.getenv("api_key_gsi")
cse_id_gsi = os.getenv("cse_id_gsi")


# Get env variables for google image search
DK = os.environ.get('DEVELOPER_KEY')
CX = os.environ.get('CX')


app = Flask(__name__)

@app.route("/AI-tutor/ppxl-answer", methods=['POST'])
def AI_tutor():
    data = request.get_json()
    doubts_left = data.get('doubts_left')
    subject = data.get('subject')
    user_question = data.get('user_question')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    payload = {
        "model": "pplx-70b-online",
        "messages": [
            {
                "role": "system",
                "content": f"You are a Classroom bot for {subject} subject. Be precise and concise."
            },
            {
                "role": "user",
                "content": f"{user_question}"
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {ppxl_api_key}"
    }
    response = requests.post(url_ppxl, json=payload, headers=headers)
    data = response.json()
    ai_tutor_json = {
        "answer": data['choices'][-1]['message']['content'],
        "doubts_left": doubts_left,
        "timestamp": timestamp,
        "subject": subject,
        "question": user_question
    }
    # print(ai_tutor_json)
    return ai_tutor_json

@app.route("/AI/general-query", methods=['POST'])
def AI_generaral_query():
    data = request.get_json()
    user_query = data.get('query')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    payload = {
        "model": "pplx-70b-online",
        "messages": [
            {
                "role": "system",
                # "content": f"you are a helping smart chat bot to answer any query"
                 "content": f"Explore and explain a concept, problem, or scenario of your choice. Provide a detailed response supported by accurate information or calculations where applicable. Your explanation should be structured and accessible to someone learning about the topic for the first time. Use appropriate formulas, theories, or principles to support your explanation."
            },
            {
                "role": "user",
                "content": f"{user_query}"
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {ppxl_api_key}"
    }
    response = requests.post(url_ppxl, json=payload, headers=headers)
    data = response.json()
    ai_tutor_json = {
        "answer1": data['choices'][-1]['message']['content'],
        # "doubts_left": doubts_left,
        # "timestamp": timestamp,
        # "subject": subject,
        # "question": user_question
    }
    # print(ai_tutor_json)
    return ai_tutor_json

@app.route("/AI/check-subject", methods=['POST'])
def AI_subject_check():
    data = request.get_json()
    user_query = data.get('query')
    subject = data.get('subject')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    payload = {
        "model": "llama-2-70b-chat",
        "messages": [
            {
                "role": "system",
                "content": f"You are a helping bot to check the subject and be strict to return one word answer only which is true or either false ,make sure it will  without any explantions ,i am providing you a subject with name {subject} and query which is {user_query} .if query belongs to provided subject  return true only otherwise return false only. Be precise and concise while comapring query to subject."
            },
            {
                "role": "user",
                "content": f"{user_query}"
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {ppxl_api_key}"
    }
    response = requests.post(url_ppxl, json=payload, headers=headers)
    data = response.json()
    print("dfsdfs",data['choices'][-1])
    ai_tutor_json =data['choices'][-1]['message']['content']
    # ai_tutor_json = {
    #     "answer1": data['choices'][-1]['message'],
    #     "anser2":data
    #     # "doubts_left": doubts_left,
    #     # "timestamp": timestamp,
    #     # "subject": subject,
    #     # "question": user_question
    # }
   
    return ai_tutor_json


@app.route("/AI-tutor/google_image_search", methods=['POST'])
def fetch_image_urls():
    # create google images search - object
    gis = GoogleImagesSearch(DK, CX)
    criteria = request.json
    # define search params:
    _search_params = {
        "q": criteria.get("query"),
        "num": 4,
        "safe": "high",
        "fileType": "jpg",
        "imgType": "photo",
        "rights": "cc_publicdomain"
        # free for use by anyone for any purpose without restriction under copyright law
    }
    # perform the search
    gis.search(search_params=_search_params)
    # retrieve image URLs
    image_urls = [image.url for image in gis.results()]
    # Create a dictionary with a single key "urls" and a list of image URLs as its value
    result_dict = {"urls": image_urls}
    # Return the dictionary as JSON
    return jsonify(result_dict)



@app.route("/AI-tutor/wolfram_answer", methods=['POST'])
def get_wolfram_response():
    data = request.get_json()
    query = data.get('query')

    api_key = os.getenv("api_key_wolfram")
    client = wolframalpha.Client(api_key)

    res = client.query(query)
    answer = next(res.results).text

    response = {
        'query': query,
        'answer': answer
    }
    return jsonify(response)



@app.route("/AI-tutor/google-results", methods=['POST'])
def search():
    # Get the query from the JSON body of the request
    data = request.get_json()
    query = data.get('query')
    # Check if the query is provided in the JSON body
    if not query:
        return jsonify({'error': 'Query parameter is missing'}), 400
    # Build the custom search service
    service = build('customsearch', 'v1', developerKey=api_key_gsi)
    # Make the API request
    res = service.cse().list(q=query, cx=cse_id_gsi).execute()
    # Parse the JSON response
    search_results = res.get('items', [])
    # Process the first 4 search results
    limited_results = []
    for index, result in enumerate(search_results[:4]):
        title = result.get('title', '')
        link = result.get('link', '')
        snippet = result.get('snippet', '')
        # Create a dictionary for the current result
        result_data = {
            'query': query,
            'title': title,
            'link': link,
            'snippet': snippet
        }
        limited_results.append(result_data)
    # Create a JSON response
    json_result = {'query': query, 'results': limited_results}
    return jsonify(json_result)





# @app.route('/IG', methods=['POST'])
# def Summary():

#     provided_text = """In the last chapter we developed the concepts of position,
#     displacement, velocity and acceleration that are needed to
#     describe the motion of an object along a straight line. We
#     found that the directional aspect of these quantities can be
#     taken care of by + and – signs, as in one dimension only two
#     directions are possible. But in order to describe motion of an
#     object  in  two  dimensions  (a  plane)  or  three  dimensions
#     (space),  we  need  to  use  vectors  to  describe  the  above-
#     mentioned physical quantities.  Therefore, it is first necessary
#     to learn the language of vectors. What is a vector? How to
#     add, subtract and multiply vectors ? What is the result of
#     multiplying a vector by a real number ? We shall learn this
#     to  enable  us  to  use  vectors  for  defining  velocity  and
#     acceleration in a plane. We then discuss motion of an object
#     in a plane.  As a simple case of motion in a plane, we shall
#     discuss motion with constant acceleration and treat in detail
#     the projectile motion. Circular motion is a familiar class of
#     motion that has a special significance in daily-life situations.
#     We shall discuss uniform circular motion in some detail.
#     The equations developed in this chapter for motion in a
#     plane can be easily extended to the case of three dimensions."""



#     user_query1 = "Give a complete summary about the provided content."

#     user_query2 = """Please create a glossary of key terms for the provided content. The glossary should include definitions for each term, 
#                     and the terms should be directly related to the main topic of the content. Return a JSON with double quotes with the following properties:
#                     Word, Meaning,
#                     Word should only contain words from the provided text,
#                     Meaning will be string with an explanation of the word of the provided content."""
    
#     user_query3 = """Please create a set of flash cards based on the provided content. Each flash card should include a question on one side, 
#         and the answer or response on the other side. The questions should be designed to test understanding of the key concepts in the content.
#         Return a JSON with double quotes with the following properties:
#         Question, Response,
#         Questions should only contain context from the provided content in an interactive way,
#         Response will be string with an explanation or answer of the Question from the provided content in an interactive way."""
    
#     user_query4 = f"""Create a very detailed teacher\'s quiz of 5 questions for a topic that focuses on subject_name with a title, type: MCQ and true/false. If takes no more than 10 to complete. 
#         Return a JSON with double quotes with the following properties: 
#         topic, duration, subject_name, title, description, questions;
#         The topic, subject_name, title and description will be based on the Provided comtent.
#         questions will have the properties as follows:   
#         questionName , option1,  option2, option3, option4, explanation, answer note answer will be the value of the correct option and "type" of question is must field. 
#         Explanation will be string with a small explanation of the answer of the question. if question type is True/False give only two options option1 and option2 
#         with value of True and False of option1 and option2  else questionName, option1,  option2, option3, option4,  answer, duration, description."""


#     doc_chunks = text_split(provided_text)
#     vectorstore = get_embeddings(doc_chunks, openai_api_key="Your_API_KEY")




#     condensed_question1 = get_condensed_question(user_query1, chat_history_tuples=[], model_name="gpt-3.5-turbo", openai_api_key="Your_API_Key")
#     relevant_sources1 = get_sources(vectorstore, condensed_question1)
#     answer1 = get_answer(relevant_sources1, user_query1, openai_api_key="Your_API_Key")

#     condensed_question2 = get_condensed_question(user_query2, chat_history_tuples=[], model_name="gpt-3.5-turbo", openai_api_key="Your_API_Key")
#     relevant_sources2 = get_sources(vectorstore, condensed_question2)
#     answer2 = get_answer(relevant_sources2, user_query2, openai_api_key="Your_API_Key")

#     condensed_question3 = get_condensed_question(user_query3, chat_history_tuples=[], model_name="gpt-3.5-turbo", openai_api_key="Your_API_Key")
#     relevant_sources3 = get_sources(vectorstore, condensed_question3)
#     answer3 = get_answer(relevant_sources3, user_query3, openai_api_key="Your_API_Key")

#     condensed_question4 = get_condensed_question(user_query4, chat_history_tuples=[], model_name="gpt-3.5-turbo", openai_api_key="Your_API_Key")
#     relevant_sources4 = get_sources(vectorstore, condensed_question4)
#     answer4 = get_answer(relevant_sources4, user_query4, openai_api_key="Your_API_Key")


#     return jsonify({"summary": answer1,
#                     "glossary": answer2,
#                     "FlashCards": answer3,
#                     "Quiz": answer4})




@app.route("/url", methods=['POST'])
def url():
    openai_api_key = "Your_API_Key"
    web_query = WebQuery(openai_api_key=openai_api_key)


    data = request.get_json()
    url = data.get('url')
    url = "https://youtu.be/9hb_0TZ_MVI?si=wHEAxY_4GH92BVAg"

    # question = data.get('query')


    user_query1 = "Give a complete summary about the provided content."

    user_query2 = """Please create a glossary of key terms for the provided content. The glossary should include definitions for each term, 
                    and the terms should be directly related to the main topic of the content. Return a JSON with double quotes with the following properties:
                    Word, Meaning,
                    Word should only contain words from the provided text,
                    Meaning will be string with an explanation of the word of the provided content."""
    
    user_query3 = """Please create a set of flash cards based on the provided content. Each flash card should include a question on one side, 
        and the answer or response on the other side. The questions should be designed to test understanding of the key concepts in the content.
        Return a JSON with double quotes with the following properties:
        Question, Response,
        Questions should only contain context from the provided content in an interactive way,
        Response will be string with an explanation or answer of the Question from the provided content in an interactive way."""
    
    user_query4 = f"""Create a very detailed teacher\'s quiz of 5 questions for a topic that focuses on subject_name with a title, type: MCQ and true/false. If takes no more than 10 to complete. 
        Return a JSON with double quotes with the following properties: 
        topic, duration, subject_name, title, description, questions;
        The topic, subject_name, title and description will be based on the Provided comtent.
        questions will have the properties as follows:   
        questionName , option1,  option2, option3, option4, explanation, answer note answer will be the value of the correct option and "type" of question is must field. 
        Explanation will be string with a small explanation of the answer of the question. if question type is True/False give only two options option1 and option2 
        with value of True and False of option1 and option2  else questionName, option1,  option2, option3, option4,  answer, duration, description."""


    web_query.ingest(url)



    answer1 = web_query.ask(user_query1)
    answer2 = web_query.ask(user_query2)
    answer3 = web_query.ask(user_query3)
    answer4 = web_query.ask(user_query4)
    
    return jsonify({"summary": answer1,
                    "glossary": answer2,
                    "FlashCards": answer3,
                    "Quiz": answer4})







if __name__ == '__main__':
    app.run()
