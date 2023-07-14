from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET']) # indicate the route you want to create. / is the default route
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    # read values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # load values from .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # indicate that we want to translate. API version 3.0 
    path = '/translate?api-version=3.0'
    # add target language parameter
    target_language_parameter = '&to=' + target_language
    # create the full url
    constructed_url = endpoint + path + target_language_parameter

    # set up header info, which includes subscripiton key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # create the body of the request with the text to be translated
    body = [{ 'text': original_text}]

    # make the call using post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # retrieve the json response
    translator_response = translator_request.json()
    # retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']

    # call render template, passing the translated text, origina text and target language to template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

