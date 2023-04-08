# Módulos
from flask import Flask, render_template, request, redirect,url_for, flash,session
from init_db import psql as sql
import os as os
from werkzeug.utils import secure_filename


pasta_upload = 'static/upload/'
extensao_permitida = set(['jpeg','jpg','gif','png'])



#cabeçalho Flask app
app = Flask(__name__)
app.secret_key = 'simulado'
app.config ['pasta_upload'] = pasta_upload
app.config['tamanho_max'] = 16 * 1024 * 1024






#Pagina Boas Vindas
@app.route("/",methods=('GET','POST'))
def boas_vindas():
        
     if request.method =='POST':
     
        #Recebe dados
        escola = request.form['inst']
        user = request.form['nome']
        ano = request.form['serie']

        #Sessão do usuário
        session['usuario'] = user
        session.permanent = True
        
        #Tratando erros
        try:
            #Pesquisar no Banco de Dados
            pesquisa = sql.execute(f"SELECT inst, nome, serie FROM estudante where inst='{escola}' and nome='{user}' and serie='{ano}';").scalar()
            
            
            if pesquisa == None:
                flash('Usuario NÃO Encontrado. Digite novamente! Ou Cadastre-se!')
            else:
                return redirect(url_for('home',user=user))                          

        except Exception as e:
            print(e)
            flash('Campos Vazios ou erro de digitação. Por favor digite novamente!')
                 
        
     
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

        #Sessão do usuário
        session['usuario'] = user
        session.permanent = True
        

        #Tratando erros
        try:
            #Pesquisar no Banco de Dados
            pesquisa = sql.execute(f"SELECT inst, nome, serie FROM estudante where inst='{escola}' and nome='{user}' and serie='{ano}';").scalar()
                        

            if pesquisa == None:
                flash('Usuario NÃO Encontrado. Digite novamente! Ou Cadastre-se!')
            else:                
                return redirect(url_for('home',user=user))                  
                            
                         

        except Exception as e:
            print(e)
            flash('Campos Vazios ou erro de digitação. Por favor digite novamente!')  
        

     
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
            
        except Exception as e:
            print(e)
            flash('Campos Vazios Ou erro de digitação. Favor digite novamente.')
          
    return render_template('cadastro.html')

@app.route("/questoes",methods=('GET','POST'))
def questoes(): 
    if 'user' in session:
        user = session['user']
        flash(f"Bem Vindo, {user}")  
                          
    if request.method == 'POST':
        #recebe dados
        titulo = request.form['title']
        enunciado = request.form['enunciate']
        imagem = request.files['picture']
        oa = request.form['a']
        ob = request.form['b']
        oc = request.form['c']
        od = request.form['d']
        oe = request.form['e']
        
        #Armazenando imagens.
        if imagem.filename == '':
            flash('Nenhuma imagem selecionanda.')
            return redirect(request.url)
        
        if imagem and extensao_permitida(imagem.filename):
            imagem.filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['pasta_upload'],imagem.filename))
            flash('Imagem Armazenada com sucesso: ' + imagem.filename)

        try:
            #Pesquisar no Banco de Dados
            sql.execute(f"INSERT INTO questoes(titulo, enunciado, imagem, a, b, c, d, e) VALUES ('{titulo}','{enunciado}','{imagem}','{oa}','{ob}','{oc}','{od}','{oe}');")
            flash('Nova questão ' + '\n' + 'GRAVADA no banco de dados.!!!')    
            
        except Exception as e:
            print(e)
            flash('Campos Vazios Ou erro de digitação. Favor digite novamente.')
          
    return render_template('questoes.html')  

@app.route("/home/<user>", methods=('GET','POST'))
def home(user):    
     
    if 'user' in session:
        user = session['user']
        flash(f"Bem Vindo, {user}")
    try:
        #Pesquisar no Banco de Dados
        result = sql.execute("SELECT * FROM questoes;").scalar()
        if result is None:
            flash('Nenhuma Questão pendente !!!')
        else:
            flash(f"Resposta de {user} REGISTRADO com sucesso.!!")
                        
    except Exception as e:
        print(e)     

        

    return render_template('home.html', result=result)
    

@app.route("/gabarito", methods=('GET','POST'))
def gabarito():
    return render_template('gabarito.html')


@app.route("/sobre")
def sobre():
    return render_template('sobre.html')






if __name__=="main":
    app.run(host = '127.0.0.1', port = 4000)
