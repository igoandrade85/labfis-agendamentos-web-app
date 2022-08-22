from app import db

from models import *

if __name__=="__main__":
    docentes = [
        #Docente(nome="Albert Einstein", email="einstein@yahoo.com"),
        #Docente(nome="Isaac Newton", email="newton@yahoo.com"),

        Docente(nome="Heverton Silva de Camargos", email="hscamargos@uft.edu.br"),
        Docente(nome="Moisés de Souza Arantes Neto", email="netomoises@mail.uft.edu.br"),
        Docente(nome="Salmo Moreira Sidel", email="sidel@mail.uft.edu.br"),
        Docente(nome="Antonio Wanderley de Oliveira", email="wanderley@uft.edu.br"),
        Docente(nome="Marcelo Leineker", email="leineker@gmail.com")
    ]
    db.session.add_all(docentes)

    experimentos_dict = {
        'Mecânica': [
            'Instrumentos de Medidas', 'Paquímetro', 'Micrômetro', 'Movimento Retilíneo Uniforme (MRU)', 'Movimento Retilíneo Uniformemente Acelerado (MRUV)', 'Queda Livre', 'Lançamento Oblíquo', 'Coeficiente de atrito', 'Segunda Lei de Newton', 'Mesa de Forças (Equilíbrio estático)', 'Equilíbrio Rotacional'
        ],
        'Hidrostática': ['Princípio de Arquimedes e Empuxo'],
        'Oscilações e Ondas': [
            'Lei de Hooke', 'Movimento Harmônico Simples (MHS)', 'Pêndulo Simples'
        ],
        'Termodinâmica': [
            'Capacidade Térmica de um calorímetro', 'Calor específico de um sólido', 'Dilatação Térmica', 'Lei de Boyle-Mariote', 'Lei do Resfriamento de Newton'
        ],
        'Eletricidade e Magnetismo': ['Campo Elétrico', 'Lei de Ohm', 'Carga e Descarga do Capacitor']
    }

    experimentos = []
    for area in experimentos_dict.keys():
        for tema in experimentos_dict[area]:
            experimento = Experimento(nome=tema, area=area, descricao="")
            experimentos.append(experimento)
    db.session.add_all(experimentos)


    db.session.commit()
    print("Banco de dados criado com sucesso!")