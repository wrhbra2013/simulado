from sqlalchemy import create_engine


#Configurar Banco de Dados Postgresql
sql = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")

#Criando tabela Aluno
sql.execute('DROP TABLE IF EXISTS estudante;')
if (sql.execute('CREATE TABLE estudante (id serial PRIMARY KEY,inst VARCHAR(50) NOT NULL,nome VARCHAR(50) NOT NULL ,serie INT NOT NULL);')):
  print('Tabela Estudante criada com sucesso!!')
else:
  print('Erro ao criar tabela Estudante')

#Criar tabela Questões
