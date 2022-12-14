import os
from datetime import date, datetime, timedelta
from xmlrpc.client import Boolean
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'pi=3.14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)

from models import *


def incluir_docente(nome, email):
    existe_email = Docente.query.filter_by(email=email).first()
    if not existe_email:
        docente = Docente(nome=nome, email=email)
        db.session.add(docente)
        db.session.commit()
        return True
    return False

def verifica_conflito_agendamento(data, turno_id, agendamento_id=None):
    agendamento = Agendamento.query.filter_by(data=data, turno_id=turno_id).first()
    # novo agendamento
    if agendamento_id is None:
        return bool(agendamento)
    
    # editar agendamento
    if agendamento:
        if agendamento.id == agendamento_id:
            return False
        return True

def incluir_agendamento(docente_id, semestre, data, turno_id, experimento_id=None, descricao_atividades=None):
    if not verifica_conflito_agendamento(data, turno_id):
        agendamento = Agendamento(data=data, semestre=semestre, turno_id=turno_id, experimento_id=experimento_id, docente_id=docente_id, descricao_atividades=descricao_atividades)
        db.session.add(agendamento)
        db.session.commit()
        return True
    return False

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.route('/')
def index():
    cor = ['lightcoral', 'seagreen', 'cornflowerblue', 'forestgreen', 'blueviolet', 'coral', 'royalblue', 'darkorange', 'dodgerblue']
    agendamentos = Agendamento.query.order_by(Agendamento.semestre, Agendamento.data, Agendamento.turno_id).all()
    events = []
    for agendamento in agendamentos:
        if agendamento.experimentos:
            tema = agendamento.experimentos.nome
        elif agendamento.descricao_atividades:
            if len(agendamento.descricao_atividades) > 150:
                tema = agendamento.descricao_atividades[:150] + "..."
            else:
                tema = agendamento.descricao_atividades
        else:
            tema = 'N??o informado'
        events.append({
            'title': agendamento.docentes.email.split('@')[0],
            'description': f"Tema: {tema} Turno: {agendamento.turnos.nome}",
            'date': agendamento.data.strftime('%Y-%m-%d'),
            'color': cor[agendamento.docentes.id],
            'docente_id': agendamento.docente_id

        })
    return render_template('index.html', events=events)

@app.route('/docentes')
def get_docentes():
    docentes = Docente.query.all()
    return render_template('docentes.html', docentes=docentes)

@app.route('/docente/<int:id>')
def get_docente(id):
    today = datetime.today()
    year = today.year
    semester = 1 if today.month < 6 else 2
    current_semester = f"{year}.{semester}"
    agendamentos = Agendamento.query.filter_by(docente_id=id).order_by(Agendamento.semestre, Agendamento.data, Agendamento.turno_id).all()
    semestres = [f"{y}.{s}" for y in range(2022, year+5) for s in range(1,3)]
    turnos = Turno.query.all()
    experimentos = Experimento.query.order_by(Experimento.area_id).all()
    docente = Docente.query.filter_by(id=id).first()
    
    return render_template('docente_detalhes.html', docente=docente, experimentos=experimentos, turnos=turnos, semestres=semestres, agendamentos=agendamentos,current_semester=current_semester)

@app.route('/docente/<int:docente_id>/insert/agendamento-rapido', methods=["POST"])
def insert_agendamento_rapido(docente_id):
    delta = timedelta(days=1)

    semestre = request.form.get('semestre')
    turno_id = request.form.get('turno')

    data_inicial = datetime.strptime(request.form.get('data_inicial'), '%Y-%m-%d')
    data_final = datetime.strptime(request.form.get('data_final'), '%Y-%m-%d')
    wdays = request.form.getlist('weekdays')
    data = data_inicial
    success = False
    while (data <= data_final):
        for wday in wdays:
            if data.weekday() == int(wday):
                inclusao_agendamento = incluir_agendamento(docente_id, semestre, data, turno_id, experimento_id=None)
                if inclusao_agendamento:
                    success = True
                else:
                    turno = Turno.query.filter_by(id=turno_id).first()
                    flash(f"warning#J?? existe uma reserva para {data.strftime('%d/%m/%Y')}, per??odo {turno.nome}.")
        data += delta
    if success:
        flash('success#Dados inseridos com sucesso!')
    return redirect(url_for('get_docente', id=docente_id)) 

@app.route('/docente/<int:docente_id>/insert/agendamento', methods=["POST"])
def insert_agendamento(docente_id): 
    data = datetime.strptime(request.form.get('data'), "%Y-%m-%d")
    turno_id = int(request.form.get('turno'))
    try:
        experimento_id = int(request.form.get('tema'))
    except:
        experimento_id = None
    semestre = request.form.get('semestre')
    descricao_atividades = request.form.get('descricao_atividades')
    inclusao_agendamento = incluir_agendamento(docente_id, semestre, data, turno_id, experimento_id, descricao_atividades)
    if inclusao_agendamento:
        flash('success#Dados inseridos com sucesso!')
    else:
        turno = Turno.query.filter_by(id=turno_id).first()
        flash(f"warning#J?? existe uma reserva para {data.strftime('%d/%m/%Y')}, per??odo {turno.nome}.")
    return redirect(url_for('get_docente', id=docente_id))

