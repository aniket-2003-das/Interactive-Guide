from flask import Flask, jsonify
import os
from google_images_search import GoogleImagesSearch
from dotenv import load_dotenv
import os
from flask import request



load_dotenv()

# Get env variables
DK = os.environ.get('DEVELOPER_KEY')
CX = os.environ.get('CX')


app = Flask(__name__)



@app.route("/student/recommend", methods=['POST'])
# @app.route("/")
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

    # Create a dictionary with numerical indices as keys and URLs as values
    result_dict = {f"URL {i + 1} ": url for i, url in enumerate(image_urls)}

    # Return the dictionary as JSON
    return jsonify(result_dict)


    

if __name__ == '__main__':
    app.run()
















 
