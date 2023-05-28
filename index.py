# Módulos
from flask import Flask, render_template, request, redirect,url_for, flash,session
from init_db import conn, cur
from werkzeug.utils import secure_filename
import os

#Pastas e extensões
pasta_upload = 'static/uploads'
extensao_permitida = set(['jpeg','jpg','png','gif'])

#Filtro de imagens
def arq_permitido(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in extensao_permitida
    

#Funções de apoio
#Login
def get_login(escola,user,ano):    
    cur.execute(f"SELECT * from estudante where inst LIKE '%{escola}%' and nome LIKE '%{user}%' and serie = '{ano}';")       
    a = cur.fetchall()
    b = len(a)    
    if b == 0:
        flash('Usuario NÃO Encontrado. Digite novamente! Ou Cadastre-se!')
        return render_template('index.html')
    else:
        #Sessão do usuário
        session['usuario'] = user
        session.permanent = True
        return redirect(url_for('home',user=user))
        

    
                
    
    

#Lista de questoes
def get_all_questoes():
    cur.execute('SELECT id FROM questoes;')
    all = cur.fetchall()
    return all

#identificar aluno por nome
def get_aluno(name):
    cur.execute(f"SELECT inst, nome from estudante where nome LIKE '{name}%';")
    name = cur.fetchall()
    return name



#Busca de  questões por questoes
def get_questoes(qnumero):
    cur.execute(f"SELECT * from questoes where id = '{qnumero}';")
    qnumero = cur.fetchmany()
    return qnumero


#Retorno de respostas do aluno
def get_respostas(qaluno):
    cur.execute(f"SELECT * FROM resultados where estudante_nome = '{qaluno}';")
    qaluno = cur.fetchall()
    return qaluno

#Apuração de notas
def get_notas(quem):
    cur.execute(f"SELECT SUM(nota) FROM resultados where estudante_nome = '{quem}' ;")
    quem = cur.fetchone()
    return quem



#Funções insert into
#Cadastro de alunos.

def post_aluno(escola,user,ano):
    cur.execute(f"INSERT INTO estudante(inst, nome, serie) VALUES ('{escola}','{user}','{ano}');")
    post_aluno = conn.commit()
    return post_aluno

#Registro de respostas
def post_resposta(escola, nome, id, enunciado, valor, input, pontos):    
    cur.execute(f"INSERT INTO resultados(estudante_escola, estudante_nome, questao_id, questao_enunciado, questao_valor, alternativa, nota)VALUES ('{escola}','{nome}','{id}', '{enunciado}','{valor}','{input}','{pontos}');")
    post_resposta =  conn.commit()  
    return post_resposta

#Registro de questoes.
def post_questoes(competencia, titulo, enunciado, filename, oa, ob, oc, od, value):
    cur.execute(f"INSERT INTO questoes(competencia, titulo, enunciado, imagem, a, b, c, d, valor) VALUES ('{competencia}','{titulo}','{enunciado}','{filename}','{oa}','{ob}','{oc}','{od}','{value}');")
    post_questoes =  conn.commit()
    return post_questoes

#Registro de comentarios
def post_comentarios(nom,contat,assu,coment):
    cur.execute(f"INSERT INTO contato (nome,contato,assunto,comentario) VALUES ('{nom}','{contat}','{assu}','{coment}') ;")
    post_comentarios = conn.commit()
    return post_comentarios

    

#Cofigurações do Flask app
app = Flask(__name__)
app.secret_key = 'simulado'
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
        autentica = get_login(escola,user,ano)
            
                 
        return autentica
    return render_template('index.html')

#Página de Reload para login
@app.route("/index",methods=('GET','POST'))
def index():
    if request.method == 'GET':
        flash('Entre com as suas credenciais.')
    if request.method =='POST':     
        #Recebe dados
        escola = request.form['inst']
        user = request.form['nome']
        ano = request.form['serie']
        autentica = get_login(escola,user,ano)
              
        return autentica
        
    return render_template('index.html')
    
      
#Pagina de cadastro
@app.route("/cadastro",methods=('GET','POST'))
def cadastro():
    if request.method =='POST':                       

        #Recebe dados
        escola = request.form['inst']
        user = request.form['nome']
        ano = request.form['serie']
        
        #Copia no Banco de Dados
        post_aluno(escola,user,ano)
        flash(f"Usuario {user} REGISTRADO com sucesso.!!")
          
        
          
    return render_template('cadastro.html')

#Página de cadastro de questões
@app.route("/questoes",methods=('GET','POST'))
def questoes():  
    
    if request.method == 'POST':
        
        #recebe dados
        competencia = request.form['competencia']
        titulo = request.form['titulo']
        enunciado = request.form['enunciado']
        imagem = request.files['imagem']
        oa = request.form['a']
        ob = request.form['b']
        oc = request.form['c']
        od = request.form['d']
        value = request.form['valor']    
        
    
        #Armazenando imagens.
        if imagem.filename == '':
             filename = ''             
             flash('Questão sem Imagem.')
             post_questoes(competencia, titulo, enunciado, filename, oa, ob, oc, od, value)
             flash('Nova questão GRAVADA no banco de dados.!!!')
             return redirect(url_for('questoes',filename=filename))
        
        if imagem and arq_permitido(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['pasta_upload'],filename))            
            flash('Imagem Armazenada com sucesso')
            
            #Inserir imagem no Banco de Dados
            post_questoes(competencia, titulo, enunciado, filename, oa, ob, oc, od, value)
            flash('Nova questão GRAVADA no banco de dados.!!!')          
            
            return render_template('questoes.html',filename=filename)      
        
        
        else:
            flash('As imagens permitidas são: jpeg, jpg, png e gif')
            return redirect(request.url)        
    
    return render_template('questoes.html')        
     
    
