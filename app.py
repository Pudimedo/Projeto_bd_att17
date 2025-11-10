from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/db_atividade17'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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



@app.route('/autores')
def listar_autores():
    autores = Autor.query.all()
    return render_template('autores/listar_autores.html', autores=autores)


@app.route('/autores/novo', methods=['GET', 'POST'])
def novo_autor():
    if request.method == 'POST':
        nome = request.form['nome']
        nacionalidade = request.form.get('nacionalidade')
        data_nascimento = request.form.get('data_nascimento')
        biografia = request.form.get('biografia')

        novo_autor = Autor(
            Nome_autor=nome,
            Nacionalidade=nacionalidade,
            Data_nascimento=data_nascimento,
            Biografia=biografia
        )
        db.session.add(novo_autor)
        db.session.commit()
        return redirect(url_for('listar_autores'))

    return render_template('autores/novo_autor.html')


@app.route('/autores/editar/<int:id>', methods=['GET', 'POST'])
def editar_autor(id):
    autor = Autor.query.get_or_404(id)

    if request.method == 'POST':
        autor.Nome_autor = request.form['nome']
        autor.Nacionalidade = request.form.get('nacionalidade')
        autor.Data_nascimento = request.form.get('data_nascimento')
        autor.Biografia = request.form.get('biografia')

        db.session.commit()
        return redirect(url_for('listar_autores'))

    return render_template('autores/editar_autor.html', autor=autor)

@app.route('/autores/excluir/<int:id>', methods=['POST'])
def excluir_autor(id):
    autor = Autor.query.get_or_404(id)
    db.session.delete(autor)
    db.session.commit()
    return redirect(url_for('listar_autores'))



@app.route('/editoras')
def listar_editoras():
    editoras = Editora.query.all()
    return render_template('editoras/listar_editoras.html', editoras=editoras)


@app.route('/editoras/nova', methods=['GET', 'POST'])
def nova_editora():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form.get('endereco')

        nova_editora = Editora(
            Nome_editora=nome,
            Endereco_editora=endereco
        )
        db.session.add(nova_editora)
        db.session.commit()
        return redirect(url_for('listar_editoras'))

    return render_template('editoras/nova_editora.html')


@app.route('/editoras/editar/<int:id>', methods=['GET', 'POST'])
def editar_editora(id):
    editora = Editora.query.get_or_404(id)

    if request.method == 'POST':
        editora.Nome_editora = request.form['nome']
        editora.Endereco_editora = request.form.get('endereco')

        db.session.commit()
        return redirect(url_for('listar_editoras'))

    return render_template('editoras/editar_editora.html', editora=editora)


@app.route('/editoras/excluir/<int:id>', methods=['POST'])
def excluir_editora(id):
    editora = Editora.query.get_or_404(id)
    db.session.delete(editora)
    db.session.commit()
    return redirect(url_for('listar_editoras'))



@app.route('/emprestimos')
def listar_emprestimos():
    emprestimos = Emprestimo.query.all()
    return render_template('emprestimos/listar_emprestimos.html', emprestimos=emprestimos)


@app.route('/emprestimos/novo', methods=['GET', 'POST'])
def novo_emprestimo():
    usuarios = Usuario.query.all()
    livros = Livro.query.all()

    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        livro_id = request.form['livro_id']
        data_emprestimo = request.form.get('data_emprestimo')
        data_devolucao_prevista = request.form.get('data_devolucao_prevista')
        data_devolucao_real = request.form.get('data_devolucao_real')
        status = request.form.get('status')

        novo = Emprestimo(
            Usuario_id=usuario_id,
            Livro_id=livro_id,
            Data_emprestimo=data_emprestimo,
            Data_devolucao_prevista=data_devolucao_prevista,
            Data_devolucao_real=data_devolucao_real,
            Status_emprestimo=status
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('listar_emprestimos'))

    return render_template('emprestimos/novo_emprestimo.html', usuarios=usuarios, livros=livros)


@app.route('/emprestimos/editar/<int:id>', methods=['GET', 'POST'])
def editar_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    usuarios = Usuario.query.all()
    livros = Livro.query.all()

    if request.method == 'POST':
        emprestimo.Usuario_id = request.form['usuario_id']
        emprestimo.Livro_id = request.form['livro_id']
        emprestimo.Data_emprestimo = request.form.get('data_emprestimo')
        emprestimo.Data_devolucao_prevista = request.form.get('data_devolucao_prevista')
        emprestimo.Data_devolucao_real = request.form.get('data_devolucao_real')
        emprestimo.Status_emprestimo = request.form.get('status')

        db.session.commit()
        return redirect(url_for('listar_emprestimos'))

    return render_template('emprestimos/editar_emprestimo.html',
                           emprestimo=emprestimo, usuarios=usuarios, livros=livros)


