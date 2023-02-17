# importação de dependencias
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
import time
from datetime import date, timedelta
from petcenter import app, db
from models import tb_user,\
    tb_usertype,\
    tb_tipopet,\
    tb_tutor,\
    tb_pet
from helpers import \
    FormularPesquisa, \
    FormularioUsuarioTrocarSenha,\
    FormularioUsuario, \
    FormularioUsuarioVisualizar, \
    FormularioTipoUsuarioEdicao,\
    FormularioTipoUsuarioVisualizar,\
    FormularioTipoPetEdicao,\
    FormularioTipoPetVisualizar,\
    FormularioTutorEdicao,\
    FormularioTutorVisualizar,\
    FormularioPetEdicao,\
    FormularioPetVisualizar


# ITENS POR PÁGINA
from config import ROWS_PER_PAGE, CHAVE
from flask_bcrypt import generate_password_hash, Bcrypt, check_password_hash

import string
import random
import numbers

##################################################################################################################################
#GERAL
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: index
#FUNÇÃO: redirecionar para página principal
#PODE ACESSAR: todos os usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))        
    return render_template('index.html', titulo='Bem vindos')

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: logout
#FUNÇÃO: remover dados de sessão e deslogar ususários
#PODE ACESSAR: todos os usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso','success')
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: login
#FUNÇÃO: direcionar para formulário de login
#PODE ACESSAR: todos os usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/login')
def login():
    return render_template('login.html')

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: autenticar
#FUNÇÃO: autenticar usuário
#PODE ACESSAR: todos os usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/autenticar', methods = ['GET', 'POST'])
def autenticar():
    usuario = tb_user.query.filter_by(login_user=request.form['usuario']).first()
    senha = check_password_hash(usuario.password_user,request.form['senha'])
    if usuario:
        if senha:
            session['usuario_logado'] = usuario.login_user
            session['nomeusuario_logado'] = usuario.name_user
            session['tipousuario_logado'] = usuario.cod_usertype
            session['coduser_logado'] = usuario.cod_user
            flash(usuario.name_user + ' Usuário logado com sucesso','success')
            #return redirect('/')
            return redirect('/')
        else:
            flash('Verifique usuário e senha', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado com sucesso','success')
        return redirect(url_for('login'))

##################################################################################################################################
#USUARIOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: usuario
#FUNÇÃO: tela do sistema para mostrar os usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/usuario', methods=['POST','GET'])
def usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('usuario')))        
    form = FormularPesquisa()
    page = request.args.get('page', 1, type=int)
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data

    if pesquisa == "" or pesquisa == None:    
        usuarios = tb_user.query\
        .join(tb_usertype, tb_usertype.cod_usertype==tb_user.cod_usertype)\
        .add_columns(tb_user.login_user, tb_user.cod_user, tb_user.name_user, tb_user.status_user, tb_usertype.desc_usertype)\
        .order_by(tb_user.name_user)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
    else:
        usuarios = tb_user.query\
        .filter(tb_user.name_user.ilike(f'%{pesquisa}%'))\
        .join(tb_usertype, tb_usertype.cod_usertype==tb_user.cod_usertype)\
        .add_columns(tb_user.login_user, tb_user.cod_user, tb_user.name_user, tb_user.status_user, tb_usertype.desc_usertype)\
        .order_by(tb_user.name_user)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)


    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoUsuario
