from google_images_search import GoogleImagesSearch
from dotenv import load_dotenv
import os


# load the API key and CX code from .env file
if os.path.exists(".env"):
  load_dotenv()
else:
  print(".env file missing, please create one with your API and CX")

# create an 'ims' sub directory if it doesn't already exists
if not os.path.exists('images/'):
  os.mkdir('images/')
spath = 'images/'

# Get env variables
DK = os.environ.get('DEVELOPER_KEY')
CX = os.environ.get('CX')

# custom progressbar function
def my_progressbar(url, progress):
    print(url + " " + progress + "%")

# create google images search - object
gis = GoogleImagesSearch(DK, CX, progressbar_fn=my_progressbar)

def fetch_images(searchfor):
  # using contextual mode (Curses)
  with GoogleImagesSearch(DK, CX) as gis:
    # define search params:
    _search_params = {"q": searchfor, 
        "num": 5, 
        "safe": "high", 
        "fileType": "jpg",
        "imgType": "photo",
        "rights": "cc_publicdomain" 
        #  free for use by anyone for any purpose without restriction under copyright law
        }
    gis.search(search_params=_search_params, path_to_dir=spath)

  print("Finished!")



search_term = "Rotational motion"
fetch_images(search_term)