import sqlite3
from datetime import datetime
from util import *
from menu import menu
import cv2

# SCA - Sistema de Controle de Acesso

conexao = sqlite3.connect("sa.db")
cursor = conexao.cursor()
camera = cv2.VideoCapture(0)
if not camera.isOpened():
        print("Erro ao abrir a câmera!")
        exit()

def cadastrar_usuario():
    """
    cadastra um novo usuário no banco de dados solicitando informações pessoais
    e capturando uma foto pela câmera.

    fluxo:
        - solicita cpf, nome e código do cartão
        - abre a câmera e salva a foto ao pressionar 'g'
        - solicita e-mail e telefone
        - insere os dados na tabela 'usuarios'

    returns:
        None
    """
    cpf = input("informe seu CPF: ")
    nome = input("Informe seu nome: ")
    cartao = input("Informe o código do seu cartão: ")
    print("\nPressione G para salvar a foto.")
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Não foi possível capturar o frame!")
            break

        cv2.imshow('Camera', frame)
        tecla = cv2.waitKey(1)  # & 0xFF
        if tecla == ord('g'):
            nome_arquivo = f"{cpf}.png"
            cv2.imwrite(nome_arquivo, frame)
            print(f"Foto salva como: {nome_arquivo}")
            break

    camera.release()
    cv2.destroyAllWindows()
    foto = nome_arquivo
    email = input("Informe seu email: ")
    telefone = input("Informe seu telefone: ")
    try:
        cursor.execute(f'''
            INSERT INTO usuarios (cpf, nome, cartao, foto, email, telefone) VALUES (?, ?, ?, ?, ?, ?)
        ''', (cpf, nome, cartao, foto, email, telefone))
        conexao.commit()
        print("Usuario salvo com sucesso!")
        sistema_voz(f"Olá {nome}, seja bem vindo!")
    except Exception:
        print("Erro ao inserir!")

def buscar():
    """
    busca um usuário no banco de dados pelo cpf informado.

    - exibe dados cadastrais e mostra a foto do usuário (se disponível).
    - dá as boas-vindas com mensagem de voz de acordo com o horário do dia.

    returns:
        None
    """
    cpf = input("\nInforme seu CPF: ")
    cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
    resultado = cursor.fetchone()
    hora = datetime.now().hour
    if resultado:
        if hora < 12:
            sistema_voz(f"Olá {resultado[1]} seu acesso foi liberado! Bom Dia.")
        elif hora >= 12 and hora < 18:
            sistema_voz(f"Olá {resultado[1]} seu acesso foi liberado! Boa Tarde.")
        else:
            sistema_voz(f"Olá {resultado[1]} seu acesso foi liberado! Boa Noite.")
        print(f"CPF: {resultado[0]}\nNome: {resultado[1]}\nCartao: {resultado[2]}\nEmail: {resultado[4]}\nTelefone: {resultado[5]}")
        foto = resultado[3]
        if foto:
            img = cv2.imread(resultado[3])
            cv2.imshow(f"Foto de {resultado[1]}", img)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
        else:
            sistema_voz("CPF não encontrado! Acesso negado.")
            print("CPF não encontrado!")

def buscar_cartao(cartao):
    """
    busca um usuário no banco de dados pelo número do cartão.

    - exibe dados cadastrais e mostra a foto do usuário (se disponível).
    - envia e-mail de registro de comparecimento.
    - dá as boas-vindas com mensagem de voz de acordo com o horário do dia.

    args:
        cartao (str): código do cartão do usuário.

    returns:
        None
    """
    cursor.execute("SELECT * FROM usuarios WHERE cartao = ?", (cartao,))
    resultado = cursor.fetchone()
    hora = datetime.now().hour
    if resultado:
        if 6 <= hora < 12:
            sistema_voz(f"Olá {resultado[1]} seu acesso foi liberado! Bom Dia.")
        elif 12 <= hora < 18:
            sistema_voz(f"Olá {resultado[1]} seu acesso foi liberado! Boa Tarde.")
        else:
            sistema_voz(f"Olá {resultado[1]} seu acesso foi liberado! Boa Noite.")
        print(f"CPF: {resultado[0]}\nNome: {resultado[1]}\nCartao: {resultado[2]}\nEmail: {resultado[4]}\nTelefone: {resultado[5]}")
        foto = resultado[3]
        if foto:
            img = cv2.imread(resultado[3])
            cv2.imshow(f"Foto de {resultado[1]}", img)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
            enviar_email(resultado[4], resultado[1])
    else:
        sistema_voz("Cartão Inválido! Acesso negado.")
        print("Cartão não encontrado na base de dados!")

def listar_usuarios():
    """
    lista todos os usuários cadastrados no banco de dados,
    exibindo cpf, nome, cartão, e-mail e telefone.

    returns:
        None
    """
    cursor.execute("SELECT * FROM usuarios")
    resultado = cursor.fetchall()
    if resultado:
        for usuario in resultado:
            print(f"\nCPF: {usuario[0]} - Nome: {usuario[1]} | Cartao: {usuario[2]} | Email: {usuario[4]} | Telefone: {usuario[5]}")

def excluir():
    """
    exclui um usuário do banco de dados pelo cpf informado.

    - solicita confirmação antes da exclusão.
    - informa o resultado da operação.

    returns:
        None
    """
    cpf = input("Digite seu CPF: ")
    cursor.execute("SELECT * FROM usuarios WHERE CPF = ?", (cpf,))
    resultado = cursor.fetchone()
    if resultado:
        confirmacao = input("\nDeseja mesmo excluir (SIM/NAO) ?: ")
        if confirmacao.lower() == "sim":
            cursor.execute("DELETE FROM usuarios WHERE CPF = ?", (cpf,))
            sistema_voz("Usuário deletado!")
            print("\nSeu usuário foi deletado!")
        else:
            print("\nOperação cancelada!")

def atualizar_usuario():
    """
    atualiza os dados de um usuário já cadastrado.

    - solicita cpf para localizar o usuário
    - permite alterar nome, cartão, e-mail e telefone
    - caso o campo seja deixado em branco, mantém o valor atual

    returns:
        None
    """
    print("\n--- Atualização Cadastral ---")
    cpf = input("Digite seu CPF: ")
    cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
    resultado = cursor.fetchone()
    if resultado:
        print("\nAperte ENTER para não mudar o campo apresentado")
        novo_nome = input(f"Nome [{resultado[1]}] / Novo nome: ").strip()
        novo_cartao = input(f"Cartão [{resultado[2]}] / Novo cartão: ").strip()
        novo_email = input(f"Email [{resultado[4]}] / Novo email: ").strip()
        novo_tel = input(f"Telefone [{resultado[5]}] / Novo telefone: ").strip()

        if not novo_nome:
            novo_nome = resultado[1]
        if not novo_cartao:
            novo_cartao = resultado[2]
        if not novo_email:
            novo_email = resultado[4]
        if not novo_tel:
            novo_tel = resultado[5]
        
        cursor.execute(
            "UPDATE usuarios SET nome=?, cartao=?, email=?, telefone=? WHERE cpf = ?",
            (novo_nome, novo_cartao, novo_email, novo_tel, cpf)
        )
        conexao.commit()
        print("\nAtualização cadastral obteve sucesso!")
    else:
        print("\nCPF não encontrado na base de dados!")