#FUNÇÃO: mostrar o formulário de cadastro de usuário
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/novoUsuario')
def novoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoUsuario')))     
    form = FormularioUsuario()
    return render_template('novoUsuario.html', titulo='Novo Usuário', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarUsuario
#FUNÇÃO: inserir informações do usuário no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarUsuario', methods=['POST',])
def criarUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('criarUsuario')))      
    form = FormularioUsuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('novoUsuario'))
    nome  = form.nome.data
    status = form.status.data
    login = form.login.data
    tipousuario = form.tipousuario.data
    email = form.email.data
    #criptografar senha
    senha = generate_password_hash("teste@12345").decode('utf-8')
    usuario = tb_user.query.filter_by(name_user=nome).first()
    if usuario:
        flash ('Usuário já existe','danger')
        return redirect(url_for('index')) 
    novoUsuario = tb_user(name_user=nome, status_user=status, login_user=login, cod_usertype=tipousuario, password_user=senha, email_user=email)
    db.session.add(novoUsuario)
    db.session.commit()
    flash('Usuário criado com sucesso','success')
    return redirect(url_for('usuario'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarUsuarioexterno - NÃO DISPONIVEL NESTA VERSAL
#FUNÇÃO: inserir informações do usuário no banco de dados realizam cadastro pela área externa
#PODE ACESSAR: novos usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/criarUsuarioexterno', methods=['POST',])
def criarUsuarioexterno():    
    nome  = request.form['nome']
    status = 0
    email = request.form['email']
    localarroba = email.find("@")
    login = email[0:localarroba]
    tipousuario = 2
    #criptografar senha
    senha = generate_password_hash(request.form['senha']).decode('utf-8')
    usuario = tb_user.query.filter_by(name_user=nome).first()
    if usuario:
        flash ('Usuário já existe','danger')
        return redirect(url_for('login')) 
    novoUsuario = tb_user(name_user=nome, status_user=status, login_user=login, cod_usertype=tipousuario, password_user=senha, email_user=email)
    db.session.add(novoUsuario)
    db.session.commit()
    flash('Usuário criado com sucesso, favor logar com ele','success')
    return redirect(url_for('login'))  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarUsuario
#FUNÇÃO: mostrar formulário de visualização dos usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarUsuario/<int:id>')
def visualizarUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))    
    usuario = tb_user.query.filter_by(cod_user=id).first()
    form = FormularioUsuarioVisualizar()
    form.nome.data = usuario.name_user
    form.status.data = usuario.status_user
    form.login.data = usuario.login_user
    form.tipousuario.data = usuario.cod_usertype
    form.email.data = usuario.email_user
    return render_template('visualizarUsuario.html', titulo='Visualizar Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarUsuario
#FUNÇÃO: mostrar formulário de edição dos usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/editarUsuario/<int:id>')
def editarUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarUsuario/<int:id>')))  
    usuario = tb_user.query.filter_by(cod_user=id).first()
    form = FormularioUsuario()
    form.nome.data = usuario.name_user
    form.status.data = usuario.status_user
    form.login.data = usuario.login_user
    form.tipousuario.data = usuario.cod_usertype
    form.email.data = usuario.email_user
    return render_template('editarUsuario.html', titulo='Editar Usuário', id=id, form=form)    
       
#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarUsuario
#FUNÇÃO: alterar as informações dos usuários no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarUsuario', methods=['POST',])
def atualizarUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarUsuario')))          
    form = FormularioUsuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('atualizarUsuario'))
    id = request.form['id']
    usuario = tb_user.query.filter_by(cod_user=request.form['id']).first()
    usuario.name_user = form.nome.data
    usuario.status_user = form.status.data
    usuario.login_user = form.login.data
    usuario.cod_uertype = form.tipousuario.data
    db.session.add(usuario)
    db.session.commit()
    flash('Usuário alterado com sucesso','success')
    return redirect(url_for('visualizarUsuario', id=request.form['id']))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarSenhaUsuario
#FUNÇÃO: formulário para edição da tela do usuário
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarSenhaUsuario/')
def editarSenhaUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))    
    form = FormularioUsuarioTrocarSenha()
    return render_template('trocarsenha.html', titulo='Trocar Senha', id=id, form=form)  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: trocarSenhaUsuario
