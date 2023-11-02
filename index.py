import requests
from flask import *
from datetime import timedelta
from gevent import monkey
monkey.patch_all()

class AI:
    def __init__(self, API_BASE_URL: str, API_KEY: str):
        self.API_BASE_URL = API_BASE_URL
        self.headers = {"Authorization": "Bearer " + API_KEY}
        
    def ask(self, question):
        inputs = [
            { "role": "system", "content": "" },
            { "role": "user", "content": question}
        ];
        response = requests.post(self.API_BASE_URL + "@cf/meta/llama-2-7b-chat-int8", headers = self.headers, json = {"messages": inputs}, verify = False)
        return response.json()

app = Flask(__name__)
model = AI("https://api.cloudflare.com/client/v4/accounts/740e559cd504527a29c7c0ee314c6b0a/ai/run/", "FhPn40-YXVmtlmwYObJ9T2-zfEC8l6JnuZHuBvxF")
app.config['SECRET_KEY'] = "FhPn40-YXVmtlmwYObJ9T2-zfEC8l6JnuZHuBvxF"
app.config['PERMENT_SESSION_LIFETIME'] = timedelta(days = 1)

@app.route("/", methods = ["GET"])
def index():
    context = session.get('context')
    if context is None:
        session['context'] = []
        context = []
    return render_template("index.html", context = context)
    
@app.route("/api", methods = ["POST"])
def api():
    question = request.values.get("question")
    result = model.ask(question)
    context = session.get('context')
    if result['success'] == False:
        context.append({"question": question, "answer": "<span style='color: red;'>Error!</span>"})
    else:
        context.append({"question": question, "answer": result['result']['response']})
    session['context'] = context
    return redirect('/')

@app.route("/clear")
def clear():
    session.clear()
    return redirect('/')
