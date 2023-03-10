#importações
import os
from petcenter import app, db
from models import tb_user, tb_usertype, tb_tipopet, tb_pet, tb_tutor
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, SubmitField,IntegerField, SelectField,PasswordField,DateField,EmailField,BooleanField,RadioField, TextAreaField, TimeField, TelField, DateTimeLocalField

##################################################################################################################################
#PESQUISA
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pesquisa (geral)
#TIPO: edição
#TABELA: nenhuma
#---------------------------------------------------------------------------------------------------------------------------------
class FormularPesquisa(FlaskForm):
    pesquisa = StringField('Pesquisa:', [validators.Length(min=1, max=50)],render_kw={"placeholder": "digite sua pesquisa"} )
    pesquisa_responsiva = StringField('Pesquisa:', [validators.Length(min=1, max=50)],render_kw={"placeholder": "digite sua pesquisa"} )
    salvar = SubmitField('Pesquisar')

##################################################################################################################################
#USUÁRIO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: usuários
#TIPO: edição
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioUsuario(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o nome do usuário"})
    status = SelectField('Situação:', coerce=int, choices=[(0,"Ativo"),(1,"Inativo")])
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o login do usuário"})    
    tipousuario = SelectField('Situação:', coerce=int,  choices=[(g.cod_usertype, g.desc_usertype) for g in tb_usertype.query.order_by('desc_usertype')])
    email = EmailField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o email do usuário"})
    salvar = SubmitField('Salvar')


#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: usuários
#TIPO: visualização
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioUsuarioVisualizar(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0,"Ativo"),(1,"Inativo")], render_kw={'readonly': True})
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    tipousuario = SelectField('Tipo:', coerce=int, choices=[(g.cod_usertype, g.desc_usertype) for g in tb_usertype.query.order_by('desc_usertype')], render_kw={'readonly': True})
    email = EmailField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    salvar = SubmitField('Editar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: trocar senha do usuário
#TIPO: edição
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioUsuarioTrocarSenha(FlaskForm):
    senhaatual = PasswordField('Senha Atual:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a senha atual"})
    novasenha1 = PasswordField('Nova Senha:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a nova senha"})
    novasenha2 = PasswordField('Confirme Nova Senha:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite novamente a senha"})
    salvar = SubmitField('Editar')  

##################################################################################################################################
#TIPO DE USUÁRIO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de usuário
#TIPO: edição
#TABELA: tb_usertype
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioTipoUsuarioEdicao(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do tipo de usuário"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de usuário
#TIPO: visualização
#TABELA: tb_usertype
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioTipoUsuarioVisualizar(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    

##################################################################################################################################
#TIPO PET
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de pet
#TIPO: edição
#TABELA: tb_tipopet
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioTipoPetEdicao(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do tipo de pet"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de pet
#TIPO: visualização
#TABELA: tb_tipopet
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioTipoPetVisualizar(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    


##################################################################################################################################
#TUTOR
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tutor
#TIPO: edição
#TABELA: tb_tutor
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioTutorEdicao(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome do tutor"})
    endereco = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=90)], render_kw={"placeholder": "digite o nome do tutor"})
    telefone = StringField('Telefone:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o telefone do tutor"})
    observacoes = TextAreaField('Observações:', [validators.DataRequired(), validators.Length(min=1, max=500)],render_kw={"placeholder": "digite as observações do tutor"})  
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    


#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tutor
#TIPO: visualização
#TABELA: tb_tutor
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioTutorVisualizar(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    endereco = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=90)], render_kw={'readonly': True})
    telefone = StringField('Telefone:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    observacoes = TextAreaField('Observações:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    

##################################################################################################################################
#PET
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pet
#TIPO: edição
#TABELA: tb_pet
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioPetEdicao(FlaskForm):
    tipopet = SelectField('Tipo:', coerce=int,  choices=[(g.cod_tipopet, g.desc_tipopet) for g in tb_tipopet.query.order_by('desc_tipopet')])
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome do pet"})
    datanascimento = DateField('Data Nascimento:', [validators.DataRequired()], render_kw={"placeholder": "digite a data de nascimento"})
    raca = StringField('Raça:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o telefone do tutor"})
    observacoes = TextAreaField('Observações:', [validators.Length(min=1, max=500)],render_kw={"placeholder": "digite as observações do tutor"})  
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    tutor = SelectField('Tutor:', coerce=int,  choices=[(g.cod_tutor, g.nome_tutor) for g in tb_tutor.query.order_by('nome_tutor')])
    salvar = SubmitField('Salvar')    


#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pet
#TIPO: visualização
#TABELA: tb_pet
#---------------------------------------------------------------------------------------------------------------------------------
class FormularioPetVisualizar(FlaskForm):
    tipopet = SelectField('Tipo:', coerce=int, choices=[(g.cod_tipopet, g.desc_tipopet) for g in tb_tipopet.query.order_by('desc_tipopet')], render_kw={'readonly': True})
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    datanascimento = DateField('Data Nascimento:', [validators.DataRequired()], render_kw={'readonly': True})
    raca = StringField('Raça:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    observacoes = TextAreaField('Observações:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    tutor = SelectField('Tutor:', coerce=int,  choices=[(g.cod_tutor, g.nome_tutor) for g in tb_tutor.query.order_by('nome_tutor')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    

##################################################################################################################################
#CONSULTA
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: consulta
#TIPO: visualização
#TABELA: tb_consulta
#--------------------------------------------------------------------------------------------------------------------------------- 
class FormularioConsultaVisualizar(FlaskForm):
    horario = StringField('Horário:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={'readonly': True})
    pet = SelectField('Pet:', coerce=int, choices=[(g.cod_pet, g.nome_pet) for g in tb_pet.query.order_by('nome_pet')], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0,"Agendada"),(1,"Realizada"),(2,"Cancelada")], render_kw={'readonly': True})
    observacoes = TextAreaField('Observações:', [validators.Length(min=1, max=50)], render_kw={'readonly': True})    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: consulta
#TIPO: edição
#TABELA: tb_consulta
#--------------------------------------------------------------------------------------------------------------------------------- 
class FormularioConsultaEdicao(FlaskForm):
    horario = DateTimeLocalField('Horário:', [validators.DataRequired()], format='%Y-%m-%dT%H:%M')
    pet = SelectField('Pet:', coerce=int, choices=[(g.cod_pet, g.nome_pet) for g in tb_pet.query.order_by('nome_pet')])
    status = SelectField('Situação:', coerce=int, choices=[(0,"Agendada"),(1,"Realizada"),(2,"Cancelada")])
    observacoes = TextAreaField('Observações:')

    