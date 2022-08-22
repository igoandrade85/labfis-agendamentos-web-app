from app import db

class Docente(db.Model):
    __tablename__ = 'docentes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    agendamentos = db.relationship('Agendamento', backref='docentes', cascade = "all,delete", lazy=True)

    def __repr__(self):
        return f'<Docente {self.nome}>'

class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    experimentos = db.relationship('Experimento', backref='areas', lazy=True)

    def __repr__(self):
        return f'<Area {self.nome}>'

class Experimento(db.Model):
    __tablename__ = 'experimentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    arquivos = db.relationship('Arquivo', backref='experimentos', cascade = "all,delete", lazy=True)
    agendamentos = db.relationship('Agendamento', backref='experimentos', lazy=True)

    def __repr__(self):
        return f'<Experimento {self.nome}>'


class Arquivo(db.Model):
    __tablename__ = 'arquivos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    experimento_id = db.Column(db.Integer, db.ForeignKey('experimentos.id'), nullable=False)

    def __repr__(self):
        return f'<Arquivo {self.nome}>'

class Turno(db.Model):
    __tablename__ = 'turnos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(16), unique=True, nullable=False)
    experimentos = db.relationship('Agendamento', backref='turnos', lazy=True)

    def __repr__(self):
        return f'<Turno {self.nome}>'

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    semestre = db.Column(db.String(16), nullable=False)
    turno_id = db.Column(db.Integer, db.ForeignKey('turnos.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    experimento_id = db.Column(db.Integer, db.ForeignKey('experimentos.id'))

    def __repr__(self):
        return f'<Agendamento {self.id}>'