#FUNÇÃO: alteração da senha do usuário no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/trocarSenhaUsuario', methods=['POST',])
def trocarSenhaUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarUsuario')))          
    form = FormularioUsuarioTrocarSenha(request.form)
    if form.validate_on_submit():
        id = session['coduser_logado']
        usuario = tb_user.query.filter_by(cod_user=id).first()
        if form.senhaatual.data != usuario.password_user:
            flash('senha atual incorreta','danger')
            return redirect(url_for('editarSenhaUsuario'))

        if form.senhaatual.data != usuario.password_user:
            flash('senha atual incorreta','danger')
            return redirect(url_for('editarSenhaUsuario')) 

        if form.novasenha1.data != form.novasenha2.data:
            flash('novas senhas não coincidem','danger')
            return redirect(url_for('editarSenhaUsuario')) 
        usuario.password_user = generate_password_hash(form.novasenha1.data).decode('utf-8')
        db.session.add(usuario)
        db.session.commit()
        flash('senha alterada com sucesso!','success')
    else:
        flash('senha não alterada!','danger')
    return redirect(url_for('editarSenhaUsuario')) 

##################################################################################################################################
#TIPO DE USUARIOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: tipousuario
#FUNÇÃO: tela do sistema para mostrar os tipos de usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/tipousuario', methods=['POST','GET'])
def tipousuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('tipousuario')))         
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        tiposusuario = tb_usertype.query.order_by(tb_usertype.desc_usertype)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        tiposusuario = tb_usertype.query.order_by(tb_usertype.desc_usertype)\
        .filter(tb_usertype.desc_usertype.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('tipousuarios.html', titulo='Tipo Usuário', tiposusuario=tiposusuario, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoUsuario
#FUNÇÃO: mostrar o formulário de cadastro de tipo de usuário
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTipoUsuario')
def novoTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTipoUsuario'))) 
    form = FormularioTipoUsuarioEdicao()
    return render_template('novoTipoUsuario.html', titulo='Novo Tipo Usuário', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTipoUsuario
#FUNÇÃO: inserir informações do tipo de usuário no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTipoUsuario', methods=['POST',])
def criarTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTipoUsuario')))     
    form = FormularioTipoUsuarioEdicao(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarTipoUsuario'))
    desc  = form.descricao.data
    status = form.status.data
    tipousuario = tb_usertype.query.filter_by(desc_usertype=desc).first()
    if tipousuario:
        flash ('Tipo Usuário já existe','danger')
        return redirect(url_for('tipousuario')) 
    novoTipoUsuario = tb_usertype(desc_usertype=desc, status_usertype=status)
    flash('Tipo de usuário criado com sucesso!','success')
    db.session.add(novoTipoUsuario)
    db.session.commit()
    return redirect(url_for('tipousuario'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTipoUsuario
#FUNÇÃO: mostrar formulário de visualização dos tipos de usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTipoUsuario/<int:id>')
def visualizarTipoUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTipoUsuario')))  
    tipousuario = tb_usertype.query.filter_by(cod_usertype=id).first()
    form = FormularioTipoUsuarioVisualizar()
    form.descricao.data = tipousuario.desc_usertype
    form.status.data = tipousuario.status_usertype
    return render_template('visualizarTipoUsuario.html', titulo='Visualizar Tipo Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTipoUsuario
##FUNÇÃO: mostrar formulário de edição dos tipos de usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTipoUsuario/<int:id>')
def editarTipoUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTipoUsuario')))  
    tipousuario = tb_usertype.query.filter_by(cod_usertype=id).first()
    form = FormularioTipoUsuarioEdicao()
    form.descricao.data = tipousuario.desc_usertype
    form.status.data = tipousuario.status_usertype
    return render_template('editarTipoUsuario.html', titulo='Editar Tipo Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTipoUsuario
#FUNÇÃO: alterar as informações dos tipos de usuários no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTipoUsuario', methods=['POST',])
def atualizarTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTipoUsuario')))      
    form = FormularioTipoUsuarioEdicao(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tipousuario = tb_usertype.query.filter_by(cod_usertype=request.form['id']).first()
        tipousuario.desc_usertype = form.descricao.data
        tipousuario.status_usertype = form.status.data
        db.session.add(tipousuario)
        db.session.commit()
        flash('Tipo de usuário atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTipoUsuario', id=request.form['id']))    

##################################################################################################################################
#TIPO DE PET
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: tipopet
#FUNÇÃO: tela do sistema para mostrar os tipos de pet cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/tipopet', methods=['POST','GET'])
def tipopet():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('tipopet')))         
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        tipospet = tb_tipopet.query.order_by(tb_tipopet.desc_tipopet)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        tipospet = tb_tipopet.query.order_by(tb_tipopet.desc_tipopet)\
        .filter(tipopet.desc_tipopet.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('tipopet.html', titulo='Tipo Pet', tipospet=tipospet, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoPet
#FUNÇÃO: mostrar o formulário de cadastro de tipo de pet
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTipoPet')
def novoTipoPet():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTipoPet'))) 
    form = FormularioTipoPetEdicao()
    return render_template('novoTipoPet.html', titulo='Novo Tipo Pet', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTipoPet
#FUNÇÃO: inserir informações do tipo de pet no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTipoPet', methods=['POST',])
def criarTipoPet():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTipoPet')))     
    form = FormularioTipoPetEdicao(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarTipoPet'))
    desc  = form.descricao.data
    status = form.status.data
    tipopet = tb_tipopet.query.filter_by(desc_tipopet=desc).first()
    if tipopet:
        flash ('Tipo Pet já existe','danger')
        return redirect(url_for('tipopet')) 
    novoTipoPet = tb_tipopet(desc_tipopet=desc, status_tipopet=status)
    flash('Tipo de pet criado com sucesso!','success')
    db.session.add(novoTipoPet)
    db.session.commit()
    return redirect(url_for('tipopet'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTipoPet
#FUNÇÃO: mostrar formulário de visualização dos tipos de pet cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTipoPet/<int:id>')
def visualizarTipoPet(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTipoPet')))  
    tipopet = tb_tipopet.query.filter_by(cod_tipopet=id).first()
    form = FormularioTipoPetVisualizar()
    form.descricao.data = tipopet.desc_tipopet
    form.status.data = tipopet.status_tipopet
    return render_template('visualizarTipoPet.html', titulo='Visualizar Tipo Pet', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTipoPet
##FUNÇÃO: mostrar formulário de edição dos tipos de usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTipoPet/<int:id>')
def editarTipoPet(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTipoPet')))  
    tipopet= tb_tipopet.query.filter_by(cod_tipopet=id).first()
    form = FormularioTipoPetEdicao()
    form.descricao.data = tipopet.desc_tipopet
    form.status.data = tipopet.status_tipopet
    return render_template('editarTipoPet.html', titulo='Editar Tipo Pet', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTipoPet
#FUNÇÃO: alterar as informações dos tipos de pet no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTipoPet', methods=['POST',])
def atualizarTipoPet():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTipoPet')))      
    form = FormularioTipoPetEdicao(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tipopet = tb_tipopet.query.filter_by(cod_tipopet=request.form['id']).first()
        tipopet.desc_tipopet = form.descricao.data
        tipopet.status_tipopet = form.status.data
        db.session.add(tipopet)
        db.session.commit()
        flash('Tipo de pet atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTipoPet', id=request.form['id']))    



##################################################################################################################################
#TUTOR
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: tutor
#FUNÇÃO: tela do sistema para mostrar os tutores cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/tutor', methods=['POST','GET'])
def tutor():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('tutor')))         
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        tutores = tb_tutor.query.order_by(tb_tutor.nome_tutor)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        tutores = tb_tutor.query.order_by(tb_tutor.nome_tutor)\
        .filter(tb_tutor.nome_tutor.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('tutores.html', titulo='Tutor', tutores=tutores, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTutor
#FUNÇÃO: mostrar o formulário de cadastro de tutor
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTutor')
def novoTutor():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTutor'))) 
    form = FormularioTutorEdicao()
    return render_template('novoTutor.html', titulo='Novo Tutor', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTutor
#FUNÇÃO: inserir informações do tutorno banco de dados
#PODE ACESSAR: todos
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTutor', methods=['POST',])
def criarTutor():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTutor')))     
    form = FormularioTutorEdicao(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarTutor'))
    nome  = form.nome.data
    endereco  = form.endereco.data
    telefone = form.telefone.data
    observacoes = form.observacoes.data
    status = form.status.data
    tutor = tb_tutor.query.filter_by(nome_tutor=nome).first()
    if tutor:
        flash ('Tutor já existe','danger')
        return redirect(url_for('tutor')) 
    novoTutor = tb_tutor(nome_tutor=nome, status_tutor=status,end_tutor=endereco, obs_tutor=observacoes,fone_tutor=telefone)
    flash('Tutor criado com sucesso!','success')
    db.session.add(novoTutor)
    db.session.commit()
    return redirect(url_for('tutor'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTutor
#FUNÇÃO: mostrar formulário de visualização dos tutores cadastrados
#PODE ACESSAR: todos
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTutor/<int:id>')
def visualizarTutor(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTutor')))  
    tutor = tb_tutor.query.filter_by(cod_tutor=id).first()
    form = FormularioTutorVisualizar()
    form.nome.data = tutor.nome_tutor
    form.endereco.data = tutor.end_tutor
    form.telefone.data = tutor.fone_tutor
    form.observacoes.data = tutor.obs_tutor
    form.status.data = tutor.status_tutor
    return render_template('visualizarTutor.html', titulo='Visualizar Tutor', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTutor
##FUNÇÃO: mostrar formulário de edição dos tutores cadastrados
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTutor/<int:id>')
def editarTutor(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTutor')))  
    tutor= tb_tutor.query.filter_by(cod_tutor=id).first()
    form = FormularioTutorEdicao()
    form.nome.data = tutor.nome_tutor
    form.endereco.data = tutor.end_tutor
    form.telefone.data = tutor.fone_tutor
    form.observacoes.data = tutor.obs_tutor
    form.status.data = tutor.status_tutor
    return render_template('editarTutor.html', titulo='Editar Tutor', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTutor
#FUNÇÃO: alterar as informações dos tutores no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTutor', methods=['POST',])
def atualizarTutor():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTutor')))      
    form = FormularioTutorEdicao(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tutor = tb_tutor.query.filter_by(cod_tutor=request.form['id']).first()
        tutor.nome_tutor = form.nome.data
        tutor.end_tutor = form.endereco.data
        tutor.fone_tutor = form.telefone.data
        tutor.obs_tutor = form.observacoes.data
        tutor.status_tutor = form.status.data
        db.session.add(tutor)
        db.session.commit()
        flash('Tutor atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTutor', id=request.form['id']))   

##################################################################################################################################
#PET
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: pet
#FUNÇÃO: tela do sistema para mostrar os pets cadastrados
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/pet', methods=['POST','GET'])
def pet():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('pet')))         
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:          
        pets = tb_pet.query\
        .join(tb_tutor, tb_tutor.cod_tutor==tb_pet.cod_tutor)\
        .join(tb_tipopet, tb_tipopet.cod_tipopet==tb_pet.cod_tipopet)\
        .add_columns(tb_pet.nome_pet, tb_tutor.nome_tutor, tb_pet.cod_pet, tb_tipopet.desc_tipopet, tb_pet.raca_pet, tb_pet.status_pet)\
        .order_by(tb_pet.nome_pet)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        pets = tb_pet.query\
        .join(tb_tutor, tb_tutor.cod_tutor==tb_pet.cod_tutor)\
        .join(tb_tipopet, tb_tipopet.cod_tipopet==tb_pet.cod_tipopet)\
        .filter(tb_pet.nome_pet.ilike(f'%{pesquisa}%'))\
        .add_columns(tb_pet.nome_pet, tb_tutor.nome_tutor, tb_pet.cod_pet, tb_tipopet.desc_tipopet, tb_pet.raca_pet, tb_pet.status_pet)\
        .order_by(tb_pet.nome_pet)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)     
    return render_template('pets.html', titulo='Pets', pets=pets, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoPet
#FUNÇÃO: mostrar o formulário de cadastro de pet
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoPet')
def novoPet():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoPet'))) 
    form = FormularioPetEdicao()
    return render_template('novoPet.html', titulo='Novo Pet', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarPet
#FUNÇÃO: inserir informações do pet no banco de dados
#PODE ACESSAR: todos
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarPet', methods=['POST',])
def criarPet():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarPet')))     
    form = FormularioPetEdicao(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarPet'))
    nome  = form.nome.data
    datanacimento  = form.datanascimento.data
    raca = form.raca.data
    observacoes = form.observacoes.data
    status = form.status.data
    tipo = form.tipopet.data
    tutor = form.tutor.data
    pet = tb_pet.query.filter_by(nome_pet=nome).first()
    if pet:
        flash ('Pet já existe','danger')
        return redirect(url_for('pet')) 
    novoPet = tb_pet(nome_pet=nome, status_pet=status,raca_pet=raca, obs_pet=observacoes,cod_tipopet=tipo,datanasc_pet=datanacimento,cod_tutor=tutor)
    flash('Pet criado com sucesso!','success')
    db.session.add(novoPet)
    db.session.commit()
    return redirect(url_for('pet'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarPet
#FUNÇÃO: mostrar formulário de visualização dos tutores cadastrados
#PODE ACESSAR: todos
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarPet/<int:id>')
def visualizarPet(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarPet')))  
    pet = tb_pet.query.filter_by(cod_pet=id).first()
    form = FormularioPetVisualizar()
    form.nome.data = pet.nome_pet
    form.raca.data = pet.raca_pet
    form.tipopet.data = pet.cod_tipopet
    form.observacoes.data = pet.obs_pet
    form.datanascimento.data = pet.datanasc_pet
    form.status.data = pet.status_pet
    form.tutor.data = pet.cod_tutor
    return render_template('visualizarPet.html', titulo='Visualizar Pet', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarPet
##FUNÇÃO: mostrar formulário de edição dos pets cadastrados
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarPet/<int:id>')
def editarPet(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarPet')))  
    pet = tb_pet.query.filter_by(cod_pet=id).first()
    form = FormularioPetEdicao()
    form.nome.data = pet.nome_pet
    form.raca.data = pet.raca_pet
    form.tipopet.data = pet.cod_tipopet
    form.observacoes.data = pet.obs_pet
    form.datanascimento.data = pet.datanasc_pet
    form.status.data = pet.status_pet
    form.tutor.data = pet.cod_tutor
    return render_template('editarPet.html', titulo='Editar Pet', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarPet
#FUNÇÃO: alterar as informações dos pets no banco de dados
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarPet', methods=['POST',])
def atualizarPet():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarPet')))      
    form = FormularioPetEdicao(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        pet = tb_pet.query.filter_by(cod_pet=request.form['id']).first()
        pet.nome_pet = form.nome.data
        pet.raca_pet = form.raca.data
        pet.cod_tipopet = form.tipopet.data
        pet.cod_tutor = form.tutor.data
        pet.obs_pet = form.observacoes.data
        pet.status_pet = form.status.data
        pet.datanasc_pet = form.datanascimento.data
        db.session.add(pet)
        db.session.commit()
        flash('Pet atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarPet', id=request.form['id']))   