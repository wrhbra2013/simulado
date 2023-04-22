#Bibliotecas
import psycopg2
import psycopg2.extras

#Configurar Banco de Dados Postgresql
def conexao():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost",port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn, cur
conn, cur = conexao()

    
#Mensagem
if (cur.execute('CREATE TABLE IF NOT EXISTS estudante (id serial PRIMARY KEY,inst VARCHAR(50) NOT NULL,nome VARCHAR(50) NOT NULL ,serie INT NOT NULL);')):
    conn.commit()
    print("Tabela Estudante Criada com Sucesso.")
else:
    print("Tabela Estudante Carregada com Sucesso.")
    
if (cur.execute('CREATE TABLE IF NOT EXISTS questoes (id serial PRIMARY KEY, titulo VARCHAR  NOT NULL, enunciado VARCHAR(10000) NOT NULL, imagem BYTEA,a VARCHAR NOT NULL ,b VARCHAR NOT NULL ,c VARCHAR NOT NULL ,d VARCHAR NOT NULL ,e VARCHAR NOT NULL ,valor boolean);')):
    conn.commit()
    print("Tabela Questões Criada com Sucesso.")
else:
    print("Tabela Questões Carregada com Sucesso.")




