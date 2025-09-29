import win32com.client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import cv2
import sqlite3

def opcao():
    try:
        opcao = int(input("Escolha uma opção: "))
        return opcao
    except Exception as e:
        print(f"Escolha inválida! Erro: {e}")

def enviar_email(email, nome):
    smtp_server ="smtp.gmail.com"
    smtp_port = 587
    email_usuario = "taylan.gonzaga@al.infnet.edu.br"
    email_senha = "ikhx mbjj wswl szej"
    data = datetime.now()
    hora = data.strftime('%H:%M')

    remetente = email_usuario
    destinatario = email
    assunto = "Comparecimento SCA"
    corpo = f"Olá, {nome}! Esse é seu registro de comparecimento ao SCA.\n\nData: {data}\n\nHorário de entrada: {hora}"

    msg = MIMEMultipart()
    msg["From"] = email_usuario
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain"))

    try:
        server=smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_usuario, email_senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        print("Mensagem enviada com sucesso!")
        server.quit()
    except Exception as e:
        print(f"Erro: {e}")

def sistema_voz(mensagem):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")

    for i, voice in enumerate(speaker.GetVoices()):
        print(i, voice.GetDescription())

    speaker.Rate=0

    speaker.Voice=speaker.getVoices().Item(0)
    texto = mensagem

    speaker.Speak(texto)

def sistema_facial():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a câmera!")
        exit()

    print("Pressione G para salvar a foto.")
    print("Pressione Q para salvar a foto.")

    contador = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Não foi possível capturar o frame!")
            break

        cv2.imshow('Camera', frame)

        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('g'):
            nome_arquivo = f"foto_{contador}.png"
            cv2.imwrite(nome_arquivo, frame)
            print(f"Foto salva como: {nome_arquivo}")
            contador += 1
        elif tecla == ord('q'):
            print("Saindo do programa!")
            break

    cap.release()
    cv2.destroyAllWindows()

def init():
    conexao = sqlite3.connect("sa.db")
    cursor = conexao.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios(
            CPF VARCHAR(20) PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cartao VARCHAR(15) NOT NULL,
            foto VARCHAR(50),
            email VARCHAR(50) NOT NULL,
            telefone VARCHAR(20) NOT NULL
            )
''')