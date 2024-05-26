from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import sqlite3
from openai import AzureOpenAI
from gptapi import api, endpoint

app = Flask(__name__)
app.secret_key = 'gitamchatbot'

link = 'www.gitam.edu'
client = AzureOpenAI(azure_endpoint=endpoint, azure_deployment="college", api_key=api, api_version="2024-02-01")

def init_sqlite_db():
    conn = sqlite3.connect('chat.db')
    print("Opened database successfully")

    conn.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            response TEXT,
            status TEXT DEFAULT 'unresolved'
        )
        ''')
    print("Tables created successfully")
    conn.close()

init_sqlite_db()

@app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = "admin"
        p = "admin"

        if username==u and password==p:  # Checking hashed password
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            return "Username or Password is incorrect"

    return render_template('login.html')

@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_history")
    unresolved_chats = cursor.fetchall()
    conn.close()
    return render_template('admin.html', chats=unresolved_chats)


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chatbot/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        session['name'] = name
        session['email'] = email
        return redirect(url_for('chat_interface'))
    return render_template('new_email.html')


@app.route('/chat/', methods=['GET', 'POST'])
def chat_interface():
    if 'name' in session and 'email' in session:
        if request.method == 'POST':
            data = request.json
            user_query = data.get('query', '')
            status = data.get('status', 'resolved')

            if status == 'unresolved':
                save_chat_history(session['name'], session['email'], user_query, "", "unresolved")
                return jsonify({"response": "Your query has been forwarded to an admin for further assistance."})

            response_text = get_llm_response(user_query)
            save_chat_history(session['name'], session['email'], user_query, response_text, status)
            return jsonify({"response": response_text})

        return render_template('chat.html')

    return redirect(url_for('chat'))

def get_llm_response(user_query):
    if not session.get('welcome_message_sent'):
        welcome_message = (
            f"Welcome to HeyBuddy! I'm here to help you find information about GITAM. Here are some popular options you can choose from:\n\n"
            f"a. Admissions\n"
            f"b. Courses Offered\n"
            f"c. Campus Facilities\n"
            f"d. Other\n\n"
            f"Please select an option or type your specific query."
        )
        session['welcome_message_sent'] = True
        return welcome_message

    messages = [
        {"role": "system", "content": f'You are an AI assistant named "HeyBuddy" that helps people find information for a college/campus/university/school detail by asking and presenting basic queries as a chatbot using the institution website. link: {link}'},
        {"role": "user", "content": user_query}
    ]

    response = client.chat.completions.create(
        model="college",
        messages=messages,
        max_tokens=800,
        temperature=0.2,
    )

    response_text = response.choices[0].message.content
    return response_text

def save_chat_history(name, email, messages, response_text, status):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (name, email, message, response, status) VALUES (?, ?, ?, ?, ?)",
                   (name, email, messages, response_text, status))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
