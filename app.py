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
        autores = db.session.execute(text("SELECT * FROM Autores")).fetchall()
        return render_template("autores/listar_autores.html", autores=autores)
    except Exception as e:
        flash(f"Erro ao listar autores: {e}", "danger")
        return redirect(url_for("index"))


@app.route("/autor/novo", methods=["GET", "POST"])
def novo_autor():
    if request.method == "POST":
        try:
            sql = text("""
                INSERT INTO Autores (Nome_autor, Nacionalidade, Data_nascimento, Biografia)
                VALUES (:nome, :nac, :nasc, :bio)
            """)
            db.session.execute(sql, {
                "nome": request.form.get("nome"),
                "nac": request.form.get("nacionalidade"),
                "nasc": request.form.get("data_nascimento"),
                "bio": request.form.get("biografia")
            })
            db.session.commit()
            flash("Autor cadastrado com sucesso!", "success")
            return redirect(url_for("listar_autores"))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar autor: {e}", "danger")

    return render_template("autores/novo_autor.html")


@app.route("/autor/editar/<int:id>", methods=["GET", "POST"])
def editar_autor(id):
    if request.method == "POST":
        try:
            sql = text("""
                UPDATE Autores SET 
                Nome_autor=:nome, Nacionalidade=:nac, Data_nascimento=:nasc, Biografia=:bio
                WHERE ID_autor=:id
            """)
            db.session.execute(sql, {
                "nome": request.form.get("nome"),
                "nac": request.form.get("nacionalidade"),
                "nasc": request.form.get("data_nascimento"),
                "bio": request.form.get("biografia"),
                "id": id
            })
            db.session.commit()
            flash("Autor editado com sucesso!", "success")
            return redirect(url_for("listar_autores"))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao editar autor: {e}", "danger")

    autor = db.session.execute(
        text("SELECT * FROM Autores WHERE ID_autor=:id"), {"id": id}
    ).fetchone()

    return render_template("autores/editar_autor.html", autor=autor)


@app.route("/autor/excluir/<int:id>", methods=["GET", "POST"])
def excluir_autor(id):
    try:
        db.session.execute(text("DELETE FROM Autores WHERE ID_autor=:id"), {"id": id})
        db.session.commit()
        flash("Autor excluído!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir: {e}", "danger")

    return redirect(url_for("listar_autores"))





@app.route("/editoras")
def listar_editoras():
    editoras = db.session.execute(text("SELECT * FROM Editoras")).fetchall()
    return render_template("editoras/listar_editoras.html", editoras=editoras)


