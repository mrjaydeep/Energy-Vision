from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import psycopg2  # Change from MySQLdb to psycopg2

app = Flask(__name__)
app.secret_key = '02092002'

# PostgreSQL configuration
DB_HOST = 'localhost'
DB_USER = 'postgres'  
DB_PASSWORD = 'Jaydeep13'  
DB_NAME = 'energy'  
DB_PORT = '5432'  

# Connect to PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Load your dataset
try:
    df = pd.read_csv("Combined12.csv")  # Replace with the correct path
except FileNotFoundError:
    print("CSV file not found. Please check the file path.")
    exit(1)

# Data Preprocessing
if not pd.api.types.is_numeric_dtype(df['normalized_label']):
    df['normalized_label'] = pd.Categorical(df['normalized_label']).codes

X = df[["Pressure", "global_radiation", "temp_mean(c)", "temp_min(c)", "temp_max(c)", "Wind_Speed", "Wind_Bearing"]]
y = df["normalized_label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

classifier = RandomForestClassifier()
classifier.fit(X_train_scaled, y_train)

@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        
        if email_exists(email):
            error = "Email already exists. Please use a different email."
            return render_template('signup.html', error=error)
        
        db = connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO Users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",
                           (firstname, lastname, email, password))
            db.commit()
            cursor.close()
            db.close()
        else:
            return "Database connection failed"

        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.form
        features = [
            float(data['pressure']),
            float(data['globalRadiation']),
            float(data['tempMean']),
            float(data['tempMin']),
            float(data['tempMax']),
            float(data['windSpeed']),
            float(data['windBearing'])
        ]
        user_features_scaled = scaler.transform([features])
        predicted_label = classifier.predict(user_features_scaled)
        
        labels = {
            0: "No energy",
            1: "Solar energy",
            2: "Wind energy",
            3: "Both solar and wind energy"
        }
        predicted_label_description = labels.get(predicted_label[0], "Unknown")
        
        return render_template('result.html', predicted_label=predicted_label_description)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            db = connect_db()
            if db:
                cursor = db.cursor()
                cursor.execute("SELECT email, password FROM Users WHERE email = %s", (email,))
                user = cursor.fetchone()

                if user and user[1] == password:
                    session['logged_in'] = True
                    return render_template('model.html')
                else:
                    message = 'Invalid Email or Password!!'
                    return render_template('login.html', message=message)
            else:
                return "Database connection failed"
        except Exception as e:
            return f"An error occurred: {str(e)}"
        finally:
            if db:
                cursor.close()
                db.close()
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

def email_exists(email):
    db = connect_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        db.close()
        return user is not None
    return False

if __name__ == '__main__':
    app.run(debug=False)
