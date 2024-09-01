import json
from Quiz1 import Quiz1_json

# Load the JSON string into a dictionary
given_quiz_json_dict = json.loads(Quiz1_json)

# Extract explanations from the quiz data
Quiz_help = {}
for idx, question in enumerate(given_quiz_json_dict['reportdata']['questions'], 1):
    explanation_key = f'explanation{idx}'
    Quiz_help[explanation_key] = question['explanation']

# Create a JSON object with explanations
explanations_json = {
    'explanations': Quiz_help
}

# Convert the JSON object to a string
Quiz_help_json_string = json.dumps(explanations_json, indent=2)


