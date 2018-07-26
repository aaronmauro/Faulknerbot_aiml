from flask import Flask, render_template, request
from flask import jsonify
from search import search, link
import os
import aiml

BRAIN_FILE="brain.dump"

k = aiml.Kernel()

# To increase the startup speed of the bot it is
# possible to save the parsed aiml files as a
# dump. This code checks if a dump exists and
# otherwise loads the aiml from the xml files
# and saves the brain dump.
if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)

k.setBotPredicate('master','Dr. Aaron Mauro')

k.setBotPredicate('botmaster','Dr. Aaron Mauro')
k.setBotPredicate('religion','atheism')
k.setBotPredicate('name','Faulknerbot')

k.setBotPredicate('BOTNAME','Faulknerbot')

app = Flask(__name__,static_url_path="/static")

#############

@app.route('/message', methods=['POST'])
def reply():
    try:
        while True:
            input_text = request.form['msg']
            if input_text.lower() == "save":
                k.saveBrain(BRAIN_FILE)
                return jsonify( { 'text': "Saving conversation..." } )
            else:
                response = k.respond(input_text)
            return jsonify( { 'text': response } )
    except Exception as e:
        return jsonify( {'text': str(e) } ) #for debugging


@app.route('/_searcher', methods=['POST'])
def searcher():
    try:
        input_text = request.form['msg']
        response = k.respond(input_text)
        return jsonify( { 'text': search(response[:8]) + link(response[:8]) } )
    except Exception as e:
        return jsonify( {'text': str(e) } )#for debugging

@app.route("/")
def index():
        return render_template("index.html")

# start app
if (__name__ == "__main__"):
    app.run()