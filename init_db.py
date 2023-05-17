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
try:
    cur.execute('CREATE TABLE IF NOT EXISTS estudante (id serial PRIMARY KEY,inst VARCHAR(50) NOT NULL,nome VARCHAR(50) NOT NULL ,serie INT NOT NULL);')
    conn.commit()
          
     
except Exception as e:    
    print('Log de erro =>',e)
finally:
     print('Tabela Estudante CARREGADA com Sucesso.')
    
    

try:
    cur.execute('CREATE TABLE IF NOT EXISTS questoes (id serial PRIMARY KEY, titulo VARCHAR  NOT NULL, enunciado VARCHAR(10000) NOT NULL, imagem VARCHAR, a VARCHAR NOT NULL ,b VARCHAR NOT NULL ,c VARCHAR NOT NULL ,d VARCHAR NOT NULL  ,valor VARCHAR);')
    conn.commit()
             

except Exception as e:
    print('Log de Erro =>',e)
finally:
     print('Tabela Questões CARREGADA com Sucesso.')
     

   
    


