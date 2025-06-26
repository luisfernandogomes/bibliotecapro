from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Boolean, DateTime, Float, Date, func
from sqlalchemy.exc import SQLAlchemyError
# em baixo importamos session(gerenciar)  e sessiomaker(construir)
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship
from datetime import date
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash, check_password_hash


engine = create_engine('sqlite:///Biblioteca')
# db_session = scoped_session(sessionmaker(bind=engine)) padrao antigo
session_local = sessionmaker(bind=engine)
Base = declarative_base()
#Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha_hash = Column(String, nullable=False)
    cargo = Column(String, nullable=False)

    def set_senha_hash(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)
    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def serialize(self):
        dados = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cargo': self.cargo
        }
        return dados

class Livros(Base):
    __tablename__ = 'livros'
    id_livro = Column(Integer, primary_key=True, autoincrement=True)
    ISBN = Column(Integer, index=True, nullable=False)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    resumo = Column(String, nullable=False)
    status = Column(Boolean, nullable=True)

    def __repr__(self):
        return '<Livro {},{},{},{},{}>'.format(self.id_livro,self.ISBN, self.titulo, self.autor, self.resumo, self.status)

    def save(self, db_session):
        db_session.add(self)
        db_session.commit()
    def delete(self,db_session):
        db_session.delete(self)
        db_session.commit()
    def get_livro(self):
        dados_livro = {
            'id do livro': self.id_livro,
            'ISBN': self.ISBN,
            'titulo': self.titulo,
            'autor': self.autor,
            'resumo': self.resumo,
            'status': self.status
        }
        return dados_livro
class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    CPF = Column(String(11), nullable=False, unique=True)
    endereco = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return '<usuario {},{},{},{}>'.format(self.id, self.nome, self.CPF, self.endereco)

    def save(self,db_session):
        db_session.add(self)
        db_session.commit()
    def delete(self,db_session):
        db_session.delete(self)
        db_session.commit()
    def get_usuario(self):
        dados_usuario = {
            'id': self.id,
            'nome': self.nome,
            'CPF': self.CPF,
            'endereco': self.endereco
        }
        return dados_usuario
class Emprestimos(Base):
    __tablename__ = 'emprestimos'
    id_emprestimo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    data_emprestimo = Column(Date, nullable=True)
    data_de_devolucao = Column(Date, nullable=True)
    ISBN_livro = Column(Integer, ForeignKey('livros.ISBN'))
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    status = Column(String, nullable=True)
    usuario = relationship('Usuarios', backref='emprestimos')
    livro = relationship('Livros', backref='emprestimos')

    def __repr__(self):
        return '<emprestimo {},{},{},{},{},{}'.format(self.id_emprestimo,self.data_emprestimo, self.data_de_devolucao, self.ISBN_livro, self.id_usuario,self.status)
    def save(self,db_session):
        db_session.add(self)
        db_session.commit()
    def delete(self,db_session):
        db_session.delete(self)
        db_session.commit()

    def get_emprestimo(self):
        dados_emprestimo = {
            'id_emprestimo': self.id_emprestimo,
            'data_emprestimo': self.data_emprestimo,
            'data_de_devolucao': self.data_de_devolucao,
            'ISBN_livro': self.ISBN_livro,
            'id_usuario': self.id_usuario,
            'status': self.status
        }
        return dados_emprestimo




def init_db():
    Base.metadata.create_all(bind=engine)
if __name__ == '__main__':
    init_db()

