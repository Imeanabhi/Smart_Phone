from flask import Flask, render_template, request, flash , redirect 
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'Abhiram',
    'password': 'Abhi@1910',
    'database': 'Smartphones'
}

# Function to get database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to display tables in the database
@app.route('/show_tables')
def show_tables():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        conn.close()
        return render_template('tables.html', tables=tables)
    else:
        flash("Failed to connect to the database.", "error")
        return redirect('/')

# Route to display data from a specific table
@app.route('/show_data/<table_name>')
def show_data(table_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name};")
        data = cursor.fetchall()
        columns = cursor.column_names
        conn.close()
        return render_template('Results.html', columns=columns, data=data, table_name=table_name)
    except Error as e:
        flash(f"Error retrieving data: {e}", "error")
        return redirect('/show_tables')

# Route for the custom query page
@app.route('/Queries', methods=['GET', 'POST'])
def custom_query():
    if request.method == 'POST':
        query = request.form['query']
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            columns = cursor.column_names
            conn.close()
            return render_template('Results.html', columns=columns, data=result, query=query)
        except Error as e:
            flash(f"Error executing query: {e}", "error")
            return redirect('/Queries')
    return render_template('Queries.html')

if __name__ == "__main__":
    app.run(debug=True)
