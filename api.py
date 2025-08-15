from flask import Flask, jsonify, redirect, request
from flask_pydantic_spec import FlaskPydanticSpec
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import selectinload
from functools import wraps
from models import *
from datetime import date
from dateutil.relativedelta import relativedelta
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, desc
from flask_jwt_extended import get_jwt_identity, JWTManager, create_access_token, jwt_required
app = Flask(__name__)
spec = FlaskPydanticSpec('Flask',
                         title='Flask API',
                         version='1.0.0')
spec.register(app)
app.config['JWT_SECRET_KEY'] = 'senha'
jwt = JWTManager(app)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        db_session = session_local()
        current_user = get_jwt_identity()
        print(current_user)
        try:
            user = db_session.execute(select(User).where(User.email == current_user)).scalar()
            print(user)
            if user and user.papel == "gerente":
                return fn(*args, **kwargs)

            return jsonify({'error':'usuario não possui permissão de administrador'})
        finally:
            db_session.close()
    return wrapper

@app.route('/')
def index():
    return redirect('/consultar_livros')


@app.route('/cadastrar_users', methods=['POST'])

def cadastrar_user():
    db_session = session_local()

    dados = request.get_json()
    nome = dados['nome']
    email = dados['email']
    cargo = dados.get('cargo', 'usuario')
    senha = dados['senha']

    if not nome or not email or not senha:
        return jsonify({"msg": "Nome de usuário e senha são obrigatórios"}), 400
    try:
        # Verificar se o usuário já existe
        user_check = select(User).where(User.email == email)
        usuario_existente = db_session.execute(user_check).scalar()

        if usuario_existente:
            return jsonify({"msg": "Usuário já existe"}), 400

        novo_usuario = User(nome=nome, email=email, cargo=cargo)
        novo_usuario.set_senha_hash(senha)
        novo_usuario.save(db_session)

        user_id = novo_usuario.id
        return jsonify({"sucesso": user_id}), 201
    except Exception as e:
        return jsonify({"error": {str(e)}}), 500
    finally:
        db_session.close()

@app.route('/login', methods=['POST'])
def login():
    db_session = session_local()
    dados = request.get_json()
    email = dados['email']
    senha = dados['senha']
    try:
        user = db_session.execute(select(User).where(User.email == email)).scalar()
        if user and user.check_password(senha):
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token)
        return jsonify({'error': 'Senha incorreto'})
    finally:
        db_session.close()

@app.route('/consultar_usuarios', methods=['GET'])
def consultar_usuarios():
    """
    Retorna uma lista de todos os usuários cadastrados.

    Endpoint:
    /consultar_usuarios

    Respostas (JSON):
    ```json
    {
        "usuarios": [
            {
                "id_usuario": 1,
                "nome": "João Silva",
                "CPF": "12312312312",
                "endereco": "Rua"
            }
        ]
    }
    ```
    Erros possíveis (JSON):
    ```json
    {
        "erro": "Mensagem de erro"
    }
    ```
    """
    db_session = session_local()
    try:
        usuarios = db_session.execute(select(Usuarios)).scalars().all()

        lista_usuarios = []
        for usuario in usuarios:
            lista_usuarios.append(usuario.get_usuario())
        return jsonify({'usuarios_cadastrados': lista_usuarios})
    except Exception as e:
        return jsonify({'error': 'Erro ao consultar usuários', 'detalhes': str(e)}), 500


@app.route('/consultar_livros')
def consultar_livros():
    """
        Retorna uma lista de todos os livros cadastrados.

        Endpoint:
        /livros

        Respostas (JSON):
        ```json
        {
            "livros": [
                {
                    "id_livro": 1,
                    "titulo": "livro1",
                    "autor": " lucianp",
                    "ISBN": "9788533302273",
                    "resumo": "resumo1"
                }
            ]
        }
        ```
        Erros possíveis (JSON):
        ```json
        {
            "erro": "Mensagem de erro"
        }
        ```
        """
    db_session = session_local()
    try:
        lista_livros = select(Livros)
        lista_livros = db_session.execute(lista_livros).scalars().all()
        result = []
        for livro in lista_livros:
            result.append(livro.get_livro())

        return jsonify({'livrosnocatalogodabiblioteca': result})
    except IntegrityError as e:
        return jsonify({'error': str(e)})