@app.route("/editora/nova", methods=["GET", "POST"])
def nova_editora():
    if request.method == "POST":
        try:
            db.session.execute(
                text("INSERT INTO Editoras (Nome_editora) VALUES (:n)"),
                {"n": request.form.get("nome")}
            )
            db.session.commit()
            flash("Editora cadastrada!", "success")
            return redirect(url_for("listar_editoras"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro: {e}", "danger")

    return render_template("editoras/nova_editora.html")


@app.route("/editora/editar/<int:id>", methods=["GET", "POST"])
def editar_editora(id):
    if request.method == "POST":
        try:
            db.session.execute(
                text("UPDATE Editoras SET Nome_editora=:n WHERE ID_editora=:id"),
                {"n": request.form.get("nome"), "id": id}
            )
            db.session.commit()
            flash("Editora editada!", "success")
            return redirect(url_for("listar_editoras"))
        except Exception as e:
            flash(f"Erro: {e}", "danger")

    editora = db.session.execute(
        text("SELECT * FROM Editoras WHERE ID_editora=:id"), {"id": id}
    ).fetchone()

    return render_template("editoras/editar_editora.html", editora=editora)


@app.route("/editora/excluir/<int:id>", methods=["GET", "POST"])
def excluir_editora(id):
    try:
        db.session.execute(text("DELETE FROM Editoras WHERE ID_editora=:id"), {"id": id})
        db.session.commit()
        flash("Editora excluída!", "success")
    except Exception as e:
        flash(f"Erro ao excluir: {e}", "danger")

    return redirect(url_for("listar_editoras"))





@app.route("/generos")
def listar_generos():
    generos = db.session.execute(text("SELECT * FROM Generos")).fetchall()
    return render_template("generos/listar_generos.html", generos=generos)


@app.route("/genero/novo", methods=["GET", "POST"])
def novo_genero():
    if request.method == "POST":
        try:
            db.session.execute(
                text("INSERT INTO Generos (Nome_genero) VALUES (:n)"),
                {"n": request.form.get("nome")}
            )
            db.session.commit()
            flash("Gênero cadastrado!", "success")
            return redirect(url_for("listar_generos"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro: {e}", "danger")

    return render_template("generos/novo_genero.html")


@app.route("/genero/editar/<int:id>", methods=["GET", "POST"])
def editar_genero(id):
    if request.method == "POST":
        try:
            db.session.execute(
                text("UPDATE Generos SET Nome_genero=:n WHERE ID_genero=:id"),
                {"n": request.form.get("nome"), "id": id}
            )
            db.session.commit()
            flash("Gênero editado!", "success")
            return redirect(url_for("listar_generos"))
        except Exception as e:
            flash(f"Erro: {e}", "danger")

    genero = db.session.execute(
        text("SELECT * FROM Generos WHERE ID_genero=:id"), {"id": id}
    ).fetchone()

    return render_template("generos/editar_genero.html", genero=genero)


@app.route("/genero/excluir/<int:id>", methods=["GET", "POST"])
def excluir_genero(id):
    try:
        db.session.execute(text("DELETE FROM Generos WHERE ID_genero=:id"), {"id": id})
        db.session.commit()
        flash("Gênero excluído!", "success")
    except Exception as e:
        flash(f"Erro ao excluir: {e}", "danger")

    return redirect(url_for("listar_generos"))




@app.route("/usuarios")
def listar_usuarios():
    usuarios = db.session.execute(text("SELECT * FROM Usuarios")).fetchall()
    return render_template("usuarios/listar_usuarios.html", usuarios=usuarios)


@app.route("/usuario/novo", methods=["GET", "POST"])
def novo_usuario():
    if request.method == "POST":
        try:
            sql = text("""
                INSERT INTO Usuarios (Nome_usuario, Email, Numero_telefone)
                VALUES (:n, :e, :t)
            """)
            db.session.execute(sql, {
                "n": request.form.get("nome"),
                "e": request.form.get("email"),
                "t": request.form.get("telefone")
            })
            db.session.commit()
            flash("Usuário cadastrado!", "success")
            return redirect(url_for("listar_usuarios"))

        except Exception as e:
            flash(f"Erro: {e}", "danger")

    return render_template("usuarios/novo_usuario.html")


@app.route("/usuario/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    if request.method == "POST":
        try:
            sql = text("""
                UPDATE Usuarios SET
                Nome_usuario=:n, Email=:e, Numero_telefone=:t
                WHERE ID_usuario=:id
            """)
            db.session.execute(sql, {
                "n": request.form.get("nome"),
                "e": request.form.get("email"),
                "t": request.form.get("telefone"),
                "id": id
            })
            db.session.commit()
            flash("Usuário editado!", "success")
            return redirect(url_for("listar_usuarios"))

        except Exception as e:
            flash(f"Erro: {e}", "danger")

    usuario = db.session.execute(
        text("SELECT * FROM Usuarios WHERE ID_usuario=:id"), {"id": id}
    ).fetchone()

    return render_template("usuarios/editar_usuario.html", usuario=usuario)


@app.route("/usuario/excluir/<int:id>", methods=["GET", "POST"])
def excluir_usuario(id):
    try:
        db.session.execute(text("DELETE FROM Usuarios WHERE ID_usuario=:id"), {"id": id})
        db.session.commit()
        flash("Usuário excluído!", "success")
    except Exception as e:
        flash(f"Erro: {e}", "danger")

    return redirect(url_for("listar_usuarios"))





@app.route("/emprestimos")
def listar_emprestimos():
    sql = text("""
        SELECT E.*, 
            U.Nome_usuario AS usuario_nome, 
            L.Titulo AS livro_titulo
        FROM Emprestimos E
        LEFT JOIN Usuarios U ON E.Usuario_id = U.ID_usuario
        LEFT JOIN Livros L ON E.Livro_id = L.ID_livro
    """)
    emprestimos = db.session.execute(sql).fetchall()
    return render_template("emprestimos/listar_emprestimos.html", emprestimos=emprestimos)


@app.route("/emprestimo/novo", methods=["GET", "POST"])
def novo_emprestimo():
    if request.method == "POST":
        try:
            sql = text("""
                INSERT INTO Emprestimos (Usuario_id, Livro_id, Data_emprestimo, Data_devolucao_prevista)
                VALUES (:u, :l, :de, :dd)
            """)
            db.session.execute(sql, {
                "u": request.form.get("usuario_id"),
                "l": request.form.get("livro_id"),
                "de": request.form.get("data_emprestimo"),
                "dd": request.form.get("data_prevista")
            })
            db.session.commit()
            flash("Emprestimo cadastrado!", "success")
            return redirect(url_for("listar_emprestimos"))

        except Exception as e:
            flash(f"Erro: {e}", "danger")

    usuarios = db.session.execute(text("SELECT * FROM Usuarios")).fetchall()
    livros = db.session.execute(text("SELECT * FROM Livros")).fetchall()

    return render_template("emprestimos/novo_emprestimo.html",
                           usuarios=usuarios, livros=livros)


@app.route("/emprestimo/editar/<int:id>", methods=["GET", "POST"])
def editar_emprestimo(id):
    if request.method == "POST":
        try:
            sql = text("""
                UPDATE Emprestimos SET
                Usuario_id=:u, Livro_id=:l, Data_emprestimo=:de, 
                Data_devolucao_prevista=:ddp, Data_devolucao_real=:ddr,
                Status_emprestimo=:s
                WHERE ID_emprestimo=:id
            """)
            db.session.execute(sql, {
                "u": request.form.get("usuario_id"),
                "l": request.form.get("livro_id"),
                "de": request.form.get("data_emprestimo"),
                "ddp": request.form.get("data_prevista"),
                "ddr": request.form.get("data_real"),
                "s": request.form.get("status"),
                "id": id
            })
            db.session.commit()
            flash("Emprestimo editado!", "success")
            return redirect(url_for("listar_emprestimos"))

        except Exception as e:
            flash(f"Erro: {e}", "danger")

    emprestimo = db.session.execute(
        text("SELECT * FROM Emprestimos WHERE ID_emprestimo=:id"), {"id": id}
    ).fetchone()

    usuarios = db.session.execute(text("SELECT * FROM Usuarios")).fetchall()
    livros = db.session.execute(text("SELECT * FROM Livros")).fetchall()

    return render_template("emprestimos/editar_emprestimo.html",
                           emprestimo=emprestimo, usuarios=usuarios, livros=livros)


@app.route("/emprestimo/excluir/<int:id>", methods=["GET", "POST"])
def excluir_emprestimo(id):
    try:
        db.session.execute(text("DELETE FROM Emprestimos WHERE ID_emprestimo=:id"), {"id": id})
        db.session.commit()
        flash("Empréstimo excluído!", "success")
    except Exception as e:
        flash(f"Erro: {e}", "danger")

    return redirect(url_for("listar_emprestimos"))



@app.route("/livros")
def listar_livros():
    sql = text("""
        SELECT L.*, 
               A.Nome_autor AS autor_nome,
               G.Nome_genero AS genero_nome,
               E.Nome_editora AS editora_nome
        FROM Livros L
        LEFT JOIN Autores A ON L.Autor_id = A.ID_autor
        LEFT JOIN Generos G ON L.Genero_id = G.ID_genero
        LEFT JOIN Editoras E ON L.Editora_id = E.ID_editora
    """)
    livros = db.session.execute(sql).fetchall()
    return render_template("livros/listar_livros.html", livros=livros)


@app.route("/livro/novo", methods=["GET", "POST"])
def novo_livro():
    if request.method == "POST":
        try:
            sql = text("""
                INSERT INTO Livros 
                (Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, Editora_id, Quantidade_disponivel, Resumo)
                VALUES (:t, :a, :i, :ano, :g, :e, :q, :r)
            """)

            db.session.execute(sql, {
                "t": request.form.get("titulo"),
                "a": request.form.get("autor_id"),
                "i": request.form.get("isbn"),
                "ano": request.form.get("ano"),
                "g": request.form.get("genero_id"),
                "e": request.form.get("editora_id"),
                "q": request.form.get("quantidade"),
                "r": request.form.get("resumo")
            })
            db.session.commit()
            flash("Livro cadastrado!", "success")
            return redirect(url_for("listar_livros"))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar: {e}", "danger")

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
            sql = text("""
                UPDATE Livros SET
                    Titulo=:t,
                    Autor_id=:a,
                    ISBN=:i,
                    Ano_publicacao=:ano,
                    Genero_id=:g,
                    Editora_id=:e,
                    Quantidade_disponivel=:q,
                    Resumo=:r
                WHERE ID_livro=:id
            """)

            db.session.execute(sql, {
                "t": request.form.get("titulo"),
                "a": request.form.get("autor_id"),
                "i": request.form.get("isbn"),
                "ano": request.form.get("ano"),
                "g": request.form.get("genero_id"),
                "e": request.form.get("editora_id"),
                "q": request.form.get("quantidade"),
                "r": request.form.get("resumo"),
                "id": id
            })

            db.session.commit()
            flash("Livro editado!", "success")
            return redirect(url_for("listar_livros"))

        except Exception as e:
            flash(f"Erro ao editar: {e}", "danger")

    livro = db.session.execute(
        text("SELECT * FROM Livros WHERE ID_livro=:id"), {"id": id}
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
        db.session.execute(text("DELETE FROM Livros WHERE ID_livro=:id"), {"id": id})
        db.session.commit()
        flash("Livro excluído!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir livro: {e}", "danger")

    return redirect(url_for("listar_livros"))



if __name__ == "__main__":
    app.run(debug=True)
