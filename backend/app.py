from datetime import datetime
import traceback
import uuid
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from flask import Flask, request, jsonify, session, redirect, url_for
from auth0 import auth_required, init_auth0, auth0  # Ensure auth0 is imported
from db import init_db, get_db_connection
from symptom import get_possible_conditions
from chatbot import get_diagnosis
from flask_cors import CORS


from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_session import Session

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)  # This will allow all origins by default
# Initialize database and Auth0
init_db()
auth0 = init_auth0(app)
print("Hisa")
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SECRET_KEY"] = env.get("0b43551f68bfbe8e09894719197eeec3db967be9e746cba7ab20a79cfbc64058")


Session(app)

@app.route('/start_chat', methods=['POST'])
# @auth_required
def start_chat():
    """
    Initiates a new chat session by generating a unique chat_id.
    """

    user_id = request.json.get("userId", "")
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    # Generate a unique chat_id for the conversation
    chat_id = str(uuid.uuid4())

    # Insert the new conversation into the database
    current_time = datetime.now()

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO conversations (chat_id, user_uuid, conversation_name, started_at)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (chat_id, user_id, "", current_time)
                )
                conn.commit()
        return jsonify({"chatId": chat_id})

    except Exception as e:
        print(e)
        print(f"Error starting chat: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/check', methods=['POST'])
def chat():
    """
    Handles interactive chat requests by taking user input, generating a response,
    and logging the conversation to the database with chat_id.
    """
    print("stat")

    message_input = request.json.get("messageInput", "")
    chat_id = request.json.get("chatId", "")

    if not chat_id or not message_input:
        return jsonify({"error": "Missing chat ID or input"}), 400

    try:
        # Generate a diagnosis or response based on the user input
        print("stat")
        response_text = get_diagnosis(message_input,[])
        # response_text="Please provide more info"
        # Store message in the database
        # with get_db_connection() as conn:
        #     with conn.cursor() as cur:
        #         # Check if it's the first message of the conversation to set the name
        #         cur.execute(
        #             "SELECT COUNT(*) FROM messages WHERE chat_id = %s",
        #             (chat_id,)
        #         )
        #         message_count = cur.fetchone()[0]

        #         # If this is the first message, update conversation name
        #         if message_count == 0:
        #             truncated_message = message_input[:50] + "..." if len(message_input) > 50 else message_input
        #             cur.execute(
        #                 "UPDATE conversations SET conversation_name = %s WHERE chat_id = %s",
        #                 (truncated_message, chat_id)
        #             )

        #         # Insert user's message and bot's response into the messages table
        #         cur.execute(
        #             """
        #             INSERT INTO messages (chat_id, sender, message_text, diagnosis)
        #             VALUES (%s, %s, %s, %s);
        #             """,
        #             (chat_id, 'user', message_input, None)
        #         )
        #         cur.execute(
        #             """
        #             INSERT INTO messages (chat_id, sender, message_text, diagnosis)
        #             VALUES (%s, %s, %s, %s);
        #             """,
        #             (chat_id, 'bot', response_text, response_text)
        #         )
        #         conn.commit()
                
        return jsonify({"response": response_text})


    except Exception as e:
        print(f"Error during chat handling: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route('/get_chat', methods=['GET'])
# @auth_required
def conversation_history():
    """
    Retrieves the conversation history for a specific chat_id.
    """
    chat_id = request.args.get("chatId")

    if not chat_id:
        return jsonify({"error": "Chat ID is required"}), 400

    try:
        # Fetch conversation history from PostgreSQL
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT sender, message_text, diagnosis, created_at
                    FROM messages
                    WHERE chat_id = %s
                    ORDER BY created_at ASC;
                    """,
                    (chat_id,)
                )
                conversation = cur.fetchall()

        # Return conversation history
        history = [{"sender": row[0], "message_text": row[1], "diagnosis": row[2], "created_at": row[3]} for row in conversation]
        return jsonify({"history": history})

    except Exception as e:
        print(f"Error fetching conversation history: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/list_chats', methods=['GET'])
# @jwt_required
def list_chats():
    """
    Lists all chats for the authenticated user.
    """
    user_id = request.args.get("userId")
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    try:
        # Fetch all chat IDs, names, and timestamps associated with the user
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT chat_id, conversation_name, started_at, ended_at
                    FROM conversations
                    WHERE user_uuid = %s
                    ORDER BY started_at DESC;
                    """,
                    (user_id,)
                )
                chats = cur.fetchall()

        # Format the response
        chat_list = [
            {
                "chat_id": row[0],
                "conversation_name": row[1] or "Unnamed Conversation",  # Default if name is missing
                "started_at": row[2],
                "ended_at": row[3]
            }
            for row in chats
        ]
        return jsonify({"chats": chat_list})

    except Exception as e:
        print(f"Error fetching chat list: {e}")
        return jsonify({"error": "Internal server error"}), 500



@app.route('/user/profile', methods=['GET'])
@auth_required
def user_profile():
    user=[]
    # user = mongo.db.users.find_one({"user_id": session["user"]["sub"]})
    return jsonify(user) if user else jsonify({"error": "User not found"}), 404

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    token = auth0.authorize_access_token()  # Exchange authorization code for a token
    session["user"] = token  # Store the token in session
    return redirect("http://localhost:3000/profile?token=" + token['id_token'])

print("Starting Flask app...")

if __name__ == "__main__":
    print("Running app...")
    app.run(host="0.0.0.0", port=5000, debug=True)