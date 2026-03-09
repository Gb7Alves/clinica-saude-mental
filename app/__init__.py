from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuração do banco de dados
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'clinica.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Registrar blueprints
    from app.routes import main_bp, pacientes_bp, profissionais_bp, consultas_bp, agendamentos_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(profissionais_bp)
    app.register_blueprint(consultas_bp)
    app.register_blueprint(agendamentos_bp)
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app
