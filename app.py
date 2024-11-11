import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, jsonify, render_template_string, flash, session, abort

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rat</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
        }
        h1 {
            font-size: 3em;
            margin-top: 20px;
        }
        button {
            font-size: 1.2em;
            margin: 10px;
            padding: 10px 20px;
        }
        .rat-image {
            width: 80%;
            max-width: 600px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Lucas and Hannah's Rat Sighting Website</h1>
    <button onclick="location.href='/sighting'">Personal Rat Sighting</button>
    <button onclick="location.href='/report'">Inspection Posts</button>
    <button onclick="location.href='/qa'">Q&A Forum</button>
    <br>
    <img src="https://cdn.theatlantic.com/thumbor/ILSffj75k48V6kniK1TJMh1DXAw=/0x0:2400x3000/648x810/media/img/2023/03/01/Rats_opener4x5-1/original.jpg" alt="Rat in NYC" class="rat-image">
</body>
</html>
"""

DB_USER = "zz3306"
DB_PASSWORD = "hry2106"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://zz3306:hry2106@w4111.cisxo09blonu.us-east-1.rds.amazonaws.com/w4111"

engine = create_engine(DATABASEURI)

with engine.connect() as connection:  # "with" ensures the connection is properly closed
    print("Session created")

    # Execute the SQL commands
    connection.execute(text("""DROP TABLE IF EXISTS test;"""))
    connection.execute(text("""CREATE TABLE IF NOT EXISTS test (
        id serial,
        name text
    );"""))
    connection.execute(text("""INSERT INTO test(name) VALUES
        ('grace hopper'), ('alan turing'), ('ada lovelace');"""))

    connection.execute(text("""DROP TABLE IF EXISTS personal_rat_sighting CASCADE;"""))
    connection.execute(text("""CREATE TABLE personal_rat_sighting (
        sighting_id int PRIMARY KEY,
        zip_code int,
        comment text
    );"""))
    connection.execute(text("DELETE FROM personal_rat_sighting;"))
    connection.execute(text("""INSERT INTO personal_rat_sighting VALUES(1, 10458, 'I just saw a rat at Butler!');"""))
    connection.execute(text("""INSERT INTO personal_rat_sighting VALUES(2, 10022, 'Spotted a rat near Lerner Hall!');"""))
    connection.execute(text("""INSERT INTO personal_rat_sighting VALUES(3, 11206, 'Saw a huge rat by Low Library steps.');"""))
    connection.execute(text("""INSERT INTO personal_rat_sighting VALUES(4, 10032, 'There was a rat scurrying near the CU Subway station.');"""))
    connection.execute(text("""INSERT INTO personal_rat_sighting VALUES(5, 10457, 'A rat just ran past me at John Jay!');"""))   

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def home():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    # else:
        return render_template_string(html_template)

# @app.route('/login', methods=['POST'])
# def do_admin_login():
#     if request.form['password'] == 'password' and request.form['username'] == 'admin':
#         session['logged_in'] = True
#     else:
#         flash('wrong password!')
#     return home()

@app.route('/sighting')
def sighting():
  engine = create_engine(DATABASEURI)
  with engine.connect() as connection:  # "with" ensures the connection is properly closed after use
     result = connection.execute((text("SELECT * FROM personal_rat_sighting")))
     columns = result.keys()  # Get column names (headers)
     formatted_result = [dict(zip(columns, row)) for row in result.fetchall()]
  return formatted_result  # Or pass to context for rendering in template

@app.route('/report')
def report():
    return "Inspection Posts Page (Coming soon)"

@app.route('/qa')
def qa():
    return "Q&A Forum (Coming soon)"

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
