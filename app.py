from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# USUARIOS = {
#     'matheus': '123',
#     'juliana': '321'
# }


# @auth.verify_password
# def verificacao(login, senha):
#     # print('validando user')
#     # print(USUARIOS.get(login) == senha)
#     if not (login, senha):
#         return False
#     return USUARIOS.get(login) == senha

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha, ativo='1').first()


class Pessoa(Resource):
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Pessoa não encontrada'
            }
        return response

    @auth.login_required
    def put(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            dados = request.json
            if 'nome' in dados:
                pessoa.nome = dados['nome']
            if 'idade' in dados:
                pessoa.idade = dados['idade']
            pessoa.save()
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Pessoa não encontrada'
            }
        return response

    @auth.login_required
    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {'status': 'sucesso', 'mensagem': 'Pessoa {} excluida com sucesso'.format(pessoa.nome)}
            pessoa.delete()
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Pessoa não encontrada'
            }
        return response


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': i.id,
                     'nome': i.nome,
                     'idade': i.idade}
                    for i in pessoas]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response


class AtividadesDeUmaPessoa(Resource):
    def get(self, nome_pessoa):
        pessoa = Pessoas.query.filter_by(nome=nome_pessoa).first()
        if pessoa is not None:
            atividades = Atividades.query.filter_by(pessoa=pessoa)
            response = [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome, 'status': i.status} for i in atividades]
        else:
            response = {
                'status': 'erro',
                'mensagem': 'Pessoa não encontrada'
            }
        return response


class Atividade(Resource):
    def get(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            response = {
                'pessoa': atividade.pessoa.nome,
                'nome': atividade.nome,
                'status': atividade.status,
                'id': atividade.id
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Atividade não encontrada'
            }
        return response

    @auth.login_required
    def put(self, id):
        try:
            dados = request.json
            atividade = Atividades.query.filter_by(id=id).first()
            atividade.status = dados['status']
            atividade.save()
            response = {
                'pessoa': atividade.pessoa.nome,
                'nome': atividade.nome,
                'status': atividade.status,
                'id': atividade.id
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Atividade não encontrada'
            }
        return response


class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome, 'status': i.status} for i in atividades]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        if pessoa is not None:
            atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status=dados['status'])
            atividade.save()
            response = {
                'pessoa': atividade.pessoa.nome,
                'nome': atividade.nome,
                'status': atividade.status,
                'id': atividade.id
            }
        else:
            response = {
                'status': 'erro',
                'mensagem': 'Pessoa não encontrada'
            }
        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(AtividadesDeUmaPessoa, '/atividades/<string:nome_pessoa>/')
api.add_resource(Atividade, '/atividades/<int:id>/')
api.add_resource(ListaAtividades, '/atividades/')

if __name__ == '__main__':
    app.run(debug=True)
