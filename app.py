from flask import Flask, request, render_template, jsonify
from chat import get_response
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Rezaalfi12",
            database="chatbot"
        )
        if connection.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to insert conversation into the database
def save_conversation(user_message, bot_response):
    connection = create_db_connection()
    if connection is None:
        print("Failed to connect to the database. Conversation not saved.")
        return
    
    try:
        cursor = connection.cursor()
        query = "INSERT INTO conversations (user_message, bot_response) VALUES (%s, %s)"
        values = (user_message, bot_response)
        cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred while saving conversation")
    finally:
        cursor.close()
        connection.close()

@app.route("/")
def index_get():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    
    # Ensure 'message' key is present
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    text = data.get("message")
    
    # TODO: Validate the text if necessary

    response = get_response(text)

    save_conversation(text, response)  # Save conversation to the database

    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
