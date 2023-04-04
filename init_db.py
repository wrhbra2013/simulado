from index import psql 



#Criando tabela Aluno
psql.execute('DROP TABLE IF EXISTS estudante;')
if (psql.execute('CREATE TABLE estudante (id serial PRIMARY KEY,inst VARCHAR(50) NOT NULL,nome VARCHAR(50) NOT NULL ,serie INT NOT NULL);')):
  print('Tabela Estudante criada com sucesso!!')
else:
  print('Erro ao criar tabela Estudante')

#Criar tabela Questões
psql.execute('DROP TABLE IF EXISTS questoes;')
if (psql.execute('CREATE TABLE questoes (id serial PRIMARY KEY, titulo VARCHAR(10000) NOT NULL, enunciado VARCHAR NOT NULL , imagem BYTEA, resposta BOOLEAN NOT NULL);')):
  print('Tabela Questões criada com sucesso!!')
else:
  print('Erro ao criar tabela Questões')
