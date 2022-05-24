from models import Pessoas, Usuarios


def inserir_pessoas():
    pessoa = Pessoas(nome='Juliana', idade=19)
    print(pessoa)
    pessoa.save()


def consulta_pessoas():
    pessoas = Pessoas.query.all()
    print(pessoas)


def alterar_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Juliana').first()
    pessoa.nome = 'Jusinha'
    pessoa.save()


def excluir_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Tetheuso').first()
    pessoa.delete()


def inserir_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha, ativo='0')
    usuario.save()


def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print([[usuario.login, usuario.ativo] for usuario in usuarios])


if __name__ == '__main__':
    consulta_todos_usuarios()