@app.route('/emprestimos/excluir/<int:id>', methods=['POST'])
def excluir_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    db.session.delete(emprestimo)
    db.session.commit()
    return redirect(url_for('listar_emprestimos'))


@app.route('/generos')
def listar_generos():
    generos = Genero.query.all()
    return render_template('generos/listar_generos.html', generos=generos)


@app.route('/generos/novo', methods=['GET', 'POST'])
def novo_genero():
    if request.method == 'POST':
        nome = request.form['nome']

        novo = Genero(Nome_genero=nome)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('listar_generos'))

    return render_template('generos/novo_genero.html')


@app.route('/generos/editar/<int:id>', methods=['GET', 'POST'])
def editar_genero(id):
    genero = Genero.query.get_or_404(id)

    if request.method == 'POST':
        genero.Nome_genero = request.form['nome']
        db.session.commit()
        return redirect(url_for('listar_generos'))

    return render_template('generos/editar_genero.html', genero=genero)


@app.route('/generos/excluir/<int:id>', methods=['POST'])
def excluir_genero(id):
    genero = Genero.query.get_or_404(id)
    db.session.delete(genero)
    db.session.commit()
    return redirect(url_for('listar_generos'))


@app.route('/livros')
def listar_livros():
    livros = Livro.query.all()
    return render_template('livros/listar_livros.html', livros=livros)


@app.route('/livros/novo', methods=['GET', 'POST'])
def novo_livro():
    autores = Autor.query.all()
    generos = Genero.query.all()
    editoras = Editora.query.all()

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor_id = request.form.get('autor_id')
        isbn = request.form.get('isbn')
        ano_publicacao = request.form.get('ano_publicacao')
        genero_id = request.form.get('genero_id')
        editora_id = request.form.get('editora_id')
        quantidade = request.form.get('quantidade')
        resumo = request.form.get('resumo')

        novo = Livro(
            Titulo=titulo,
            Autor_id=autor_id,
            ISBN=isbn,
            Ano_publicacao=ano_publicacao,
            Genero_id=genero_id,
            Editora_id=editora_id,
            Quantidade_disponivel=quantidade,
            Resumo=resumo
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('listar_livros'))

    return render_template('livros/novo_livro.html', autores=autores, generos=generos, editoras=editoras)


@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):
    livro = Livro.query.get_or_404(id)
    autores = Autor.query.all()
    generos = Genero.query.all()
    editoras = Editora.query.all()

    if request.method == 'POST':
        livro.Titulo = request.form['titulo']
        livro.Autor_id = request.form.get('autor_id')
        livro.ISBN = request.form.get('isbn')
        livro.Ano_publicacao = request.form.get('ano_publicacao')
        livro.Genero_id = request.form.get('genero_id')
        livro.Editora_id = request.form.get('editora_id')
        livro.Quantidade_disponivel = request.form.get('quantidade')
        livro.Resumo = request.form.get('resumo')

        db.session.commit()
        return redirect(url_for('listar_livros'))

    return render_template('livros/editar_livro.html', livro=livro, autores=autores, generos=generos, editoras=editoras)


@app.route('/livros/excluir/<int:id>', methods=['POST'])
def excluir_livro(id):
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    return redirect(url_for('listar_livros'))



@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar_usuarios.html', usuarios=usuarios)


@app.route('/usuarios/novo', methods=['GET', 'POST'])
def novo_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        multa = request.form.get('multa')

        novo = Usuario(
            Nome_usuario=nome,
            Email=email,
            Numero_telefone=telefone,
            Multa_atual=multa or 0
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('listar_usuarios'))

    return render_template('usuarios/novo_usuario.html')


@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.Nome_usuario = request.form['nome']
        usuario.Email = request.form.get('email')
        usuario.Numero_telefone = request.form.get('telefone')
        usuario.Multa_atual = request.form.get('multa') or 0

        db.session.commit()
        return redirect(url_for('listar_usuarios'))

    return render_template('usuarios/editar_usuario.html', usuario=usuario)


@app.route('/usuarios/excluir/<int:id>', methods=['POST'])
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('listar_usuarios'))

if __name__ == '__main__':
    app.run(debug=True)