import requests
from explanation_extraction import Quiz_help_json_string

ppxl_api_key = "Your_API_key"
url_ppxl = "https://api.perplexity.ai/chat/completions"


#  give rescource links, related video links and related image links for each query along answwer
def suppliment_text():
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": f"You are a suppliment generator for a open book quiz. Take topic = types of bond in atoms and molecules, subject = chemistry."
            },
            {
                "role": "user",
                "content": "Generate text material for the suppliment."
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
    text_content = {
        "answer": data['choices'][-1]['message']['content']
    }
    print(text_content)
    return text_content


def suppliment_video():
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": f"You are a video suppliment generator for a open web quiz. Take topic = types of bond in atoms and molecules, subject = chemistry"
            },
            {
                "role": "user",
                "content": "Provide a list of video url links in a json array for preparation material for the quiz."
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
    video_links = {
        "answer": data['choices'][-1]['message']['content']
    }
    print(video_links)

suppliment_text()

suppliment_video()