@app.route('/consultar_emprestimos')
def consultar_emprestimos():
    """
     Retorna uma lista de todos os empréstimos registrados

     Endpoint:
     /consultar_emprestimos

     Respostas (JSON):
     ```json
     {
         "emprestimos": [
             {
                 "id_emprestimo": 1,
                 "id_usuario": 1,
                 "id_livro": 1,
                 "data": 03/02/2024
             }
         ]
     }
     ```
     Erros possíveis (JSON):
     ```json
     {
         "erro": "Mensagem de erro"
     }
     ```
     """
    db_session = session_local()
    try:
        emprestimos = db_session.execute(
            select(Emprestimos)
            .options(
                selectinload(Emprestimos.usuario),
                selectinload(Emprestimos.livro)
            )
        ).scalars().all()

        lista = []
        for emp in emprestimos:
            lista.append({
                'id_emprestimo': emp.id_emprestimo,
                'data_emprestimo': emp.data_emprestimo,
                'data_de_devolucao': emp.data_de_devolucao,
                'status': emp.status,
                'usuario': {
                    'id': emp.usuario.id,
                    'nome': emp.usuario.nome,
                    'CPF': emp.usuario.CPF,
                    'endereco': emp.usuario.endereco
                },
                'livro': {
                    'ISBN': emp.livro.ISBN,
                    'titulo': emp.livro.titulo,
                    'status': emp.livro.status
                }
            })

        return jsonify({'sucesso': lista})
    except IntegrityError as e:
        return jsonify({'error': str(e)})

@app.route('/get_emprestimos_por_usuario/<id>', methods=['GET'])
def get_emprestimos(id):
    """
        Retorna uma lista do todos os empréstimos realizados por usuario

        Endpoint:
        /get_emprestimos_por_usuario/<id>

        Respostas (JSON):
        ```json
        {
            "emprestimos": [
                {
                'id_emprestimo': emp.id_emprestimo,
                'data_emprestimo': emp.data_emprestimo,
                'data_de_devolucao': emp.data_de_devolucao,

                    'usuario': {
                        'id': emp.usuario.id,
                        'nome': emp.usuario.nome,
                        'CPF': emp.usuario.CPF,
                        'endereco': emp.usuario.endereco
                    },
                    'livro': {
                        'ISBN': emp.livro.ISBN,
                        'titulo': emp.livro.titulo,
                        'status': emp.livro.status
                }
            ]
        }
        ```
        Erros possíveis (JSON):
        ```json
        {
            "erro": "Mensagem de erro"
        }
        ```
        """
    db_session = session_local()
    try:

        emprestimos = db_session.execute(
            select(Emprestimos).where(Emprestimos.id_usuario == id)
            .options(
                selectinload(Emprestimos.usuario),
                selectinload(Emprestimos.livro)
            )
        ).scalars().all()

        lista = []
        for emp in emprestimos:
            lista.append({
                'id_emprestimo': emp.id_emprestimo,
                'data_emprestimo': emp.data_emprestimo,
                'data_de_devolucao': emp.data_de_devolucao,
                'usuario': {
                    'id': emp.usuario.id,
                    'nome': emp.usuario.nome,
                    'CPF': emp.usuario.CPF,
                    'endereco': emp.usuario.endereco
                },
                'livro': {
                    'ISBN': emp.livro.ISBN,
                    'titulo': emp.livro.titulo,
                    'status': emp.livro.status
                }
            })

        return jsonify({'sucesso': lista})
    except IntegrityError as e:
        return jsonify({'error': str(e)})
