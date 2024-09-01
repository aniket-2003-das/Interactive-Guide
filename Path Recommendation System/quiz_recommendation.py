import requests
from explanation_extraction import Quiz_help_json_string

ppxl_api_key = "Your_API_key"
url_ppxl = "https://api.perplexity.ai/chat/completions"


#  give rescource links, related video links and related image links for each query along answwer
def Quiz_2():
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": f"You are a Quiz generator for a open book quiz."
            },
            {
                "role": "user",
                "content": f"""Create a very detailed json quiz using {Quiz_help_json_string} as reference for explanations. Give title = types of bond, topic = types of bond in atoms and molecules, subject = chemistry, type: MCQ and true/false. If takes no more than 10 minutes to complete.
                Return a JSON with double quotes that will have the properties as follows: title, topic, duration, subjectName, description, questions; 
                questions will have the properties as follows: questionName, type , option1,  option2, option3, option4, explanation, answer, answer will be the field value of the correct option.
                Explanation will be string with a small explanation of the answer of the question.
                if question type is True/False give only two options option1 and option2 with value of True and False of option1 and option2  else questionName, option1,  option2, option3, option4,  answer, duration, description.
            """
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
    answer = data['choices'][-1]['message']['content']
    print(answer)
    return answer


Quiz_2()