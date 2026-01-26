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


   #Gatilhos de Validação
#GATILHO 1
#Não permite livro com quantidade negativa
CREATE TRIGGER trg_valida_quantidade_livro
BEFORE INSERT ON Livros
FOR EACH ROW
BEGIN
    IF NEW.Quantidade_disponivel < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantidade inválida';
    END IF;
END$$

#GATILHO 2
#Não permite ISBN repetido
CREATE TRIGGER trg_valida_isbn
BEFORE INSERT ON Livros
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT * FROM Livros WHERE ISBN = NEW.ISBN) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ISBN já cadastrado';
    END IF;
END$$

#GATILHO 3
#Não permite empréstimo se não houver livro disponível
CREATE TRIGGER trg_valida_emprestimo_livro
BEFORE INSERT ON Emprestimos
FOR EACH ROW
BEGIN
    IF (SELECT Quantidade_disponivel 
        FROM Livros 
        WHERE ID_livro = NEW.Livro_id) <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Livro indisponível';
    END IF;
END$$

#GATILHO 4
# Não permite empréstimo se o usuário tiver multa
CREATE TRIGGER trg_valida_multa_usuario
BEFORE INSERT ON Emprestimos
FOR EACH ROW
BEGIN
    IF (SELECT Multa_atual 
        FROM Usuarios 
        WHERE ID_usuario = NEW.Usuario_id) > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Usuário com multa';
    END IF;
END$$

#GATILHO 5
#Não permite devolver antes da data do empréstimo
CREATE TRIGGER trg_valida_data_devolucao
BEFORE UPDATE ON Emprestimos
FOR EACH ROW
BEGIN
    IF NEW.Data_devolucao_real < OLD.Data_emprestimo THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Data de devolução inválida';
    END IF;
END$$


#Geração Automática de Valores
#GATILHO 6
#Preenche automaticamente data de inscrição e multa
CREATE TRIGGER trg_data_usuario
BEFORE INSERT ON Usuarios
FOR EACH ROW
BEGIN
    SET NEW.Data_inscricao = CURDATE();
    SET NEW.Multa_atual = 0;
END$$

#GATILHO 7
#Preenche data e status do empréstimo
CREATE TRIGGER trg_data_emprestimo
BEFORE INSERT ON Emprestimos
FOR EACH ROW
BEGIN
    SET NEW.Data_emprestimo = CURDATE();
    SET NEW.Status_emprestimo = 'pendente';
END$$

# GATILHO 8
#Define a devolução prevista para 7 dias
CREATE TRIGGER trg_data_prevista
BEFORE INSERT ON Emprestimos
FOR EACH ROW
BEGIN
    SET NEW.Data_devolucao_prevista =
        DATE_ADD(CURDATE(), INTERVAL 7 DAY);
END$$

#GATILHO 9
#Diminui a quantidade do livro ao emprestar
CREATE TRIGGER trg_baixa_livro
AFTER INSERT ON Emprestimos
FOR EACH ROW
BEGIN
    UPDATE Livros
    SET Quantidade_disponivel = Quantidade_disponivel - 1
    WHERE ID_livro = NEW.Livro_id;
END$$

#GATILHO 10
#Aumenta a quantidade do livro ao devolver
CREATE TRIGGER trg_devolve_livro
AFTER UPDATE ON Emprestimos
FOR EACH ROW
BEGIN
    IF NEW.Status_emprestimo = 'devolvido' THEN
        UPDATE Livros
        SET Quantidade_disponivel = Quantidade_disponivel + 1
        WHERE ID_livro = NEW.Livro_id;
    END IF;
END$$

DELIMITER ;


#GATILHOS DE AUDITORIA
#➡️1. Registrar operações de INSERT, UPDATE e DELETE na tabela Autores
DELIMITER $$
CREATE TRIGGER trg_auditoria_autores
AFTER INSERT ON Autores
FOR EACH ROW
BEGIN
    INSERT INTO Logs_Auditoria (Tabela_afetada, Operacao, Descricao)
    VALUES ('Autores', 'INSERT', CONCAT('Autor inserido: ID ', NEW.ID_autor, ' | Nome: ', NEW.Nome_autor));
END$$

CREATE TRIGGER trg_auditoria_autores_update
AFTER UPDATE ON Autores
FOR EACH ROW
BEGIN
    INSERT INTO Logs_Auditoria (Tabela_afetada, Operacao, Descricao)
    VALUES ('Autores', 'UPDATE', CONCAT('Autor atualizado: ID ', OLD.ID_autor, ' | De: ', OLD.Nome_autor, ' Para: ', NEW.Nome_autor));
END$$

CREATE TRIGGER trg_auditoria_autores_delete
AFTER DELETE ON Autores
FOR EACH ROW
BEGIN
    INSERT INTO Logs_Auditoria (Tabela_afetada, Operacao, Descricao)
    VALUES ('Autores', 'DELETE', CONCAT('Autor excluído: ID ', OLD.ID_autor, ' | Nome: ', OLD.Nome_autor));
END$$
DELIMITER ;

