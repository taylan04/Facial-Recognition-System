from util import *
from menu import menu
from crud import *

def operacao():
    """
    executa o loop principal do sistema, exibindo o menu e chamando as operações
    correspondentes com base na opção escolhida pelo usuário.

    returns:
        None
    """
    while True:
        menu()
        n = opcao()
        match n:
            case 1:
                cadastrar_usuario()
            case 2:
                buscar()
            case 3:
                atualizar_usuario()
            case 4:
                excluir()
            case 5:
                listar_usuarios()
            case 6:
                break
            case __:
                buscar_cartao(n)

init()
operacao()
conexao.close()
