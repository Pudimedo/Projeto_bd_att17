from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = "123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/db_atividade17'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)





@app.route("/")
def index():
    return render_template("index.html")





@app.route("/autores")
def listar_autores():
    try:
        autores = db.session.execute(
            text("SELECT * FROM Autores")
        ).fetchall()
        return render_template("autores/listar_autores.html", autores=autores)

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))


@app.route("/autor/novo", methods=["GET", "POST"])
def novo_autor():
    if request.method == "POST":
        try:
            db.session.execute(text("""
                INSERT INTO Autores 
                (Nome_autor, Nacionalidade, Data_nascimento, Biografia)
                VALUES (:nome, :nac, :data, :bio)
            """), {
                "nome": request.form.get("nome"),
                "nac": request.form.get("nacionalidade"),
                "data": request.form.get("data_nascimento"),
                "bio": request.form.get("biografia")
            })

            db.session.commit()
            flash("Autor cadastrado com sucesso!", "success")
            return redirect(url_for("listar_autores"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    return render_template("autores/novo_autor.html")


@app.route("/autor/editar/<int:id>", methods=["GET", "POST"])
def editar_autor(id):
    if request.method == "POST":
        try:
            db.session.execute(text("""
                UPDATE Autores SET
                    Nome_autor = :nome,
                    Nacionalidade = :nac,
                    Data_nascimento = :data,
                    Biografia = :bio
                WHERE ID_autor = :id
            """), {
                "nome": request.form.get("nome"),
                "nac": request.form.get("nacionalidade"),
                "data": request.form.get("data_nascimento"),
                "bio": request.form.get("biografia"),
                "id": id
            })

            db.session.commit()
            flash("Autor editado com sucesso!", "success")
            return redirect(url_for("listar_autores"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    autor = db.session.execute(
        text("SELECT * FROM Autores WHERE ID_autor = :id"),
        {"id": id}
    ).fetchone()

    return render_template("autores/editar_autor.html", autor=autor)


@app.route("/autor/excluir/<int:id>", methods=["GET", "POST"])
def excluir_autor(id):
    try:
        db.session.execute(
            text("DELETE FROM Autores WHERE ID_autor = :id"),
            {"id": id}
        )
        db.session.commit()
        flash("Autor excluído com sucesso!", "success")

    except Exception as e:
        db.session.rollback()
        flash(str(e), "danger")

    return redirect(url_for("listar_autores"))





@app.route("/editoras")
def listar_editoras():
    try:
        editoras = db.session.execute(
            text("SELECT * FROM Editoras")
        ).fetchall()
        return render_template("editoras/listar_editoras.html", editoras=editoras)

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))


@app.route("/editora/nova", methods=["GET", "POST"])
def nova_editora():
    if request.method == "POST":
        try:
            db.session.execute(
                text("INSERT INTO Editoras (Nome_editora) VALUES (:nome)"),
                {"nome": request.form.get("nome")}
            )
            db.session.commit()
            flash("Editora cadastrada com sucesso!", "success")
            return redirect(url_for("listar_editoras"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    return render_template("editoras/nova_editora.html")


@app.route("/editora/editar/<int:id>", methods=["GET", "POST"])
def editar_editora(id):
    if request.method == "POST":
        try:
            db.session.execute(
                text("UPDATE Editoras SET Nome_editora = :nome WHERE ID_editora = :id"),
                {"nome": request.form.get("nome"), "id": id}
            )
            db.session.commit()
            flash("Editora editada com sucesso!", "success")
            return redirect(url_for("listar_editoras"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    editora = db.session.execute(
        text("SELECT * FROM Editoras WHERE ID_editora = :id"),
        {"id": id}
    ).fetchone()

    return render_template("editoras/editar_editora.html", editora=editora)


@app.route("/editora/excluir/<int:id>", methods=["GET", "POST"])
def excluir_editora(id):
    try:
        db.session.execute(
            text("DELETE FROM Editoras WHERE ID_editora = :id"),
            {"id": id}
        )
        db.session.commit()
        flash("Editora excluída com sucesso!", "success")

    except Exception as e:
        db.session.rollback()
        flash(str(e), "danger")

    return redirect(url_for("listar_editoras"))





@app.route("/generos")
def listar_generos():
    try:
        generos = db.session.execute(
            text("SELECT * FROM Generos")
        ).fetchall()
        return render_template("generos/listar_generos.html", generos=generos)

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))


@app.route("/genero/novo", methods=["GET", "POST"])
def novo_genero():
    if request.method == "POST":
        try:
            db.session.execute(
                text("INSERT INTO Generos (Nome_genero) VALUES (:nome)"),
                {"nome": request.form.get("nome")}
            )
            db.session.commit()
            flash("Gênero cadastrado com sucesso!", "success")
            return redirect(url_for("listar_generos"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    return render_template("generos/novo_genero.html")


@app.route("/genero/editar/<int:id>", methods=["GET", "POST"])
def editar_genero(id):
    if request.method == "POST":
        try:
            db.session.execute(
                text("UPDATE Generos SET Nome_genero = :nome WHERE ID_genero = :id"),
                {"nome": request.form.get("nome"), "id": id}
            )
            db.session.commit()
            flash("Gênero editado com sucesso!", "success")
            return redirect(url_for("listar_generos"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    genero = db.session.execute(
        text("SELECT * FROM Generos WHERE ID_genero = :id"),
        {"id": id}
    ).fetchone()

    return render_template("generos/editar_genero.html", genero=genero)


@app.route("/genero/excluir/<int:id>", methods=["GET", "POST"])
def excluir_genero(id):
    try:
        db.session.execute(
            text("DELETE FROM Generos WHERE ID_genero = :id"),
            {"id": id}
        )
        db.session.commit()
        flash("Gênero excluído com sucesso!", "success")

    except Exception as e:
        db.session.rollback()
        flash(str(e), "danger")

    return redirect(url_for("listar_generos"))





@app.route("/usuarios")
def listar_usuarios():
    try:
        usuarios = db.session.execute(
            text("SELECT * FROM Usuarios")
        ).fetchall()
        return render_template("usuarios/listar_usuarios.html", usuarios=usuarios)

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))


@app.route("/usuario/novo", methods=["GET", "POST"])
def novo_usuario():
    if request.method == "POST":
        try:
            db.session.execute(text("""
                INSERT INTO Usuarios 
                (Nome_usuario, Email, Numero_telefone, Data_inscricao, Multa_atual)
                VALUES (:nome, :email, :telefone, CURDATE(), 0)
            """), {
                "nome": request.form.get("nome"),
                "email": request.form.get("email"),
                "telefone": request.form.get("telefone")
            })

            db.session.commit()
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("listar_usuarios"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    return render_template("usuarios/novo_usuario.html")


@app.route("/usuario/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    if request.method == "POST":
        try:
            db.session.execute(text("""
                UPDATE Usuarios SET
                    Nome_usuario = :nome,
                    Email = :email,
                    Numero_telefone = :telefone
                WHERE ID_usuario = :id
            """), {
                "nome": request.form.get("nome"),
                "email": request.form.get("email"),
                "telefone": request.form.get("telefone"),
                "id": id
            })

            db.session.commit()
            flash("Usuário editado com sucesso!", "success")
            return redirect(url_for("listar_usuarios"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    usuario = db.session.execute(
        text("SELECT * FROM Usuarios WHERE ID_usuario = :id"),
        {"id": id}
    ).fetchone()

    return render_template("usuarios/editar_usuario.html", usuario=usuario)


@app.route("/usuario/excluir/<int:id>", methods=["GET", "POST"])
def excluir_usuario(id):
    try:
        db.session.execute(
            text("DELETE FROM Usuarios WHERE ID_usuario = :id"),
            {"id": id}
        )
        db.session.commit()
        flash("Usuário excluído com sucesso!", "success")

    except Exception as e:
        db.session.rollback()
        flash(str(e), "danger")

    return redirect(url_for("listar_usuarios"))






@app.route("/emprestimos")
def listar_emprestimos():
    try:
        emprestimos = db.session.execute(text("""
            SELECT E.*, 
                   U.Nome_usuario AS usuario_nome, 
                   L.Titulo AS livro_titulo
            FROM Emprestimos E
            LEFT JOIN Usuarios U ON E.Usuario_id = U.ID_usuario
            LEFT JOIN Livros L ON E.Livro_id = L.ID_livro
        """)).fetchall()
        return render_template("emprestimos/listar_emprestimos.html", emprestimos=emprestimos)

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))


@app.route("/emprestimo/novo", methods=["GET", "POST"])
def novo_emprestimo():
    if request.method == "POST":
        try:
            db.session.execute(text("""
                INSERT INTO Emprestimos 
                (Usuario_id, Livro_id, Data_emprestimo, Data_devolucao_prevista, Status_emprestimo)
                VALUES (:usuario, :livro, CURDATE(), :prevista, 'pendente')
            """), {
                "usuario": request.form.get("usuario_id"),
                "livro": request.form.get("livro_id"),
                "prevista": request.form.get("data_prevista")
            })

            db.session.commit()
            flash("Empréstimo cadastrado com sucesso!", "success")
            return redirect(url_for("listar_emprestimos"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    usuarios = db.session.execute(text("SELECT * FROM Usuarios")).fetchall()
    livros = db.session.execute(text("SELECT * FROM Livros")).fetchall()
    return render_template("emprestimos/novo_emprestimo.html", usuarios=usuarios, livros=livros)


@app.route("/emprestimo/editar/<int:id>", methods=["GET", "POST"])
def editar_emprestimo(id):
    if request.method == "POST":
        try:
            db.session.execute(text("""
                UPDATE Emprestimos SET
                    Usuario_id = :usuario,
                    Livro_id = :livro,
                    Data_emprestimo = :data_emprestimo,
                    Data_devolucao_prevista = :data_prevista,
                    Data_devolucao_real = :data_real,
                    Status_emprestimo = :status
                WHERE ID_emprestimo = :id
            """), {
                "usuario": request.form.get("usuario_id"),
                "livro": request.form.get("livro_id"),
                "data_emprestimo": request.form.get("data_emprestimo"),
                "data_prevista": request.form.get("data_prevista"),
                "data_real": request.form.get("data_real"),
                "status": request.form.get("status"),
                "id": id
            })

            db.session.commit()
            flash("Empréstimo editado com sucesso!", "success")
            return redirect(url_for("listar_emprestimos"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    emprestimo = db.session.execute(
        text("SELECT * FROM Emprestimos WHERE ID_emprestimo = :id"),
        {"id": id}
    ).fetchone()
    usuarios = db.session.execute(text("SELECT * FROM Usuarios")).fetchall()
    livros = db.session.execute(text("SELECT * FROM Livros")).fetchall()
    return render_template("emprestimos/editar_emprestimo.html",
                           emprestimo=emprestimo, usuarios=usuarios, livros=livros)


@app.route("/emprestimo/excluir/<int:id>", methods=["GET", "POST"])
def excluir_emprestimo(id):
    try:
        db.session.execute(
            text("DELETE FROM Emprestimos WHERE ID_emprestimo = :id"),
            {"id": id}
        )
        db.session.commit()
        flash("Empréstimo excluído com sucesso!", "success")

    except Exception as e:
        db.session.rollback()
        flash(str(e), "danger")

    return redirect(url_for("listar_emprestimos"))




@app.route("/livros")
def listar_livros():
    try:
        livros = db.session.execute(text("""
            SELECT L.*, 
                   A.Nome_autor AS autor_nome,
                   G.Nome_genero AS genero_nome,
                   E.Nome_editora AS editora_nome
            FROM Livros L
            LEFT JOIN Autores A ON L.Autor_id = A.ID_autor
            LEFT JOIN Generos G ON L.Genero_id = G.ID_genero
            LEFT JOIN Editoras E ON L.Editora_id = E.ID_editora
        """)).fetchall()
        return render_template("livros/listar_livros.html", livros=livros)

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))


@app.route("/livro/novo", methods=["GET", "POST"])
def novo_livro():
    if request.method == "POST":
        try:
            db.session.execute(text("""
                INSERT INTO Livros 
                (Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, Editora_id, Quantidade_disponivel, Resumo)
                VALUES (:titulo, :autor, :isbn, :ano, :genero, :editora, :quantidade, :resumo)
            """), {
                "titulo": request.form.get("titulo"),
                "autor": request.form.get("autor_id"),
                "isbn": request.form.get("isbn"),
                "ano": request.form.get("ano"),
                "genero": request.form.get("genero_id"),
                "editora": request.form.get("editora_id"),
                "quantidade": request.form.get("quantidade"),
                "resumo": request.form.get("resumo")
            })

            db.session.commit()
            flash("Livro cadastrado com sucesso!", "success")
            return redirect(url_for("listar_livros"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    autores = db.session.execute(text("SELECT * FROM Autores")).fetchall()
    generos = db.session.execute(text("SELECT * FROM Generos")).fetchall()
    editoras = db.session.execute(text("SELECT * FROM Editoras")).fetchall()
    return render_template("livros/novo_livro.html",
                           autores=autores,
                           generos=generos,
                           editoras=editoras)


@app.route("/livro/editar/<int:id>", methods=["GET", "POST"])
def editar_livro(id):
    if request.method == "POST":
        try:
            db.session.execute(text("""
                UPDATE Livros SET
                    Titulo = :titulo,
                    Autor_id = :autor,
                    ISBN = :isbn,
                    Ano_publicacao = :ano,
                    Genero_id = :genero,
                    Editora_id = :editora,
                    Quantidade_disponivel = :quantidade,
                    Resumo = :resumo
                WHERE ID_livro = :id
            """), {
                "titulo": request.form.get("titulo"),
                "autor": request.form.get("autor_id"),
                "isbn": request.form.get("isbn"),
                "ano": request.form.get("ano"),
                "genero": request.form.get("genero_id"),
                "editora": request.form.get("editora_id"),
                "quantidade": request.form.get("quantidade"),
                "resumo": request.form.get("resumo"),
                "id": id
            })

            db.session.commit()
            flash("Livro editado com sucesso!", "success")
            return redirect(url_for("listar_livros"))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

    livro = db.session.execute(
        text("SELECT * FROM Livros WHERE ID_livro = :id"),
        {"id": id}
    ).fetchone()
    autores = db.session.execute(text("SELECT * FROM Autores")).fetchall()
    generos = db.session.execute(text("SELECT * FROM Generos")).fetchall()
    editoras = db.session.execute(text("SELECT * FROM Editoras")).fetchall()
    return render_template("livros/editar_livro.html",
                           livro=livro,
                           autores=autores,
                           generos=generos,
                           editoras=editoras)


@app.route("/livro/excluir/<int:id>", methods=["GET", "POST"])
def excluir_livro(id):
    try:
        db.session.execute(
            text("DELETE FROM Livros WHERE ID_livro = :id"),
            {"id": id}
        )
        db.session.commit()
        flash("Livro excluído com sucesso!", "success")

    except Exception as e:
        db.session.rollback()
        flash(str(e), "danger")

    return redirect(url_for("listar_livros"))




if __name__ == "__main__":
    app.run(debug=True)
