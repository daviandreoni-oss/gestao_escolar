from flask import Flask, jsonify, request

from database import criar_tabelas, conectar_banco

app = Flask(__name__)

criar_tabelas()

@app.route("/")
def inicio():
    return "Sistema de Gerenciamento Escolar"


@app.route("/cadastrar", methods=["GET", "POST"])
def formulario_cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        idade = request.form["idade"]
        data_nascimento = request.form.get("data_nascimento") or None

        conexao = conectar_banco()
        conexao.execute(
            """
            INSERT INTO alunos (nome, email, idade, data_nascimento)
            VALUES (?, ?, ?, ?)
            """, (nome, email, idade, data_nascimento)
        )
        conexao.commit()
        conexao.close()

        return """
            <h1>Aluno cadastrado com sucesso!</h1>
            <p><a href="/alunos">Ver alunos cadastrados</a></p>
            <p><a href="/cadastrar">Cadastrar outro aluno</a></p>
        """

    return """
        <!doctype html>
        <html lang="pt-br">
        <head>
            <meta charset="utf-8">
            <title>Cadastrar aluno</title>
        </head>
        <body>
            <h1>Cadastrar aluno</h1>
            <form method="post" action="/cadastrar">
                <label for="nome">Nome:</label>
                <input id="nome" name="nome" type="text" required>
                <br>
                <label for="email">E-mail:</label>
                <input id="email" name="email" type="email" required>
                <br>
                <label for="idade">Idade:</label>
                <input id="idade" name="idade" type="number" min="1" required>
                <br>
                <label for="data_nascimento">Data de nascimento (opcional):</label>
                <input id="data_nascimento" name="data_nascimento" type="date">
                <br>
                <button type="submit">Cadastrar</button>
            </form>
            <p><a href="/alunos">Ver alunos cadastrados</a></p>
        </body>
        </html>
    """


@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    dados = request.get_json()

    nome = dados["nome"]
    email = dados["email"]
    idade = dados["idade"]
    data_nascimento = dados.get("data_nascimento")

    conexao = conectar_banco()

    conexao.execute(
        """
        INSERT INTO alunos (nome, email, idade, data_nascimento)
        VALUES (?, ?, ?, ?)
        """, (nome, email, idade, data_nascimento)
    )

    conexao.commit()
    conexao.close()

    return "Aluno cadastrado com sucesso", 200



@app.route("/alunos", methods=["GET"])
def buscar_alunos():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT * FROM alunos
    """)

    colunas = [coluna[0] for coluna in cursor.description]
    alunos = [dict(zip(colunas, aluno)) for aluno in cursor.fetchall()]
    conexao.close()

    return jsonify(alunos)

if __name__ == "__main__":
    app.run(debug=True)
