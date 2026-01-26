# Por algum motivo não consigo rodar o schema.sql :(
import mysql.connector

def initDatabase():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    
    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS db_atividade17;")
    cursor.execute("USE db_atividade17;")

    tabelas_sql = [
        """
        CREATE TABLE IF NOT EXISTS Autores (
            ID_autor INT AUTO_INCREMENT PRIMARY KEY,
            Nome_autor VARCHAR(255) NOT NULL,
            Nacionalidade VARCHAR(255),
            Data_nascimento DATE,
            Biografia TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Generos (
            ID_genero INT AUTO_INCREMENT PRIMARY KEY,
            Nome_genero VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Editoras (
            ID_editora INT AUTO_INCREMENT PRIMARY KEY,
            Nome_editora VARCHAR(255) NOT NULL,
            Endereco_editora TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Livros (
            ID_livro INT AUTO_INCREMENT PRIMARY KEY,
            Titulo VARCHAR(255) NOT NULL,
            Autor_id INT,
            ISBN VARCHAR(13) NOT NULL,
            Ano_publicacao INT,
            Genero_id INT,
            Editora_id INT,
            Quantidade_disponivel INT,
            Resumo TEXT,
            FOREIGN KEY (Autor_id) REFERENCES Autores(ID_autor),
            FOREIGN KEY (Genero_id) REFERENCES Generos(ID_genero),
            FOREIGN KEY (Editora_id) REFERENCES Editoras(ID_editora)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Usuarios (
            ID_usuario INT AUTO_INCREMENT PRIMARY KEY,
            Nome_usuario VARCHAR(255) NOT NULL,
            Email VARCHAR(255),
            Numero_telefone VARCHAR(15),
            Data_inscricao DATE DEFAULT CURRENT_DATE,
            Multa_atual DECIMAL(10,2) DEFAULT 0.00
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Emprestimos (
            ID_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
            Usuario_id INT,
            Livro_id INT,
            Data_emprestimo DATE,
            Data_devolucao_prevista DATE,
            Data_devolucao_real DATE,
            Status_emprestimo ENUM('pendente', 'devolvido', 'atrasado') DEFAULT 'pendente',
            FOREIGN KEY (Usuario_id) REFERENCES Usuarios(ID_usuario),
            FOREIGN KEY (Livro_id) REFERENCES Livros(ID_livro)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Logs_Auditoria (
            ID_log INT AUTO_INCREMENT PRIMARY KEY,
            Tabela_afetada VARCHAR(50),
            Operacao VARCHAR(20),
            Descricao TEXT,
            Data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    for sql in tabelas_sql:
        cursor.execute(sql)

    triggers_sql = [
        """
        CREATE TRIGGER IF NOT EXISTS trg_baixar_estoque_livro
        AFTER INSERT ON Emprestimos
        FOR EACH ROW
        UPDATE Livros
        SET Quantidade_disponivel = Quantidade_disponivel - 1
        WHERE ID_livro = NEW.Livro_id
        """,
        """
        CREATE TRIGGER IF NOT EXISTS trg_preencher_usuario
        BEFORE INSERT ON Usuarios
        FOR EACH ROW
        SET NEW.Data_inscricao = IFNULL(NEW.Data_inscricao, CURDATE()),
            NEW.Multa_atual = IFNULL(NEW.Multa_atual, 0.00)
        """,
        """
        CREATE TRIGGER IF NOT EXISTS trg_log_novo_emprestimo
        AFTER INSERT ON Emprestimos
        FOR EACH ROW
        INSERT INTO Logs_Auditoria (Tabela_afetada, Operacao, Descricao)
        VALUES (
            'Emprestimos',
            'INSERT',
            CONCAT('Empréstimo criado | Usuário ID: ', NEW.Usuario_id, ' | Livro ID: ', NEW.Livro_id)
        )
        """,
        """
        CREATE TRIGGER IF NOT EXISTS trg_status_atrasado
        BEFORE UPDATE ON Emprestimos
        FOR EACH ROW
        SET NEW.Status_emprestimo = IF(
            NEW.Data_devolucao_real IS NULL AND NEW.Data_devolucao_prevista < CURDATE(),
            'atrasado',
            NEW.Status_emprestimo
        )
        """
    ]

    for trigger_sql in triggers_sql:
        try:
            cursor.execute(trigger_sql)
        except mysql.connector.Error as err:
            print(f"Erro ao criar trigger (pode já existir): {err}")

    connection.commit()
    cursor.close()
    connection.close()
    print("Banco de dados e tabelas criados com triggers funcionais.")

if __name__ == "__main__":
    initDatabase()
