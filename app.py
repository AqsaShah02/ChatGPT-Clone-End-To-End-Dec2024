from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import requests
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
AIXPLAIN_API_KEY = os.getenv("AIXPLAIN_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
MODEL_ID = os.getenv("MODEL_ID")
POST_URL = os.getenv("POST_URL")

headers = {
    "x-api-key": AIXPLAIN_API_KEY,
    "Content-Type": "application/json"
}

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)
print("Connected to DB")

@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    mychats = [chat for chat in chats]
    print(mychats)
    return render_template("index.html", myChats=mychats)

def fetch_answer_from_model(question):
    data = {"text": question}
    try:
        response = requests.post(POST_URL, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        request_id = response_data.get("requestId")
        if not request_id:
            return None

        get_url = f"https://models.aixplain.com/api/v1/data/{request_id}"
        while True:
            get_response = requests.get(get_url, headers=headers)
            get_response.raise_for_status()
            result = get_response.json()
            if result.get("completed"):
                return result.get("data")
            time.sleep(5)

    except requests.RequestException as e:
        print(f"Error while communicating with the model API: {e}")
        return None

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        print(chat)

        if chat:
            data = {"result": chat["answer"]}
            return jsonify(data)
        else:
            answer = fetch_answer_from_model(question)
            if answer:
                mongo.db.chats.insert_one({"question": question, "answer": answer})
                data = {"result": answer}
            else:
                data = {"result": "Sorry, I don't know the answer to that question."}
            return jsonify(data)

    data = {"result": "Hello There"}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
