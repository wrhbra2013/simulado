# Módulos
from flask import Flask, render_template, request, redirect,url_for, flash
from sqlalchemy import create_engine

#cabeçalho Flask app
app = Flask(__name__)
app.config['SECRET_KEY']='simulado'

#Realizar Operações no banco
sql = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")



#Pagina Boas Vindas
@app.route("/",methods=('GET','POST'))
def boas_vindas():
     if request.method =='POST':
     
        #Recebe dados
        escola = request.form['inst']
        user = request.form['nome']
        ano = request.form['serie']

        #Pesquisar no Banco de Dados
        pesquisa = sql.execute(f"SELECT inst, nome, serie FROM estudante where inst={escola} and nome={user} and serie={ano};")
        print(pesquisa)
        resultado = pesquisa.fetchall()
        
        if resultado == None:
            flash('Usuario NÃO Encontrado. \n Digite novamente! \n Ou Cadastre-se!')
        else:
            return redirect(url_for('home'))

     
     return render_template('index.html')     


      
#Pagina de cadastro
@app.route("/cadastro",methods=('GET','POST'))
def cadastro():
    if request.method =='POST':                       

        #Recebe dados
        escola = request.form['inst']
        user = request.form['nome']
        ano = request.form['serie']

        #Pesquisar no Banco de Dados
        sql.execute(f"INSERT INTO estudante(inst, nome, serie) VALUES ({escola},{user},{ano});")
                
        flash(f"Usuario {user} REGISTRADO com sucesso.!!")   
  
    return render_template('cadastro.html')

@app.route("/home",methods=('GET','POST'))
def home():
    flash('Bem Vindo' )   
  
    return render_template('home.html')




if __name__=="main":
    app.run()