#Bibliotecas
import psycopg2
import psycopg2.extras

#Configurar Banco de Dados Postgresql
def conexao():
    #Conexão Local
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost",port="5432")
    #Conexão railway
    #conn = psycopg2.connect("postgresql://postgres:RatcGkjPcIUg0QT17nsA@containers-us-west-75.railway.app:6160/railway")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn, cur
conn, cur = conexao()

    
#Mensagem
try:
    cur.execute('CREATE TABLE IF NOT EXISTS estudante (id serial PRIMARY KEY,inst VARCHAR(30) NOT NULL,nome VARCHAR(30) NOT NULL ,cidade VARCHAR(30),serie INT NOT NULL, last_update TIMESTAMP DEFAULT now()::timestamp(0));')
    conn.commit()
          
     
except Exception as e:    
    print('Log de erro =>',e)
finally:
     print('Tabela Estudante CARREGADA com Sucesso.')
    
    

try:
    cur.execute('CREATE TABLE IF NOT EXISTS questoes (id serial PRIMARY KEY, competencia VARCHAR(70), titulo VARCHAR  NOT NULL, enunciado VARCHAR(10000) NOT NULL, imagem VARCHAR, a VARCHAR NOT NULL ,b VARCHAR NOT NULL ,c VARCHAR NOT NULL ,d VARCHAR NOT NULL  ,valor VARCHAR, last_update TIMESTAMP DEFAULT now()::timestamp(0));')
    conn.commit()
             

except Exception as e:
    print('Log de Erro =>',e)
finally:
     print('Tabela Questões CARREGADA com Sucesso.')
     
try:
    cur.execute('CREATE TABLE IF NOT EXISTS resultados (id serial PRIMARY KEY, estudante_escola VARCHAR(30) NOT NULL, estudante_nome VARCHAR(30) NOT NULL,  questao_id INT, questao_enunciado VARCHAR(10000), questao_valor VARCHAR(2), alternativa VARCHAR(2), nota INT, last_update TIMESTAMP DEFAULT now()::timestamp(0));')
    conn.commit()
             

except Exception as e:
    print('Log de Erro =>',e)
finally:
     print('Tabela Resultados CARREGADA com Sucesso.')
     

try:
    cur.execute('CREATE TABLE IF NOT EXISTS comentarios (id serial PRIMARY KEY, nome VARCHAR(30),contato VARCHAR(30),assunto VARCHAR(30), comentario VARCHAR, last_update TIMESTAMP DEFAULT now()::timestamp(0));')
    conn.commit()           

except Exception as e:
    print('Log de Erro =>',e)
finally:
    print('Comentarios...')
    
    
    


