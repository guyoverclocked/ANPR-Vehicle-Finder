from flask import Flask, render_template, request
import mysql.connector
app = Flask(__name__)

db = mysql.connector.connect(
    host="127.0.0.1",
    user="anpr",
    passwd="anpr1234",
    database ="lost_vehicle"
)
mycursor = db.cursor()
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        reg_no = request.form['reg_no']

        query = 'INSERT INTO user_info (name, email, reg_no) VALUES (%s, %s, %s)'
        values = (name, email, reg_no)
        mycursor.execute(query, values)
        db.commit()
        db.close()

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
