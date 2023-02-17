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

# criação da classe tipousuário conectada com o banco de dados mysql
class tb_tipostatus(db.Model):
    cod_tipostatus = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_tipostatus = db.Column(db.String(50), nullable=False)
    status_tipostatus = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    

# criação da classe tipopet conectada com o banco de dados mysql
class tb_tipopet(db.Model):
    cod_tipopet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_tipopet = db.Column(db.String(50), nullable=False)
    status_tipopet = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name   