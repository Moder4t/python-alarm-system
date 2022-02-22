import smtplib
import logging 

#------------------------------------------------------------------------------------------------------------------------------------------
#Debut de la class email
class email: 
    SMTP_USER = "2195882@collegeahuntsic.qc.ca" 
    SMTP_PASSWORD = "s891006" 
    SMTP_SERVER = "smtp-mail.outlook.com" 
    SMTP_PORT = 587 
    emailFrom = str 
    nameFrom = str 
    emailTo = str 
    nameTo = str
#------------------------------------------------------------------------------------------------------------------------------------------
# Proprieter du e-mail
    def __init__(self, emailFrom, nameFrom, emailTo, nameTo):
        self.emailFrom = emailFrom 
        self.nameFrom = nameFrom 
        self.emailTo = emailTo 
        self.nameTo = nameTo 
        self.log = LogHistory()
#------------------------------------------------------------------------------------------------------------------------------------------
#Envoie de e-mail
    def send(self, objet, msg): 
        entete = ( 
            "From: " + self.nameFrom + " <" + self.emailFrom + ">\n" 
            "To: " + self.nameFrom + " <" + self.emailTo + ">\n" 
            "Subject:" + objet + "\n\n" 
            ) 
        print(entete + msg) 
        try: 
            server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)  
            server.starttls() 
            server.login(self.SMTP_USER, self.SMTP_PASSWORD) 
            server.sendmail(self.emailFrom, self.emailTo, (entete + msg)) 
            server.close() 
        except smtplib.SMTPException: 
            self.log.error("Impossible d'envoyer le mail a " + self.emailTo)
        except (smtplib.socket.error, smtplib.SMTPConnectError): 
            self.log.error("Connexion impossible au serveur SMTP")
#------------------------------------------------------------------------------------------------------------------------------------------
# Debut de la class Log
class LogHistory:
    def __init__(self):
        LOG_LEVEL = logging.ERROR
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        if LOG_LEVEL >= logging.ERROR: 
            logging.basicConfig(filename = "monSysteme.log", level = LOG_LEVEL, format = LOG_FORMAT) 
        else: 
            logging.basicConfig(level = LOG_LEVEL, format = LOG_FORMAT)
    def debug(self, msg):
        logging.debug(msg)
    def error(self, msg):
        logging.error(msg)
    def critical(self, msg):
        logging.critical(msg)
#------------------------------------------------------------------------------------------------------------------------------------------
