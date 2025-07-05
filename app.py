from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, amount REAL, category TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    data = c.fetchall()
    total = sum([row[2] for row in data])
    conn.close()
    return render_template('index.html', data=data, total=total)

@app.route('/add', methods=['POST'])
def add():
    item = request.form['item']
    amount = float(request.form['amount'])
    category = request.form['category']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (item, amount, category) VALUES (?, ?, ?)", (item, amount, category))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
