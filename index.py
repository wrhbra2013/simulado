# Módulos
from flask import Flask, render_template, request, redirect,url_for, flash,session
from init_db import conn, cur
from werkzeug.utils import secure_filename
import os

#Pastas e extensões
pasta_upload = 'static/uploads'
extensao_permitida = set(['jpeg','jpg','png','gif'])

def arq_permitido(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in extensao_permitida
    
def get_questoes(indice):
    cur.execute(f"SELECT * FROM questoes where id = '{indice}';")
    indice = cur.fetchone()
    return indice



#Cofigurações do Flask app
app = Flask(__name__)
app.secret_key = 'simulado'
app.permanent_session_lifetime = minutes=5
app.config['pasta_upload'] = pasta_upload
app.config['max_content_length'] = 16 * 1024 * 1024

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
            cur.execute(f"SELECT inst, nome, serie FROM estudante where inst='{escola}' and nome='{user}' and serie='{ano}';")
            pesquisa = cur.fetchall()
            
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
            cur.execute(f"SELECT inst, nome, serie FROM estudante where inst='{escola}' and nome='{user}' and serie='{ano}';")
            pesquisa =  cur.fetchall()        

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
            cur.execute(f"INSERT INTO estudante(inst, nome, serie) VALUES ('{escola}','{user}','{ano}');")
            conn.commit()
            flash(f"Usuario {user} REGISTRADO com sucesso.!!")
            
        except Exception as e:
            print(e)
            flash('Campos Vazios Ou erro de digitação. Favor digite novamente.')
          
    return render_template('cadastro.html')

@app.route("/questoes",methods=('GET','POST'))
def questoes():
     if request.method == 'POST':
        #recebe dados
        titulo = request.form['titulo']
        enunciado = request.form['enunciado']
        imagem = request.files['imagem']
        oa = request.form['a']
        ob = request.form['b']
        oc = request.form['c']
        od = request.form['d']
        oe = request.form['e']
        value = request.form['valor']    
        
    
        #Armazenando imagens.
        if imagem.filename == '':
             filename = ''
             flash('Questão sem Imagem.')
             cur.execute(f"INSERT INTO questoes(titulo, enunciado, imagem, a, b, c, d, e,valor) VALUES ('{titulo}','{enunciado}','{filename}','{oa}','{ob}','{oc}','{od}','{oe}','{value}');")
             conn.commit()
             flash('Nova questão GRAVADA no banco de dados.!!!')
             return redirect(request.url)
        
        if imagem and arq_permitido(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['pasta_upload'],filename))            
            flash('Imagem Armazenada com sucesso')
            
            #Inserir imagem no Banco de Dados
            cur.execute(f"INSERT INTO questoes(titulo, enunciado, imagem, a, b, c, d, e,valor) VALUES ('{titulo}','{enunciado}','{filename}','{oa}','{ob}','{oc}','{od}','{oe}','{value}');")
            conn.commit()
            flash('Nova questão GRAVADA no banco de dados.!!!')            
            
            return render_template('questoes.html',filename=filename)      
        
        
        else:
            flash('As imagens permitidas são: jpeg, jpg, png e gif')
            return redirect(request.url)        
    
     return render_template('questoes.html')  
        
            
     
    

@app.route('/display/<filename>')
def display(filename):     
     return redirect(url_for('static', filename='uploads/' + filename),code=301)
        
    
@app.route("/home/<user>", methods=('GET','POST'))
def home(user):    
    if request.method == 'GET':                 
        if 'user' in session:
            user = session['user']
            
        #Buscar questões     
        cur.execute("SELECT id FROM questoes where id = id;")              
        indice = cur.fetchall()               
              
        if indice is None:
            flash('Nenhuma Questão pendente !!!')
        else:
            flash("As séries  estão carregadas.!!")        
        
                     
    if request.method == 'POST': 
        btn = request.form['btn']  
        return redirect(url_for('q',btn=btn))            
          
    return render_template('home.html',indice=indice,user=user)

@app.route("/q/<btn>",methods=['GET','POST'])
def q(btn):
    if request.method == 'GET':
        cur.execute(f"SELECT * FROM questoes where id = '{btn}';")
        result = cur.fetchmany()
    if request.method == 'POST':
        input = request.form['questao']
        return redirect(url_for('gabarito',input=input))
    return render_template('q.html',result=result,btn=btn)

              
    

@app.route("/gabarito/<input>")
def gabarito(input):
    
    cur.execute('SELECT id, enunciado, valor from questoes;')
    res = cur.fetchmany()
    valor = [last['valor'] for last in res]
    valor 
    print('valor==',valor)
    print('input==',input)
    cur.execute("SELECT id FROM questoes where id = id;")
    indice = cur.fetchmany()
    if input and valor == True:
        flash('Resposta CERTA!!!')
    else:
        flash('Resposta ERRADA!!!')                
    return render_template('gabarito.html',res=res,indice=indice,input=input)


@app.route("/sobre")
def sobre():
    return render_template('sobre.html')

@app.route("/delete/<indice>",methods=['post'])
def delete(indice): 
    cur.execute(f"DELETE FROM questoes where id ='{indice}'")
    conn.commit() 
    flash(f"Questão'{indice}'apagada.") 
    return url_for('delete',indice=indice)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__=='__main__':
    app.run(debug=True)
