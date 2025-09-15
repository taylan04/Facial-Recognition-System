import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server ="smtp.gmail.com"
smtp_port = 587
email_usuario = "taylan.gonzaga@al.infnet.edu.br"
email_senha = "ikhx mbjj wswl szej"

remetente = email_usuario
destinatario = "taylansilva0402@gmail.com"
assunto = "Teste de email"
corpo = "Olá, testando envio de email"

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