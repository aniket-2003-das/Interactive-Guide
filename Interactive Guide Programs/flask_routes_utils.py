from flask import Flask, request, jsonify
from io import BytesIO
from  datetime import datetime
import os
from utils import *
app = Flask(__name__)







@app.route('/chatbot', methods=['POST'])
def pdf_requester():
    user_query = request.args.get('user_query')
    uploaded_file = request.files['pdf_file']

    # Generate the file path where you want to save the PDF
    save_path = os.path.join('C:\\Users', uploaded_file.filename)

    # Save the uploaded PDF to the specified directory
    uploaded_file.save(save_path)
    
    # Process file and user query with the chatbot function
    pdf_text = parse_pdf(save_path)
    doc_chunks = text_split(pdf_text)
    vectorstore = get_embeddings(doc_chunks, openai_api_key="Your_Api_key")
    condensed_question = get_condensed_question(user_query, chat_history_tuples=[], model_name="gpt-3.5-turbo", openai_api_key="Your_Api_key")
    relevant_sources = get_sources(vectorstore, condensed_question)
    answer = get_answer(relevant_sources, user_query, openai_api_key="Your_Api_key")
    output_text = answer.get("output_text")

    # # Delete the downloaded file after processing
    os.remove(save_path)
    return jsonify({"result": output_text})







# @app.route('/IC/generate_quiz', methods=['POST'])
# def generate_quiz():
    
#     topic = request.args.get('topic')
#     subject_name = request.args.get('subject_name')
#     difficulty_level = request.args.get('difficulty_level')
#     duration = request.args.get('duration')
#     teacherId = request.args.get('teacher_id')
#     current_time = datetime.utcnow()

#     user_query = f"""Create a very detailed teacher\'s quiz for {topic} that focuses on {subject_name} with difficulty level {difficulty_level}, type: MCQ and true/false. If takes no more than {duration} to complete. Return a JSON with double quotes with the following properties: 
#             topic, difficulty_level, duration, subject_name, title, description, teacherId = {teacherId}, created_At = {current_time}, createdBy = "AI", Modified_At = {current_time}, questionImage = Boolean False ,status = Boolean False, visibility = Boolean False, assignedQuizesToClasses = Boolean False type, questions;
#             questions will have the properties as follows:   
#             questionName , option1,  option2, option3, option4, explanation, answer note answer will be the value of the correct option and "type" of question is must field. Explanation will be string with a small explanation of the answer of the question. if question type is True/False give only two options option1 and option2 
#             with value of True and False of option1 and option2  else questionName, option1,  option2, option3, option4,  answer, duration, description."""
#     uploaded_file = request.files['pdf_file']

#     # Generate the file path where you want to save the PDF
#     save_path = os.path.join('C:\\Users', uploaded_file.filename)

#     # Save the uploaded PDF to the specified directory
#     uploaded_file.save(save_path)
    
#     # Process file and user query with the chatbot function
#     pdf_text = parse_pdf(save_path)
#     doc_chunks = text_split(pdf_text)
#     vectorstore = get_embeddings(doc_chunks, openai_api_key="Your_Api_key")
#     condensed_question = get_condensed_question(user_query, chat_history_tuples=[], model_name="gpt-3.5-turbo", openai_api_key="Your_Api_key")
#     relevant_sources = get_sources(vectorstore, condensed_question)
#     answer = get_answer(relevant_sources, user_query, openai_api_key="Your_Api_key")
#     output_text = answer.get("output_text")

#     # # Delete the downloaded file after processing
#     os.remove(save_path)
#     return jsonify({"result": output_text})



# @app.route('/IC/flashCards', methods=['POST'])
# def flash_cards():
    


#     user_query = """Please create a glossary of key terms for the provided content. The glossary should include definitions for each term, 
#                     and the terms should be directly related to the main topic of the content. Return a JSON with double quotes with the following properties:
#                     Word, Meaning;"""
#     uploaded_file = request.files['pdf_file']

#     # Generate the file path where you want to save the PDF
#     save_path = os.path.join('C:\\Users', uploaded_file.filename)

#     # Save the uploaded PDF to the specified directory
#     uploaded_file.save(save_path)
    
#     # Process file and user query with the chatbot function
#     pdf_text = parse_pdf(save_path)
#     doc_chunks = text_split(pdf_text)
#     vectorstore = get_embeddings(doc_chunks, openai_api_key="Your_Api_key")
#     condensed_question = get_condensed_question(user_query, chat_history_tuples=[], model_name="gpt-3.5-turbo", openai_api_key="Your_Api_key")
#     relevant_sources = get_sources(vectorstore, condensed_question)
#     answer = get_answer(relevant_sources, user_query, openai_api_key="Your_Api_key")
#     output_text = answer.get("output_text")

#     # # Delete the downloaded file after processing
#     os.remove(save_path)
#     return jsonify({"result": output_text})



if __name__ == '__main__':
    app.run(debug=True)













