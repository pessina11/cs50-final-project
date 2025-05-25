from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

def get_db():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    return redirect("/history")

# Resto das rotas serão adicionadas aqui...

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # Verifica campos vazios
        if not username or not password or not confirmation:
            flash('Por favor, preencha todos os campos.')
            return redirect('/register')

        # Verifica se senhas coincidem
        if password != confirmation:
            flash('As senhas não coincidem.')
            return redirect('/register')

        conn = get_db()
        cur = conn.cursor()

        # Verifica se usuário já existe
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            flash('Nome de usuário já está em uso.')
            conn.close()
            return redirect('/register')

        # Cria novo usuário com senha hasheada
        hash_pw = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
        conn.commit()
        conn.close()

        flash('Registro efetuado com sucesso! Faça login.')
        return redirect('/login')

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')

        if not username or not password:
            flash('Preencha todos os campos.')
            return redirect('/login')

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if not user or not check_password_hash(user['hash'], password):
            flash('Usuário e/ou senha inválidos.')
            return redirect('/login')

        session['user_id'] = user['id']
        session['username'] = user['username']
        flash(f'Bem-vindo(a), {user["username"]}!')
        return redirect('/')

    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu.")
    return redirect("/login")

@app.route("/history")
def history():
    if "user_id" not in session:
        flash("Faça login para acessar o histórico.")
        return redirect("/login")

    user_id = session["user_id"]
    db = get_db()
    transactions = db.execute(
        "SELECT type, category, amount, date FROM transactions WHERE user_id = ? ORDER BY date DESC",
        (user_id,)
    ).fetchall()
    db.close()

    return render_template("history.html", transactions=transactions)

from datetime import datetime

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        flash("Faça login para adicionar transações.")
        return redirect("/login")

    if request.method == "POST":
        t_type = request.form.get("type")
        category = request.form.get("category")
        amount = request.form.get("amount")
        date = request.form.get("date")

        if not t_type or not category or not amount or not date:
            flash("Preencha todos os campos.")
            return redirect("/add")

        try:
            amount = float(amount)
            # Validar o formato da data
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            flash("Valor ou data inválidos.")
            return redirect("/add")

        db = get_db()
        db.execute(
            "INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], t_type, category, amount, date)
        )
        db.commit()
        db.close()

        flash("Transação adicionada!")
        return redirect("/history")

    return render_template("add.html")

@app.route("/report")
def report():
    if "user_id" not in session:
        flash("Faça login para ver o relatório.")
        return redirect("/login")

    user_id = session["user_id"]
    db = get_db()
    # Consulta para agrupar por ano-mês, categoria, e tipo (income/expense)
    data = db.execute("""
        SELECT
            substr(date, 1, 7) AS month,
            category,
            type,
            SUM(amount) AS total
        FROM transactions
        WHERE user_id = ?
        GROUP BY month, category, type
        ORDER BY month DESC, category
    """, (user_id,)).fetchall()
    db.close()

    # Organizar dados para exibir no template
    report_data = {}
    for row in data:
        month = row["month"]
        if month not in report_data:
            report_data[month] = {"income": {}, "expense": {}}
        report_data[month][row["type"]][row["category"]] = row["total"]

    return render_template("report.html", report=report_data)


