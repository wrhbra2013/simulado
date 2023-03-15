# Módulos
from flask import Flask, render_template, request, redirect
import psycopg2

#cabeçalho Flask app
app = Flask(__name__)

#Configurar Banco de Dados Postgresql
def conexao():
    psql = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/postgres")
    return psql


#Pagina Boas Vindas
@app.route("/",methods=['GET','POST'])
def boas_vindas():
    if request.method =='POST':
        psql = conexao()

        #Recebe dados
        instituicao = request.form['inst']
        nomeUsuario = request.form['nome']
        serieUsuario = request.form['serie']

    
    return render_template('index.html')

@app.route("/cadastro",methods=['GET','POST'])
def cadastro():   
  
    return render_template('cadastro.html')

@app.route("/home",methods=['GET','POST'])
def home():   
  
    return render_template('home.html')




if __name__=="main":
    app.run()