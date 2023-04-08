from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

#Configurar Banco de Dados Postgresql
def conexao():  
  global psql 
  psql = create_engine("postgresql://postgres:postgres@localhost:5432/postgres",poolclass=NullPool)
  
  return psql

#Instanciar função
psql = conexao()

#Ler cnfigurações de tabela padrão.
with open("table.sql") as arquivo:
    psql.execute(arquivo.read())
    

print("Tabelas Estudante e Questões Criadas com Sucesso.")


