import requests
from api import *
def get_usuarios():
    url = "http://10.135.235.23:5000/consultar_usuarios"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        # print(dados['usuarios_cadastrados'])
        # for u in dados['usuarios_cadastrados']:
        #     print(u['CPF'])
        # return jsonify({'sucesso': u['CPF']})
        print(dados['usuarios_cadastrados'])
        return dados['usuarios_cadastrados']

    else:
        dados = response.json()
        return dados
get_usuarios()
def post_user(nome, email,cargo,senha):
    url = "http://10.135.235.23:5000/cadastrar_users"
    user = {
        'nome': nome,
        'email': email,
        'cargo': cargo,
        'senha': senha
    }
    response = requests.post(url, json=user)
    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        dados = response.json()
        return dados
# post_user('Luis','luis@gmail.com','gerente','luis123')
def login(email, senha):
    url = "http://10.135.235.23:5000/login"
    logar = {
        'email': email,
        'senha': senha
    }
    response = requests.post(url, json=logar)
    if response.status_code == 200:
        dados = response.json()
        print(dados)
        return dados
    else:
        dados = response.json()
        print(dados)
        return dados
#    *****************************************************************************************
# login('luis@gmail.com','luis123')
def get_emprestimos():
    url = "http://10.135.235.23:5000/consultar_emprestimos"

    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        return dados['sucesso']
    else:
        return response.status_code
def get_livros():
    url = "http://10.135.235.23:5000/consultar_livros"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()

        return dados['livrosnocatalogodabiblioteca']

    else:

        return response.json()
def post_livro(titulo, autor, resumo, isbn):
    try:
        url = "http://10.135.235.23:5000/cadastrar_livro"
        livro = {"titulo": titulo,
                 "autor": autor,
                 "resumo": resumo,
                 "isbn": isbn}
        response = requests.post(url, json=livro)
        if response.status_code == 200:
            dados_post = response.json()
            return dados_post
        else:
            return response.json()
    except Exception as e:
        print(e)
def devolver_livro(isbn, id_usuario):
    url = "http://10.135.235.23:5000/devolver_livro"
    devolucao = {"isbn_livro": isbn,
                 "id_usuario": id_usuario
                 }
    response = requests.put(url, json=devolucao)
    if response.status_code == 200:
        dados_post = response.json()
        return dados_post
    else:
        print(response.status_code)
        dados = response.json()
        if 'error' in dados:
            print(dados['error'])

def cadastrar_emprestimos(id_usuario,isbn):
    url = "http://10.135.235.23:5000/cadastrar_emprestimo"
    emprestimo = {"id_usuario": id_usuario,
                  "isbn": isbn}
    response = requests.post(url, json=emprestimo)
    if response.status_code == 200:

        dados_post = response.json()
        return dados_post
    else:
        try:
            return response.json()
        except IndexError as e:
            print(e)
def get_emprestimos_por_usuario(id):
    url = f"http://10.135.235.23:5000/get_emprestimos_por_usuario/{id}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        return dados['sucesso']
    else:
        return response.json()
# get_emprestimos_por_usuario(1)


def editar_emprestimo(ISBN,id_usuario):
    url = f"http://10.135.235.23:5000/editar_emprestimo/{ISBN}"
    emprestimo = {"id_usuario":id_usuario}
    response = requests.put(url, json=emprestimo)
    if response.status_code == 200:

        dados_post = response.json()
        return dados_post
    else:
        return response.json()

def put_livro(id,titulo, autor, resumo, isbn):
    url = f"http://10.135.235.23:5000/atualizar_livro/{id}"
    livro = {"titulo": titulo,
             "autor": autor,
             "resumo": resumo,
             "isbn": isbn}
    response = requests.put(url, json=livro)
    if response.status_code == 200:

        dados_post = response.json()
        return dados_post
    else:
        return response.json()


def post_usuario(nome,cpf,endereco):
    url = "http://10.135.235.23:5000/cadastrar_usuario"
    usuario = {"nome": nome,
                "cpf": cpf,
                "endereco": endereco}
    response = requests.post(url, json=usuario)
    if response.status_code == 200:

        dados_post = response.json()
        return dados_post
    else:
        return response.json()

def post_emprestimo(id_usuario,isbn):
    url = "http://10.135.235.23:5000/cadastrar_emprestimo"
    emprestimo = {"id_usuario": id_usuario,
                  "isbn": isbn}
    response = requests.post(url, json=emprestimo)
    if response.status_code == 200:

        dados_post = response.json()
        return dados_post
    else:
        return response.json()

def put_usuario(id,nome,cpf,endereco):
    url = f"http://10.135.235.23:5000/atualizar_usuario/{id}"
    usuario = {"nome": nome,
                "CPF": cpf,
                "endereco": endereco}
    response = requests.put(url, json=usuario)
    if response.status_code == 200:

        dados_post = response.json()
        return dados_post
    else:
        return response.json()

def put_emprestimo(ISBN,id_usuario):
    url = f"http://10.135.235.23:5000/editar_emprestimo/{ISBN}"
    emprestimo = {"id_usuario": id_usuario}
    response = requests.put(url, json=emprestimo)
    if response.status_code == 200:

        dados_post = response.json()
        return dados_post
    else:
        print(response.json())