@app.route('/docente/<int:docente_id>/update/agendamento/<int:agendamento_id>', methods=["POST"])
def update_agendamento(docente_id, agendamento_id):
    data = datetime.strptime(request.form.get('data'), "%Y-%m-%d")
    turno_id = int(request.form.get('turno'))
    if not verifica_conflito_agendamento(data, turno_id, agendamento_id):
        try:
            experimento_id = int(request.form.get('tema'))
        except:
            experimento_id = None
        semestre = request.form.get('semestre')
        agendamento = Agendamento.query.filter_by(id=agendamento_id).first()
        agendamento.data = data
        agendamento.turno_id = turno_id
        agendamento.experimento_id = experimento_id
        agendamento.semestre = semestre
        agendamento.descricao_atividades = request.form.get('descricao_atividades')
        print(request.form.get('descricao_atividades'))
        db.session.commit()
        flash('success#Dados alterados com sucesso!')
    else:
        turno = Turno.query.filter_by(id=turno_id).first()
        flash(f"warning#J?? existe uma reserva para {data.strftime('%d/%m/%Y')}, per??odo {turno.nome}.")
    return redirect(url_for('get_docente', id=docente_id))

@app.route('/docente/<int:docente_id>/delete/agendamento/<int:agendamento_id>')
def delete_agendamento(docente_id, agendamento_id):
    agendamento = Agendamento.query.filter_by(id=agendamento_id).first()
    db.session.delete(agendamento)
    db.session.commit()
    flash('success#Dados exclu??dos com sucesso!')
    return redirect(url_for('get_docente', id=docente_id))


@app.route('/insert/docente', methods=["POST"])
def insert_docente():
    nome = request.form.get('nome')
    email = request.form.get('email')
    if incluir_docente(nome, email):
        flash('success#Dados inseridos com sucesso!')
    else:
        flash('warning#E-mail j?? existe!')
    return redirect(url_for('get_docentes'))

@app.route('/update/docente/<int:id>', methods=["POST"])
def update_docente(id):
    docente = Docente.query.filter_by(id=id).first()
    nome = request.form.get('nome')
    email = request.form.get('email')
    existe_email = Docente.query.filter_by(email=email).first()
    if not existe_email:
        docente.nome = nome
        docente.email = email
        db.session.commit()
        flash('success#Dados atualizados com sucesso!')
    else:
        if existe_email.id == id:
            docente.nome = nome
            docente.email = email
            db.session.commit()
            flash('success#Dados atualizados com sucesso!')
        else:
            flash('warning#E-mail j?? existe!')
    return redirect(url_for('get_docentes'))

@app.route('/delete/docente/<int:id>')
def delete_docente(id):
    docente = Docente.query.filter_by(id=id).first()
    db.session.delete(docente)
    db.session.commit()
    flash('success#Dados excu??dos com sucesso!')
    return redirect(url_for('get_docentes'))

@app.route('/experimentos')
def get_experimentos():
    areas = Area.query.all()
    experimentos = Experimento.query.order_by(Experimento.area_id).all()
    return render_template('experimentos.html', areas=areas, experimentos=experimentos)

@app.route('/insert/experimento', methods=["POST"])
def insert_experimento():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    area_id = request.form.get('area_id')
    existe_experimento = Experimento.query.filter_by(nome=nome).first()
    if not existe_experimento:
        experimento = Experimento(nome=nome, descricao=descricao, area_id=area_id)
        db.session.add(experimento)
        db.session.commit()
        flash('success#Dados inclu??dos com sucesso!')
    else:
        if existe_experimento:
            flash('warning#Experimento j?? existe!')

    return redirect(url_for('get_experimentos'))

@app.route('/update/experimento/<int:id>', methods=["POST"])
def update_experimento(id):
    experimento = Experimento.query.filter_by(id=id).first()
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    area_id = request.form.get('area_id')
    existe_nome = Experimento.query.filter_by(nome=nome).first()
    if not existe_nome:
        experimento.nome = nome
        experimento.descricao = descricao
        experimento.area_id = area_id
        db.session.commit()
        flash('success#Dados atualizados com sucesso!')
    else:
        if existe_nome.id == id:
            experimento.nome = nome
            experimento.descricao = descricao
            experimento.area_id = area_id
            db.session.commit()
            flash('success#Dados atualizados com sucesso!')
        else:
            flash(f'warning#Nome {nome} j?? existe!')
    return redirect(url_for('get_experimento', id=id))

@app.route('/delete/experimento/<int:id>')
def delete_experimento(id):
    experimento = Experimento.query.filter_by(id=id).first()
    db.session.delete(experimento)
    db.session.commit()
    flash('success#Dados excu??dos com sucesso!')
    return redirect(url_for('get_experimentos'))

@app.route('/experimento/<int:id>')
def get_experimento(id):
    areas = Area.query.all()
    experimento = Experimento.query.filter_by(id=id).first()
    return render_template('experimento_detalhes.html', areas=areas, experimento=experimento)

if __name__=="__main__":
    app.run(debug=True)