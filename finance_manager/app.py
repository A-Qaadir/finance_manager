from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'finance_manager.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    transactions = cur.fetchall()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO transactions (description, amount, date) VALUES (?, ?, ?)",
                    (description, amount, date))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add_transaction.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']
        cur.execute("UPDATE transactions SET description = ?, amount = ?, date = ? WHERE id = ?",
                    (description, amount, date, id))
        conn.commit()
        return redirect(url_for('index'))
    cur.execute("SELECT * FROM transactions WHERE id = ?", (id,))
    transaction = cur.fetchone()
    return render_template('edit_transaction.html', transaction=transaction)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_transaction(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id = ?", (id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
