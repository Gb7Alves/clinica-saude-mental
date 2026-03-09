from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Paciente, Profissional, Consulta, Agendamento
from datetime import datetime, timedelta

# Blueprints
main_bp = Blueprint('main', __name__)
pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')
profissionais_bp = Blueprint('profissionais', __name__, url_prefix='/profissionais')
consultas_bp = Blueprint('consultas', __name__, url_prefix='/consultas')
agendamentos_bp = Blueprint('agendamentos', __name__, url_prefix='/agendamentos')

# ==================== ROTAS PRINCIPAIS ====================
@main_bp.route('/')
def index():
    total_pacientes = Paciente.query.count()
    total_profissionais = Profissional.query.count()
    total_consultas = Consulta.query.count()
    agendamentos_proximos = Agendamento.query.filter(
        Agendamento.status == 'Agendado',
        Agendamento.data_agendamento >= datetime.now()
    ).count()
    
    return render_template('index.html', 
                         total_pacientes=total_pacientes,
                         total_profissionais=total_profissionais,
                         total_consultas=total_consultas,
                         agendamentos_proximos=agendamentos_proximos)

# ==================== ROTAS DE PACIENTES ====================
@pacientes_bp.route('/')
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes/listar.html', pacientes=pacientes)

@pacientes_bp.route('/novo', methods=['GET', 'POST'])
def novo_paciente():
    if request.method == 'POST':
        try:
            paciente = Paciente(
                nome=request.form['nome'],
                cpf=request.form['cpf'],
                data_nascimento=datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date(),
                telefone=request.form['telefone'],
                email=request.form.get('email'),
                endereco=request.form.get('endereco'),
                historico_medico=request.form.get('historico_medico')
            )
            db.session.add(paciente)
            db.session.commit()
            flash(f'Paciente {paciente.nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('pacientes.listar_pacientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar paciente: {str(e)}', 'danger')
    
    return render_template('pacientes/novo.html')

@pacientes_bp.route('/<int:id>')
def ver_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    consultas = Consulta.query.filter_by(paciente_id=id).all()
    agendamentos = Agendamento.query.filter_by(paciente_id=id).all()
    
    return render_template('pacientes/ver.html', 
                         paciente=paciente, 
                         consultas=consultas,
                         agendamentos=agendamentos)

@pacientes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            paciente.nome = request.form['nome']
            paciente.cpf = request.form['cpf']
            paciente.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
            paciente.telefone = request.form['telefone']
            paciente.email = request.form.get('email')
            paciente.endereco = request.form.get('endereco')
            paciente.historico_medico = request.form.get('historico_medico')
            
            db.session.commit()
            flash('Paciente atualizado com sucesso!', 'success')
            return redirect(url_for('pacientes.ver_paciente', id=paciente.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar paciente: {str(e)}', 'danger')
    
    return render_template('pacientes/editar.html', paciente=paciente)

@pacientes_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    try:
        db.session.delete(paciente)
        db.session.commit()
        flash('Paciente deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar paciente: {str(e)}', 'danger')
    
    return redirect(url_for('pacientes.listar_pacientes'))

# ==================== ROTAS DE PROFISSIONAIS ====================
@profissionais_bp.route('/')
def listar_profissionais():
    profissionais = Profissional.query.all()
    return render_template('profissionais/listar.html', profissionais=profissionais)

@profissionais_bp.route('/novo', methods=['GET', 'POST'])
def novo_profissional():
    if request.method == 'POST':
        try:
            profissional = Profissional(
                nome=request.form['nome'],
                cpf=request.form['cpf'],
                especialidade=request.form['especialidade'],
                telefone=request.form['telefone'],
                email=request.form.get('email'),
                numero_registro=request.form.get('numero_registro')
            )
            db.session.add(profissional)
            db.session.commit()
            flash(f'Profissional {profissional.nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('profissionais.listar_profissionais'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar profissional: {str(e)}', 'danger')
    
    return render_template('profissionais/novo.html')

@profissionais_bp.route('/<int:id>')
def ver_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    consultas = Consulta.query.filter_by(profissional_id=id).all()
    agendamentos = Agendamento.query.filter_by(profissional_id=id).all()
    
    return render_template('profissionais/ver.html', 
                         profissional=profissional,
                         consultas=consultas,
                         agendamentos=agendamentos)

@profissionais_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            profissional.nome = request.form['nome']
            profissional.cpf = request.form['cpf']
            profissional.especialidade = request.form['especialidade']
            profissional.telefone = request.form['telefone']
            profissional.email = request.form.get('email')
            profissional.numero_registro = request.form.get('numero_registro')
            
            db.session.commit()
            flash('Profissional atualizado com sucesso!', 'success')
            return redirect(url_for('profissionais.ver_profissional', id=profissional.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar profissional: {str(e)}', 'danger')
    
    return render_template('profissionais/editar.html', profissional=profissional)

@profissionais_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    try:
        db.session.delete(profissional)
        db.session.commit()
        flash('Profissional deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar profissional: {str(e)}', 'danger')
    
    return redirect(url_for('profissionais.listar_profissionais'))

# ==================== ROTAS DE CONSULTAS ====================
@consultas_bp.route('/')
def listar_consultas():
    consultas = Consulta.query.all()
    return render_template('consultas/listar.html', consultas=consultas)

@consultas_bp.route('/nova', methods=['GET', 'POST'])
def nova_consulta():
    if request.method == 'POST':
        try:
            consulta = Consulta(
                paciente_id=request.form['paciente_id'],
                profissional_id=request.form['profissional_id'],
                data_consulta=datetime.strptime(request.form['data_consulta'], '%Y-%m-%dT%H:%M'),
                diagnostico=request.form.get('diagnostico'),
                prescricao=request.form.get('prescricao'),
                observacoes=request.form.get('observacoes')
            )
            db.session.add(consulta)
            db.session.commit()
            flash('Consulta registrada com sucesso!', 'success')
            return redirect(url_for('consultas.listar_consultas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar consulta: {str(e)}', 'danger')
    
    pacientes = Paciente.query.all()
    profissionais = Profissional.query.all()
    return render_template('consultas/nova.html', pacientes=pacientes, profissionais=profissionais)

@consultas_bp.route('/<int:id>')
def ver_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    return render_template('consultas/ver.html', consulta=consulta)

@consultas_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            consulta.diagnostico = request.form.get('diagnostico')
            consulta.prescricao = request.form.get('prescricao')
            consulta.observacoes = request.form.get('observacoes')
            
            db.session.commit()
            flash('Consulta atualizada com sucesso!', 'success')
            return redirect(url_for('consultas.ver_consulta', id=consulta.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar consulta: {str(e)}', 'danger')
    
    return render_template('consultas/editar.html', consulta=consulta)

@consultas_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    try:
        db.session.delete(consulta)
        db.session.commit()
        flash('Consulta deletada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar consulta: {str(e)}', 'danger')
    
    return redirect(url_for('consultas.listar_consultas'))

# ==================== ROTAS DE AGENDAMENTOS ====================
@agendamentos_bp.route('/')
def listar_agendamentos():
    agendamentos = Agendamento.query.all()
    return render_template('agendamentos/listar.html', agendamentos=agendamentos)

@agendamentos_bp.route('/novo', methods=['GET', 'POST'])
def novo_agendamento():
    if request.method == 'POST':
        try:
            agendamento = Agendamento(
                paciente_id=request.form['paciente_id'],
                profissional_id=request.form['profissional_id'],
                data_agendamento=datetime.strptime(request.form['data_agendamento'], '%Y-%m-%dT%H:%M'),
                status=request.form.get('status', 'Agendado'),
                observacoes=request.form.get('observacoes')
            )
            db.session.add(agendamento)
            db.session.commit()
            flash('Agendamento criado com sucesso!', 'success')
            return redirect(url_for('agendamentos.listar_agendamentos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar agendamento: {str(e)}', 'danger')
    
    pacientes = Paciente.query.all()
    profissionais = Profissional.query.all()
    return render_template('agendamentos/novo.html', pacientes=pacientes, profissionais=profissionais)

@agendamentos_bp.route('/<int:id>')
def ver_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    return render_template('agendamentos/ver.html', agendamento=agendamento)

@agendamentos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            agendamento.data_agendamento = datetime.strptime(request.form['data_agendamento'], '%Y-%m-%dT%H:%M')
            agendamento.status = request.form.get('status')
            agendamento.observacoes = request.form.get('observacoes')
            
            db.session.commit()
            flash('Agendamento atualizado com sucesso!', 'success')
            return redirect(url_for('agendamentos.ver_agendamento', id=agendamento.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar agendamento: {str(e)}', 'danger')
    
    return render_template('agendamentos/editar.html', agendamento=agendamento)

@agendamentos_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    try:
        db.session.delete(agendamento)
        db.session.commit()
        flash('Agendamento deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar agendamento: {str(e)}', 'danger')
    
    return redirect(url_for('agendamentos.listar_agendamentos'))
