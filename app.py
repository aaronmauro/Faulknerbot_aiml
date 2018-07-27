from flask import Flask, render_template, jsonify, request, make_response
from search import search, link
import os
import aiml


BRAIN_FILE = "brain.dump" #absolute path is absolutely necessary

k = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    k.loadBrain(BRAIN_FILE)

else:
    k.bootstrap(learnFiles="data/std-startup.aiml", commands="load aiml b")
    k.saveBrain(BRAIN_FILE)

k.setBotPredicate('master','Dr. Aaron Mauro')

k.setBotPredicate('botmaster','Dr. Aaron Mauro')
k.setBotPredicate('religion','atheism')
k.setBotPredicate('name','Faulknerbot')

k.setBotPredicate('BOTNAME','Faulknerbot')

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")
@app.route("/about")
def about():
	return render_template("about.html")

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

if __name__ == "__main__":
    app.run()
