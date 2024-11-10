from flask import Flask, request, jsonify, session, redirect, url_for
from auth0 import auth_required, init_auth0, auth0
from db import mongo, init_db
from symptom import get_possible_conditions
from chatbot import get_diagnosis

app = Flask(__name__)
app.config["SECRET_KEY"] = "O3T9ILZQZR4KW4V7"
app.config["MONGO_URI"] = "mongodb+srv://sgupta98mnit:O3T9ILZQZR4KW4V7@cluster0.awihk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize database and Auth0
init_db(app)
auth0 = init_auth0(app)



app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)

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
    user = mongo.db.users.find_one({"user_id": session["user"]["sub"]})
    return jsonify(user) if user else jsonify({"error": "User not found"}), 404

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    token = auth0.authorize_access_token()  # Exchange authorization code for a token
    session["user"] = token  # Store the token in session
    return redirect("http://localhost:3000/profile?token=" + token['id_token'])

if __name__ == "__main__":
    app.run(debug=True)
