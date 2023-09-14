from flask import Flask, render_template, request, redirect, flash, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong, random value

# MongoDB setup
client = MongoClient('mongodb+srv://21z229:mithu@cluster0.q3drxsx.mongodb.net/')
db = client['complaints']
complaints_collection = db['complaints']

# Define the admin username and password
admin_username = "SU"
admin_password = "ob23-24"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle complaint submission
        complaint_text = request.form['complaint']
        complaints_collection.insert_one({
            'text': complaint_text
        })
        flash('Complaint submitted successfully.')

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            return redirect('/complaints')
        else:
            flash('Invalid login. Please check your credentials.')

    return render_template('login.html')

@app.route('/complaints')
def complaints():
    if session['logged_in']:
        all_complaints = list(complaints_collection.find())
        return render_template('complaints.html', complaints=all_complaints)
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)



