from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'campustradedb'  # Replace with your MySQL database name

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('landing_page.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Create MySQL cursor
        cur = mysql.connection.cursor()

        # Insert user into database
        cur.execute("INSERT INTO users (first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                    (first_name, last_name, username, email, password))

        # Commit to database
        mysql.connection.commit()

        # Close connection
        cur.close()

        return redirect('/login.html')

    return render_template('signup.html')

@app.route("/login", methods=["POST"])
def login_user():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Create MySQL cursor
        cur = mysql.connection.cursor()

        # Check if the user exists in the database
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        if user:
            # User exists, store user information in session

            # Redirect to a dashboard or profile page after successful login
            return redirect('/')
        else:
            # User not found or incorrect password, redirect to login page with an error message
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
