CREATE DATABASE IF NOT EXISTS db_atividade17;
USE db_atividade17;

CREATE TABLE Autores (
    ID_autor INT AUTO_INCREMENT PRIMARY KEY,
    Nome_autor VARCHAR(255) NOT NULL,
    Nacionalidade VARCHAR(255),
    Data_nascimento DATE,
    Biografia TEXT
);

CREATE TABLE Generos (
    ID_genero INT AUTO_INCREMENT PRIMARY KEY,
    Nome_genero VARCHAR(255) NOT NULL
);

CREATE TABLE Editoras (
    ID_editora INT AUTO_INCREMENT PRIMARY KEY,
    Nome_editora VARCHAR(255) NOT NULL,
    Endereco_editora TEXT
);

CREATE TABLE Livros (
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
);

CREATE TABLE Usuarios (
    ID_usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nome_usuario VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Numero_telefone VARCHAR(15),
    Data_inscricao DATE DEFAULT CURRENT_DATE,
    Multa_atual DECIMAL(10,2) DEFAULT 0.00
);

CREATE TABLE Emprestimos (
    ID_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    Usuario_id INT,
    Livro_id INT,
    Data_emprestimo DATE,
    Data_devolucao_prevista DATE,
    Data_devolucao_real DATE,
    Status_emprestimo ENUM('pendente', 'devolvido', 'atrasado') DEFAULT 'pendente',
    FOREIGN KEY (Usuario_id) REFERENCES Usuarios(ID_usuario),
    FOREIGN KEY (Livro_id) REFERENCES Livros(ID_livro)
);

CREATE TABLE Logs_Auditoria (
    ID_log INT AUTO_INCREMENT PRIMARY KEY,
    Tabela_afetada VARCHAR(50),
    Operacao VARCHAR(20),
    Descricao TEXT,
    Data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_validar_estoque_livro
BEFORE INSERT ON Emprestimos
FOR EACH ROW
SET @qtd = (SELECT Quantidade_disponivel FROM Livros WHERE ID_livro = NEW.Livro_id);

CREATE TRIGGER trg_baixar_estoque_livro
AFTER INSERT ON Emprestimos
FOR EACH ROW
UPDATE Livros
SET Quantidade_disponivel = Quantidade_disponivel - 1
WHERE ID_livro = NEW.Livro_id;

CREATE TRIGGER trg_preencher_usuario
BEFORE INSERT ON Usuarios
FOR EACH ROW
SET NEW.Data_inscricao = IFNULL(NEW.Data_inscricao, CURDATE()),
    NEW.Multa_atual = IFNULL(NEW.Multa_atual, 0.00);

CREATE TRIGGER trg_log_novo_emprestimo
AFTER INSERT ON Emprestimos
FOR EACH ROW
INSERT INTO Logs_Auditoria (Tabela_afetada, Operacao, Descricao)
VALUES (
    'Emprestimos',
    'INSERT',
    CONCAT('Empréstimo criado | Usuário ID: ', NEW.Usuario_id, ' | Livro ID: ', NEW.Livro_id)
);

CREATE TRIGGER trg_status_atrasado
BEFORE UPDATE ON Emprestimos
FOR EACH ROW
SET NEW.Status_emprestimo = IF(NEW.Data_devolucao_real IS NULL AND NEW.Data_devolucao_prevista < CURDATE(), 'atrasado', NEW.Status_emprestimo);
