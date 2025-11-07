import mysql.connector

def initDatabase():
    connection = mysql.connector.connect(
        host="localhost",
        user="root"
    )
    
    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS db_atividade17;")
    cursor.execute("USE db_atividade17;")

    with open('database/schema.sql', 'r') as schema_file:
        schema_sql = schema_file.read()

    commands = schema_sql.split(';')  # Divide o script em cada ;

    try:
        for command in commands:
            command = command.strip()  # Remove espaços extras
            if command:  # Ignora comandos vazios
                cursor.execute(command)
        print("Banco de dados e tabelas criados com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao executar o script: {err}")
    finally:
        cursor.close()
        connection.commit()
        connection.close()
# TUDO ISSO PQ O PYTHON N QUER ACEITAR O MULTI=TRUE E EU N SEI PQ AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH
initDatabase()