#➡️2. Registrar dados antigos e novos em alterações na tabela Livros
DELIMITER $$
CREATE TRIGGER trg_auditoria_livros_detalhado
AFTER UPDATE ON Livros
FOR EACH ROW
BEGIN
    IF OLD.Titulo != NEW.Titulo OR OLD.Quantidade_disponivel != NEW.Quantidade_disponivel THEN
        INSERT INTO Logs_Auditoria (Tabela_afetada, Operacao, Descricao)
        VALUES ('Livros', 'UPDATE', 
            CONCAT('Livro ID ', OLD.ID_livro, 
                   ' | Título alterado de "', OLD.Titulo, '" para "', NEW.Titulo, '"',
                   ' | Estoque de ', OLD.Quantidade_disponivel, ' para ', NEW.Quantidade_disponivel));
    END IF;
END$$
DELIMITER ;

#➡️3. Registrar o cadastro de novos usuários (equivalente a "novos alunos")
DELIMITER $$
CREATE TRIGGER trg_auditoria_novo_usuario
AFTER INSERT ON Usuarios
FOR EACH ROW
BEGIN
    INSERT INTO Logs_Auditoria (Tabela_afetada, Operacao, Descricao)
    VALUES ('Usuarios', 'INSERT', CONCAT('Usuário cadastrado: ID ', NEW.ID_usuario, ' | Nome: ', NEW.Nome_usuario, ' | Email: ', NEW.Email));
END$$
DELIMITER ;

#➡️4. Registrar atualizações na tabela Emprestimos (equivalente a "tabela de Notas")
DELIMITER $$
CREATE TRIGGER trg_auditoria_emprestimos
AFTER UPDATE ON Emprestimos
FOR EACH ROW
BEGIN
    IF OLD.Status_emprestimo != NEW.Status_emprestimo THEN
        INSERT INTO Logs_Auditoria (Tabela_afetada, Operacao, Descricao)
        VALUES ('Emprestimos', 'UPDATE', 
            CONCAT('Empréstimo ID ', OLD.ID_emprestimo,
                   ' | Status alterado de "', OLD.Status_emprestimo, '" para "', NEW.Status_emprestimo, '"'));
    END IF;
END$$
DELIMITER ;

#➡️5. Registrar exclusão de livros (equivalente a "exclusão de disciplinas")
DELIMITER $$
CREATE TRIGGER trg_auditoria_livros_delete
AFTER DELETE ON Livros
FOR EACH ROW
BEGIN
    INSERT INTO Logs_Auditoria (Tabela_afetada, Operacao, Descricao)
    VALUES ('Livros', 'DELETE', CONCAT('Livro excluído: ID ', OLD.ID_livro, ' | Título: ', OLD.Titulo));
END$$
DELIMITER ;


#GATILHOS DE ATUALIZAÇÃO AUTOMÁTICA PÓS-EVENTO
#➡️1. Ajustar dados de outras tabelas automaticamente: Ao excluir um autor, definir Autor_id = NULL nos livros associados
DELIMITER $$
CREATE TRIGGER trg_ajustar_livros_apagar_autor
BEFORE DELETE ON Autores
FOR EACH ROW
BEGIN
    UPDATE Livros 
    SET Autor_id = NULL 
    WHERE Autor_id = OLD.ID_autor;
END$$
DELIMITER ;

#➡️2. Refletir ações que desencadeiam mudanças em cascata: Ao excluir um gênero, remover referência nos livros
DELIMITER $$
CREATE TRIGGER trg_remover_genero_livros
BEFORE DELETE ON Generos
FOR EACH ROW
BEGIN
    UPDATE Livros 
    SET Genero_id = NULL 
    WHERE Genero_id = OLD.ID_genero;
END$$
DELIMITER ;

#➡️3. Alterar situação do usuário para “inativo” quando todas as matrículas forem canceladas → Adaptado para usuário sem empréstimos ativos
DELIMITER $$
CREATE TRIGGER trg_verificar_usuario_inativo
AFTER DELETE ON Emprestimos
FOR EACH ROW
BEGIN
    DECLARE total_emprestimos INT;
    
    SELECT COUNT(*) INTO total_emprestimos
    FROM Emprestimos 
    WHERE Usuario_id = OLD.Usuario_id 
      AND Status_emprestimo = 'pendente';

    IF total_emprestimos = 0 THEN
        UPDATE Usuarios 
        SET Email = CONCAT(Email, ' (SEM EMPRÉSTIMOS ATIVOS)') 
        WHERE ID_usuario = OLD.Usuario_id;
    END IF;
END$$
DELIMITER ;

#➡️4. Ajustar carga horária total de um curso → Adaptado para recalcular total de livros por autor
DELIMITER $$
CREATE TRIGGER trg_recalcular_livros_autor
AFTER INSERT ON Livros
FOR EACH ROW
BEGIN
    UPDATE Autores 
    SET Biografia = CONCAT(Biografia, ' | Total de livros atualizado em: ', CURDATE())
    WHERE ID_autor = NEW.Autor_id;
END$$

CREATE TRIGGER trg_recalcular_livros_autor_delete
AFTER DELETE ON Livros
FOR EACH ROW
BEGIN
    UPDATE Autores 
    SET Biografia = CONCAT(Biografia, ' | Livro removido em: ', CURDATE())
    WHERE ID_autor = OLD.Autor_id;
END$$
DELIMITER ;

#➡️5. Remover notas automaticamente ao cancelar uma matrícula → Adaptado para cancelar empréstimos ao excluir usuário
DELIMITER $$
CREATE TRIGGER trg_excluir_emprestimos_usuario
BEFORE DELETE ON Usuarios
FOR EACH ROW
BEGIN
    DELETE FROM Emprestimos WHERE Usuario_id = OLD.ID_usuario;
END$$
DELIMITER ;