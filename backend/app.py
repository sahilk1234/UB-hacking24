from flask import Flask, request, jsonify, session
from auth0 import auth_required, auth0, init_auth0
from db import mongo, init_db
from symptom import get_possible_conditions
from chatbot import get_diagnosis

app = Flask(__name__)
app.config["SECRET_KEY"] = "O3T9ILZQZR4KW4V7"
app.config["MONGO_URI"] = "mongodb+srv://sgupta98mnit:O3T9ILZQZR4KW4V7@cluster0.awihk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize database and Auth0
init_db(app)
init_auth0(app)

# Routes
@app.route('/symptom_checker', methods=['POST'])
@auth_required
def symptom_checker():
    symptoms = request.json.get("symptoms", [])
    conditions = get_possible_conditions(symptoms)
    return jsonify({"possible_conditions": conditions})

@app.route('/chatbot', methods=['POST'])
@auth_required
def chatbot():
    user_input = request.json.get("input", "")
    diagnosis = get_diagnosis(user_input)
    return jsonify({"diagnosis": diagnosis})

@app.route('/user/profile', methods=['GET'])
@auth_required
def user_profile():
    user = mongo.db.users.find_one({"user_id": session["user_id"]})
    return jsonify(user)

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

@app.route('/callback')
def callback():
    auth0.authorize_access_token()
    session['user_id'] = auth0.get('userinfo')['sub']
    return "Logged in successfully!"

if __name__ == "__main__":
    app.run(debug=True)