#Rota especifica para imagens.
@app.route('/display/<filename>')
def display(filename):     
     return redirect(url_for('static', filename='uploads/' + filename),code=301)
 
#Aprresentação das questões       
@app.route("/home/<user>", methods=('GET','POST'))
def home(user):    
    #Buscar questões     
    indice = get_all_questoes()    
    if indice is None:
        flash('Nenhuma Questão pendente !!!')  
                     
    if request.method == 'POST':         
        btn = request.form['btn']       
        
        return redirect(url_for('q',btn=btn,user=user))     
    return render_template('home.html',indice=indice,user=user)

#Página de questões
@app.route("/q/<user>/<btn>",methods=['GET','POST'])
def q(user,btn):
    #Encontrar aluno
    aluno = get_aluno(user)
        
    #Busca por questão
    result = get_questoes(btn)
    
    
    #Quantidade de questoes     
    indice = get_all_questoes()                   
           
                              
    if request.method == 'POST': 
        try:              
            #identificação do aluno
            escola = request.form['estudante_escola']
            nome = request.form['estudante_nome']

            #identificação da questão.
            id = request.form['questao_id']
            enunciado = request.form['questao_enunciado']
            valor = request.form['questao_valor']

            #Alternativa Marcada.
            input = request.form['input_estudante'] 

            #Filtro da resposta certa.           
            resposta = input in valor
            #Apuração instantnea
            if resposta == True:
                #resp = 'true'
                nota = 1 
            else:
                #resp = 'false'
                nota = 0
            pontos = nota
                
            post_resposta(escola, nome, id, enunciado, valor, input, pontos)
        except Exception:
            flash('Falta ASSINALAR alternativa!!')
            
            
        return redirect(url_for('gabarito',user=user))   
    return render_template('q.html',btn=btn,aluno=aluno,indice=indice,result=result)

              
    
#Pagina de Resposta
@app.route("/gabarito/<user>",methods=['GET','POST'])
def gabarito(user): 
    res = get_respostas(user)  
            
      
    if request.method == 'POST': 
        #Notas Por aluno 
        s = get_notas(user)
        #Filtro do dicionário
        for i in s:
            soma = i    
             
        
        return redirect(url_for('notas',user=user,soma=soma))                   
    return render_template('gabarito.html',res=res,user=user)

#Pǵina de Apuração de notas
@app.route("/notas/<user>/<soma>")
def notas(user,soma):
    #Quantidade de questões
    q = get_all_questoes()
   #filtro do dicionário
    quant = len(q)
    #
    resp = get_respostas(user)         
    return render_template('notas.html',user=user,soma=soma,quant=quant,resp=resp)

#Página de Suporte e referência.
@app.route("/sobre",methods=['GET','POST'])
def sobre():
    if request.method == 'POST':
        nom = request.form['nome']
        contat = request.form['contato']
        assu = request.form['assunto']
        coment = request.form['comentario']
        post_comentarios(nom,contat,assu,coment)
        
        return redirect(url_for('sobre'))    
    return render_template('sobre.html')


#Rota de Logout
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('usuario', None)
    return redirect(url_for('index'))

#Rota de erro de página e Recepção.
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html',error=error), 404


if __name__=='__main__':
    app.run(debug=True)