@app.route('/cadastrar_livro', methods=['POST'])


def cadastrar_livro():
    """
        Cadastra um novo livro no sistema

        Endpoint:
        /cadastrar_livro

        Corpo da Requisição (JSON):
        ```json
        {
            "titulo": "Nome do Livro",
            "autor": "Nome do Autor",
            "isbn": "11111111111",
            "resumo": "Resumo do livro"
        }
        ```

        Respostas (JSON):
        ```json
        {
            "id_livro": 1,
            "titulo": "Nome do Livro",
            "autor": "Nome do Autor",
            "ISBN": "11111111111",
            "resumo": "Resumo do livro"
        }

        Erros possíveis (JSON):
        ```json
        {
            "erro": "Campos não podem ser vazios"
        }
        """
    db_session = session_local()
    if request.method == 'POST':
        dados = request.get_json()
        titulo = dados['titulo']
        autor = dados['autor']
        resumo = dados['resumo']
        isbn = dados['isbn']
        isbn_existente = select(Livros)
        isbn_existente = db_session.execute(isbn_existente.filter_by(ISBN=isbn)).first()
        if isbn_existente:
            return jsonify({'error': 'isbn_existente'}), 400
        if not titulo:
            return jsonify({"error": 'campo titulo vazio'}), 400
        if not autor:
            return jsonify({"error": 'campo autor vazio'}), 400
        if not resumo:
            return jsonify({"error": 'campo resumo vazio'}), 400
        if not isbn:
            return jsonify({"error": 'campo ISBN vazio'}), 400
        else:
            try:
                isbn = int(isbn)
                livro_salvado = Livros(titulo=titulo,
                                       autor=autor,
                                       resumo=resumo,
                                       ISBN=isbn,
                                       status=True)
                livro_salvado.save(db_session)
                if livro_salvado.status:
                    status_emprestimo = 'Está disponivel para emprestimo'
                else:
                    status_emprestimo = 'Livro não está disponivel para emprestimo'
                return jsonify({
                    'titulo': livro_salvado.titulo,
                    'autor': livro_salvado.autor,
                    'resumo': livro_salvado.resumo,
                    'status': status_emprestimo,
                    'ISBN': livro_salvado.ISBN
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500


@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    """
        Cadastra um novo usuário no sistema.

        Endpoint:
        /cadastrar_usuario

        Corpo da Requisição (JSON):
        ```json
        {
            "nome": "Mariaaaaaaaaaa",
            "cpf": "40570214858",
            "endereco": "Avenida 333"
        }
        ```
        Erros possíveis (JSON):
        ```json
        {
            "status": false,
            "erro": "Campos não podem ser vazios"
        }
        ```
        Status: 400 Bad Request
        """
    db_session = session_local()
    if request.method == 'POST':
        dados = request.get_json()
        nome = dados['nome']
        cpf = dados['cpf']
        endereco = dados['endereco']

        cpf_ja_cadastrado = select(Usuarios)
        cpf_ja_cadastrado = db_session.execute(cpf_ja_cadastrado.filter_by(CPF=cpf)).first()
        if cpf_ja_cadastrado:
            return jsonify({"error": 'CPF ja cadastrado'})

        endereco_ja_cadastrado = select(Usuarios)
        endereco_ja_cadastrado = db_session.execute(endereco_ja_cadastrado.filter_by(endereco=endereco)).first()
        if endereco_ja_cadastrado:
            return jsonify({"error": 'endereco ja cadastrado'})
        if not dados['nome']:
            return jsonify({"error": 'campo nome vazio'}, 400)
        if not dados['cpf']:
            return jsonify({"error": 'campo cpf vazio'}, 400)
        if not dados['endereco']:
            return jsonify({"error": 'campo endereco vazio'}, 400)
        else:
            try:
                usuario_salvado = Usuarios(nome=nome,
                                           CPF=cpf,
                                           endereco=endereco)
                usuario_salvado.save(db_session)
                return jsonify({
                    'nome': usuario_salvado.nome,
                    'cpf': usuario_salvado.CPF,
                    'endereco': usuario_salvado.endereco})
            except IntegrityError as e:
                return jsonify({'error': str(e)})


@app.route('/cadastrar_emprestimo', methods=['POST'])
def cadastrar_emprestimo():
    """
        Realiza um empréstimo de livro

        Endpoint:
        /cadastrar_emprestimo

        Corpo da Requisição (JSON):
        ```json
        {
            "id_usuario": 1,
            "id_livro": 2,
            "data_emprestimo": "YYYY-MM-DD",
            "data_devolucao": "YYYY-MM-DD"
        }
        ```

        Respostas (JSON):
        ```json
        {
            "id_emprestimo": 1,
            "id_usuario": 1,
            "id_livro": 2,
            "data_emprestimo": "YYYY-MM-DD",
            "data_devolucao": "YYYY-MM-DD"
        }
        ```
        Status: 201 Created

        Erros possíveis (JSON):
        ```json
        {
            "erro": "Campos obrigatórios estão ausentes"
        }
        ```
        Status: 400 Bad Request
        ```json
        {
            "erro": "Usuário não encontrado"
        }
        ```
        Status: 404 Not Found
        ```json
        {
            "erro": "Livro não encontrado"
        }
        ```
        Status: 404 Not Found
        ```json
        {
            "erro": "Mensagem de erro"
        }
        ```
        Status: 400 Bad Request
    """
    db_session = session_local()
    try:
        data_emprestimo = date.today()

        data_de_devolucao = data_emprestimo + relativedelta(weeks=5)
        data_emprestimo.strftime('%d/%m/%Y')
        dados = request.get_json()
        isbn = dados['isbn']
        id_usuario = dados['id_usuario']

        id_usuario = int(id_usuario)
        if not isbn or not id_usuario:
            return jsonify({'error': 'Campos ISBN e id_usuario são obrigatórios'}), 400
        emprestimos_usuario = db_session.execute(
            select(Emprestimos).filter_by(id_usuario=id_usuario)
        ).scalars().all()

        for emprestimo in emprestimos_usuario:
            livro = db_session.execute(
                select(Livros).filter_by(ISBN=emprestimo.ISBN_livro)
            ).scalar_one_or_none()

            if livro and livro.status == False:
                return jsonify({
                    'error': 'Usuário já possui empréstimo ativo. Devolva o livro antes de realizar um novo empréstimo.'
                })
        isbn = int(isbn)

        livro = db_session.execute(select(Livros).filter_by(ISBN=isbn)).scalar()
        if not livro:
            return jsonify({'error': 'Livro não encontrado'}), 404

        if not livro.status:
            return jsonify({'error': 'Livro não está disponível para empréstimo'}), 400

        usuario = db_session.get(Usuarios, id_usuario)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        emprestimo = Emprestimos(
            data_emprestimo=data_emprestimo,
            data_de_devolucao=data_de_devolucao,
            ISBN_livro=isbn,
            id_usuario=id_usuario,
            status='pendente'
        )
        emprestimo.save(db_session)

        livro.status = False
        livro.save()

        return jsonify({
            'data_emprestimo': emprestimo.data_emprestimo,
            'data_de_devolucao': emprestimo.data_de_devolucao,
            'ISBN_livro': emprestimo.ISBN_livro,
            'id_usuario': emprestimo.id_usuario
        })
    except IntegrityError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/atualizar_usuario/<id>', methods=['PUT'])
def editar_usuario(id):
    """
           Atualiza os dados de um usuário existente

           Endpoint:
           atualizar_usuario/<id>


           Corpo da Requisição (JSON):
           ```json
           {
               "nome": "Novo Nome do Usuário",
               "cpf": "111.222.333-44",
               "endereco": "Nova Rua, 789"
           }
           ```
           (Envie apenas os campos que deseja atualizar)

           Respostas (JSON):
           ```json
           {
               "id_usuario": 1,
               "nome": "Novo Nome do Usuário",
               "CPF": "111.222.333-44",
               "endereco": "Nova Rua"
           }
           ```
           Status: 200 OK

           Erros possíveis (JSON):
           ```json
           {
               "erro": "Usuário não encontrado"
           }
           ```
           Status: 404 Not Found
           ```json
           {
               "erro": "Mensagem de erro"
           }
           ```
           Status: 400 Bad Request
       """
    db_session = session_local()
    if request.method == 'PUT':
        try:
            id = int(id)
            # usuario_editado = db_session.execute(select(Usuarios).where(Usuarios.id_usuario == id)).scalar()
            usuario = select(Usuarios)
            # fazer a busca do banco, filtrando o id:
            usuario_editado = db_session.execute(usuario.filter_by(id=id)).scalar()
            if not usuario_editado:
                return jsonify({'error': 'usuario não encontrado'})
            dados = request.get_json()
            usuario_editado.nome = dados['nome']
            usuario_editado.CPF = dados['CPF']
            usuario_editado.endereco = dados['endereco']
            cpf_existente = db_session.execute(
                select(Usuarios).filter(Usuarios.CPF == usuario_editado.CPF, Usuarios.id != id)
            ).scalar()
            if not dados['nome'] or not dados['CPF'] or not dados['endereco']:
                return jsonify({'error':'campos estão vazios'})
            if cpf_existente:
                return jsonify({'error': 'CPF ja cadastrado'})
            usuario_editado.save()
            return jsonify({'dados': usuario_editado.get_usuario()})


        except IntegrityError as e:
            return jsonify({'error': str(e)}), 500

@app.route('/atualizar_livro/<id>', methods=['PUT'])
def atualizar_livro(id):
    """
               Atualiza os dados de um usuário existente

               Endpoint:
               atualizar_usuario/<id>


               Corpo da Requisição (JSON):
               ```json
               {
                     "titulo": "Nome do Livro",
                    "autor": "Nome do Autor",
                    "isbn": "11111111111",
                    "resumo": "Resumo do livro"
               }
               ```
               (Envie apenas os campos que deseja atualizar)

               Respostas (JSON):
               ```json
               {
                    "titulo": "Nome do Livro",
                    "autor": "Nome do Autor",
                    "isbn": "11111111111",
                    "resumo": "Resumo do livro"
                }
               ```
               Status: 200 OK

               Erros possíveis (JSON):
               ```json
               {
                   "erro": "Usuário não encontrado"
               }
               ```
               Status: 404 Not Found
               ```json
               {
                   "erro": "Mensagem de erro"
               }
               ```
               Status: 400 Bad Request
           """
    db_session = session_local()
    try:
        livro = select(Livros)
        livro = db_session.execute(livro.filter_by(id_livro=id)).scalar()
        if not livro:
            return jsonify({'error': 'Livro não encontrado'}), 404
        dados = request.get_json()

        titulo = dados['titulo']
        livro_existente = select(Livros)
        titulo_existente = db_session.execute(livro_existente.filter_by(titulo=titulo)).scalar()
        if titulo_existente:
            return jsonify({'titulo de livro já cadastrado': titulo})
        autor = dados['autor']
        resumo = dados['resumo']
        isbn = dados['isbn']
        if titulo:
            livro.titulo = titulo
        if autor:
            livro.autor = autor
        if resumo:
            livro.resumo = resumo
        if isbn:
            livro.ISBN = isbn
        livro.save()
        return jsonify({'sucesso': livro.get_livro()})
    except IntegrityError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/emprestimos_por_usuario/<id_usuario>', methods=['GET'])
def emprestimos_por_usuario(id_usuario):
    """
            Lista dos empréstimos realizados por usuario

            Endpoint:
            /emprestimos_por_usuario/<id_usuario>

            Respostas (JSON):
            ```json
            {
                "emprestimos": [
                    {
                    'id_emprestimo': emp.id_emprestimo,
                    'data_emprestimo': emp.data_emprestimo,
                    'data_de_devolucao': emp.data_de_devolucao,

                        'usuario': {
                            'id': emp.usuario.id,
                            'nome': emp.usuario.nome,
                            'CPF': emp.usuario.CPF,
                            'endereco': emp.usuario.endereco
                        },
                        'livro': {
                            'ISBN': emp.livro.ISBN,
                            'titulo': emp.livro.titulo,
                            'status': emp.livro.status
                    }
                ]
            }
            ```
            Erros possíveis (JSON):
            ```json
            {
                "erro": "Mensagem de erro"
            }
            ```
            """
    db_session = session_local()
    try:
        emprestimos = db_session.execute(select(Emprestimos).filter_by(id_usuario=id_usuario)).scalars()
        if not emprestimos:
            return jsonify({'mensagem': 'Nenhum empréstimo encontrado para este usuário'})

        lista_emprestimos = []
        for emprestimo in emprestimos:
            lista_emprestimos.append(emprestimo.get_emprestimo())
        return jsonify({'emprestimos': lista_emprestimos})
    except IntegrityError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/editar_emprestimo/<ISBN>', methods=['PUT'])
def editar_emprestimo(ISBN):
    db_session = session_local()
    if request.method == 'PUT':
        try:
            ISBN = int(ISBN)
            livro_encontrado = db_session.execute(select(Emprestimos).filter_by(ISBN_livro=ISBN)).scalar_one_or_none()
            print(livro_encontrado)
            if not livro_encontrado:
                return jsonify({'error': 'livro não encontrado'})
            dados = request.get_json()
            id_usuario = dados['id_usuario']
            id_usuario = int(id_usuario)
            usuario_encontrado = db_session.execute(select(Usuarios).filter_by(id=id_usuario)).first()
            if not usuario_encontrado:
                return jsonify({"error": "usuario nao encontrado"})
            livro_encontrado.id_usuario = id_usuario
            livro_encontrado.save()
            return jsonify({"sucesso": livro_encontrado.get_emprestimo()})
        except IntegrityError as e:
            return jsonify({'error': str(e)}), 500


@app.route('/devolver_livro', methods=['PUT'])
def devolver():
    db_session = session_local()
    try:
        dados = request.get_json()
        id_usuario = dados['id_usuario']
        isbn_livro = dados['isbn_livro']
        user_existente = db_session.execute(select(Usuarios).filter_by(id=id_usuario)).scalar()
        livro_existente = db_session.execute(select(Livros).filter_by(ISBN=isbn_livro)).scalar()
        status_emprestimo = db_session.execute(select(Emprestimos).filter_by(ISBN_livro=isbn_livro)).scalar()
        status_emprestimo.status = 'finalizado'

        if not user_existente:
            return jsonify({'error': 'usuario não encontrado'})
        if not livro_existente:
            return jsonify({'error': 'livro não existente'})
        if livro_existente.status:
            return jsonify({'error': 'livro já está devolvido'}),
        status_emprestimo.save()
        livro_existente.status = True
        livro_existente.save()
        return jsonify({'dados': livro_existente.get_livro()})
    except IntegrityError as e:
        return jsonify({'error': str(e)}), 500


# Banco
# Emprestimos, id usuario
# Usuario: cpf, endereço
# livro: /
# //////////////////////////
# proteção: editar emprestimos,
# emprestimos por usuario
# atulizar livro,
# atualizar usuario,
# cadastro de emprestimos,
# cadastro usuario,
# cadastro de livro
# consultar usuarios
# ////////////////
# sem proteção
# consultar livros

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
