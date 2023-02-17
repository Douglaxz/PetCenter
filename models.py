from petcenter import db

# criação da classe usuário conectada com o banco de dados mysql
class tb_user(db.Model):
    cod_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False)
    password_user = db.Column(db.String(50), nullable=False)
    status_user = db.Column(db.Integer, nullable=False)
    login_user = db.Column(db.String(50), nullable=False)
    cod_usertype = db.Column(db.Integer, nullable=False)
    email_user = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

# criação da classe tipousuário conectada com o banco de dados mysql
class tb_usertype(db.Model):
    cod_usertype = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_usertype = db.Column(db.String(50), nullable=False)
    status_usertype = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    
 

# criação da classe tipopet conectada com o banco de dados mysql
class tb_tipopet(db.Model):
    cod_tipopet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_tipopet = db.Column(db.String(50), nullable=False)
    status_tipopet = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name   


# criação da classe tutor conectada com o banco de dados mysql
class tb_tutor(db.Model):
    cod_tutor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_tutor = db.Column(db.String(50), nullable=False)
    end_tutor = db.Column(db.String(90), nullable=False)
    status_tutor = db.Column(db.Integer, nullable=False)
    fone_tutor = db.Column(db.String(50), nullable=False)
    obs_tutor = db.Column(db.String(90), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name  

# criação da classe pet conectada com o banco de dados mysql
class tb_pet(db.Model):
    cod_pet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_tipopet = db.Column(db.Integer, nullable=False)
    nome_pet = db.Column(db.String(50), nullable=False)
    raca_pet = db.Column(db.String(90), nullable=False)
    status_pet = db.Column(db.Integer, nullable=False)
    datanasc_pet = db.Column(db.DateTime, nullable=False)
    obs_pet = db.Column(db.String(90), nullable=False)
    cod_tutor = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name  

# criação da classe consulta conectada com o banco de dados mysql
class tb_consulta(db.Model):
    cod_consulta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_pet = db.Column(db.Integer, nullable=False)
    data_consulta = db.Column(db.DateTime, nullable=False)
    status_consulta = db.Column(db.Integer, nullable=False)   
    obs_consulta = db.Column(db.String(90), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name  
