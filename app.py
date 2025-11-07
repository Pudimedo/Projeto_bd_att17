from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/db_atividade17'

db = SQLAlchemy(app)


class Autor(db.Model):
    __tablename__ = 'Autores'

    ID_autor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_autor = db.Column(db.String(255), nullable=False)
    Nacionalidade = db.Column(db.String(255))
    Data_nascimento = db.Column(db.Date)
    Biografia = db.Column(db.Text)


class Genero(db.Model):
    __tablename__ = 'Generos'

    ID_genero = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_genero = db.Column(db.String(255), nullable=False)

class Editora(db.Model):
    __tablename__ = 'Editoras'

    ID_editora = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_editora = db.Column(db.String(255), nullable=False)
    Endereco_editora = db.Column(db.Text)

class Livro(db.Model):
    __tablename__ = 'Livros'

    ID_livro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Titulo = db.Column(db.String(255), nullable=False)
    Autor_id = db.Column(db.Integer, db.ForeignKey('Autores.ID_autor'))
    ISBN = db.Column(db.String(13), nullable=False)
    Ano_publicacao = db.Column(db.Integer)
    Genero_id = db.Column(db.Integer, db.ForeignKey('Generos.ID_genero'))
    Editora_id = db.Column(db.Integer, db.ForeignKey('Editoras.ID_editora'))
    Quantidade_disponivel = db.Column(db.Integer)
    Resumo = db.Column(db.Text)

    autor = db.relationship('Autor', backref='livros')
    genero = db.relationship('Genero', backref='livros')
    editora = db.relationship('Editora', backref='livros')

class Usuario(db.Model):
    __tablename__ = 'Usuarios'

    ID_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_usuario = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255))
    Numero_telefone = db.Column(db.String(15))
    Data_inscricao = db.Column(db.Date)
    Multa_atual = db.Column(db.Numeric(10, 2))


class Emprestimo(db.Model):
    __tablename__ = 'Emprestimos'

    ID_emprestimo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.ID_usuario'))
    Livro_id = db.Column(db.Integer, db.ForeignKey('Livros.ID_livro'))
    Data_emprestimo = db.Column(db.Date)
    Data_devolucao_prevista = db.Column(db.Date)
    Data_devolucao_real = db.Column(db.Date)
    Status_emprestimo = db.Column(db.Enum('pendente', 'devolvido', 'atrasado'))

    usuario = db.relationship('Usuario', backref='emprestimos')
    livro = db.relationship('Livro', backref='emprestimos')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)