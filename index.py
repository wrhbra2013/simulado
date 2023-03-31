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

        #Tratando erros
        try:
            #Pesquisar no Banco de Dados
            pesquisa = sql.execute(f"SELECT inst,nome,ano FROM estudante where inst='{escola}' and nome='{user}' and serie='{ano}';").scalar()
            print(pesquisa)
            

            if pesquisa == None:
                flash('Usuario NÃO Encontrado. Digite novamente! Ou Cadastre-se!')                                
                          

        except Exception:
            flash('Campos Vazios ou erro de digitação. Por favor digite novamente!')
        finally:
             return render_template('home.html')

            
        
     
     return render_template('index.html')

@app.route("/index",methods=('GET','POST'))
def index():
     if request.method == 'GET':
         flash('Entre com suas credenciais.')
     
     if request.method =='POST':
     
        #Recebe dados
        escola = request.form['inst']
        user = request.form['nome']
        ano = request.form['serie']

        #Tratando erros
        try:
            #Pesquisar no Banco de Dados
            pesquisa = sql.execute(f"SELECT inst, nome, ano FROM estudante where inst='{escola}' and nome='{user}' and serie='{ano}';").scalar()
            print(pesquisa)
            

            if pesquisa == None:
                flash('Usuario NÃO Encontrado. Digite novamente! Ou Cadastre-se!')                      
                            
                         

        except Exception as e:
            print(e)
            flash('Campos Vazios ou erro de digitação. Por favor digite novamente!')  
        finally: 
            return render_template('home.html')

     
     return render_template('index.html')


      
#Pagina de cadastro
@app.route("/cadastro",methods=('GET','POST'))
def cadastro():
    if request.method =='POST':                       

        #Recebe dados
        escola = request.form['inst']
        user = request.form['nome']
        ano = request.form['serie']
        
        try:
            #Pesquisar no Banco de Dados
            sql.execute(f"INSERT INTO estudante(inst, nome, serie) VALUES ('{escola}','{user}','{ano}');")
                  
            flash(f"Usuario {user} REGISTRADO com sucesso.!!")
        except Exception:
            flash('Campos Vazios Ou erro de digitação. Favor digite novamente.')
          
    return render_template('cadastro.html')

@app.route("/home",methods=('GET','POST'))
def home():
    
    flash('Bem Vindo' )   
  
    return render_template('home.html')

@app.route("/gabarito")
def gabarito():
    return render_template('gabarito.html')

@app.route("/sobre")
def sobre():
    return render_template('sobre.html')






if __name__=="main":
    app.run()