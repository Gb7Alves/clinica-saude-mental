from app import db
from datetime import datetime

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    endereco = db.Column(db.String(300), nullable=True)
    historico_medico = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    consultas = db.relationship('Consulta', backref='paciente', lazy=True, cascade='all, delete-orphan')
    agendamentos = db.relationship('Agendamento', backref='paciente', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Paciente {self.nome}>'


class Profissional(db.Model):
    __tablename__ = 'profissionais'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    numero_registro = db.Column(db.String(50), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    consultas = db.relationship('Consulta', backref='profissional', lazy=True, cascade='all, delete-orphan')
    agendamentos = db.relationship('Agendamento', backref='profissional', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Profissional {self.nome}>'


class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    data_consulta = db.Column(db.DateTime, nullable=False)
    diagnostico = db.Column(db.Text, nullable=True)
    prescricao = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Consulta {self.id}>'


class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    data_agendamento = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Agendado')  # Agendado, Realizado, Cancelado
    observacoes = db.Column(db.Text, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Agendamento {self.id}>'
