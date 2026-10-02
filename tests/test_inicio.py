from app import app
from unittest.mock import patch


cliente = app.test_client()

def test_inicio_status_code():
    resposta = cliente.get("/")

    assert resposta.status_code == 200


def test_inicio_message():
    resposta = cliente.get("/")

    assert resposta.get_data(as_text=True) == "Sistema de Gerenciamento Escolar"


def test_buscar_alunos_retorna_lista_json():
    resposta = cliente.get("/alunos")

    assert resposta.status_code == 200
    assert isinstance(resposta.get_json(), list)


def test_formulario_cadastro():
    resposta = cliente.get("/cadastrar")

    assert resposta.status_code == 200
    assert b'<form method="post" action="/cadastrar">' in resposta.data
    assert b'name="nome"' in resposta.data
    assert b'name="email"' in resposta.data
    assert b'name="idade"' in resposta.data
    assert b'name="data_nascimento"' in resposta.data


def test_cadastrar_aluno_pelo_formulario():
    with patch("app.conectar_banco") as conectar_banco:
        resposta = cliente.post(
            "/cadastrar",
            data={
                "nome": "Ana",
                "email": "ana.form@example.com",
                "idade": "15",
                "data_nascimento": "2011-04-12",
            },
        )

    assert resposta.status_code == 200
    assert b"Aluno cadastrado com sucesso!" in resposta.data
    conexao = conectar_banco.return_value
    conexao.execute.assert_called_once()
    assert conexao.execute.call_args.args[1] == (
        "Ana", "ana.form@example.com", "15", "2011-04-12"
    )
    conexao.commit.assert_called_once()
    conexao.close.assert_called_once()


def test_cadastrar_aluno_por_json_com_data_nascimento():
    with patch("app.conectar_banco") as conectar_banco:
        resposta = cliente.post(
            "/alunos",
            json={
                "nome": "Bruno",
                "email": "bruno.json@example.com",
                "idade": 14,
                "data_nascimento": "2012-08-25",
            },
        )

    assert resposta.status_code == 200
    conexao = conectar_banco.return_value
    conexao.execute.assert_called_once()
    assert conexao.execute.call_args.args[1] == (
        "Bruno", "bruno.json@example.com", 14, "2012-08-25"
    )