import re #Bibliothek regex wird importiert. Ist für die Überprüfung der Eingaben.
import mysql.connector#Bibliothek mysql wird importiert. Ist für die Verbindung zur Datenbank.
import datetime#Bibliothek datetime wird importiert. Ist für die Prüfung vom Geburtsdatum.
import smtplib
class DB:#Hier passiert alles was mit der DB zutun hat
    def __init__(self,user,pswd,host,port,db):#Hier werden die Informationen übergeben die ich für eine DB verbindung brauche
        self.config = {
            'user': user,
            'password': pswd,
            'host': host,
            'port': port,
            'database': db
        }
        self.mydb = None
        self.cur = None
    def connect(self):#eine Verbindung zur DB wird erstellt
        self.mydb = mysql.connector.connect(**self.config)
        self.cur = self.mydb.cursor()
    def insert_kunde(self,benutzername,pswt,vorname,nachname,email,geburtsdatum,telefon):#ein Neuer Kunde wird erstellt
        sql = "INSERT INTO `kunden`(`benutzername`, `passwort`, `vorname`, `nachname`, `email`, `geburtsdatum`, `telefon`) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(benutzername,pswt,vorname,nachname,email,geburtsdatum,telefon)
        self.cur.execute(sql)
        self.mydb.commit()
    def insert_kundenevent(self,kunden_id,event_id):
        sql="INSERT INTO `kundenevents` (`kID`, `eID`) VALUES ('{}', '{}');".format(kunden_id,event_id)
        self.cur.execute(sql)
        self.mydb.commit()
    def select_pswd(self,benutzername_email):#Hier wird das Passwort zurückgegeben was ich für die Anmeldung brauche
        sql = "SELECT passwort FROM `kunden` WHERE benutzername = '{}' or email = '{}'".format(benutzername_email, benutzername_email)
        self.cur.execute(sql)
        return self.cur.fetchall()
    def select_id(self,benutzername_email,pswd):
        sql = "SELECT id FROM kunden WHERE (`benutzername`='{}' or `email`='{}') and `passwort` = '{}' ".format(benutzername_email,pswd)
        self.cur.execute(sql)
        return self.cur.fetchall()
    def close(self):#die Verbindung zur DB wird getrennt
        self.cur.close()
        self.mydb.close()

class Login:#Hier passiert alles was im hintergrund der Webseite
    def __init__(self):
        self.db = DB('root','root','localhost','8889','coronatracking')#hier kann ich die Klasse DB verwenden bzw. hier wird sie aufgerufen
        self.id = None
    def anmelden(self):#anmelde funktion
        benutzername_email = 'ar'#Eingabefeld für Benutzername bzw. E-Mail
        pswt = 'a'#Eingabefeld für das Passwort
        
        benutzername_email = benutzername_email.strip()#Leerzeichen werden am Anfang und am Ende entfernt
        self.db.connect()#Verbindung zur DB wird erstellt
        pswd = self.db.select_pswd(benutzername_email)#das Passwort was zum Benutzername/E-Mail passt was in der DB gespeichert wurde wird hier zurückgegeben

        if pswt != pswd[0][0]:#hier wird geschaut ob das Passwort im Eingabefeld das gleiche Passwort ist wie in der DB. Stimmt es nicht kommt eine Fehlermeldung.
            fehler_medlung = "Fehler! Benutzername/E-Mail oder Passwort stimmt nicht."
            print(fehler_medlung)
        self.db.close()#Verbindung zur DB wird getrennt

    def neu(self):
        benutzername = 'ud'#Eingabefeld vom Benutzernamen
        pswt = 'u'#Eingabefeld vom Passwort
        pswt_w = 'u'#Eingabefeld vom Passwort wiederholen
        vorname = 'ulli'#Eingabefeld vom Vornamen
        nachname = 'doujak'#Eingabefeld vom Nachname
        email = 'ud@gmail.com'#Eingabefeld vom E-Mail
        geburtsdatum = '2020-11-10'#Eingabefeld vom Geburtsdatum
        telefon = ''#Eingabefeld von der Telefonnummer
       
       


        benutzername = benutzername.strip()#Leerzeichen werden am Anfang und am Ende entfernt
        vorname = vorname.strip()#Leerzeichen werden am Anfang und am Ende entfernt
        nachname = nachname.strip()#Leerzeichen werden am Anfang und am Ende entfernt

        p_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        p_name = "^[a-zA-Z]+$"

        if pswt != pswt_w:#Hier wird geschaut ob in den Passwortfelder das gleiche drinnen steht, wenn nicht kommt eine Fehlermeldung
                fehler_medlung = "Fehler! Passwortfelder stimmen nicht überein."
                print(fehler_medlung)
        geburtsdatum = datetime.datetime.strptime(geburtsdatum, '%Y-%m-%d')#wird zum type datetime conventiert
        if geburtsdatum > datetime.datetime.today():#schaut ob du schon geboren wurdest, wenn nicht fehler meldung
            print('Geburtsdatum stimmt nicht!')
        
        if not re.search(p_email,email):  
            print('Keine gültige Email Adresse')

        if not re.search(p_name,vorname):  
            print('Kein gültiger Vorname. Es sind nur Buchstaben erlaubt.') 
        if not re.search(p_name,nachname):  
            print('Kein gültiger Vorname. Es sind nur Buchstaben erlaubt.') 




        self.db.connect()#verbindung zur DB wird erstellt
        self.db.insert_kunde(benutzername,pswt,vorname,nachname,email,geburtsdatum,telefon)#neues Konot wird erstellt
        self.db.close()#Verbindung zur DB wird getrentt
    def kunde_id(self,benutzername_email,pswt):
        self.db.connect()#Verbindung zur DB wird erstellt
        self.id = self.db.select_id(benutzername_email,pswt)
        self.id = self.id[0][0]
        self.db.close()#Verbindung zur DB wird getrent
    
    def kundenevent(self):
        self.db.connect()#Verbindung zur DB wird erstellt
        event_id = '1'
        self.db.insert_kundenevent(self.id,event_id)
        self.db.close()#Verbindung zur DB wird getrent
    def mail(self):
        user = 'alisa6rieger@gmail.com'
        pwd = 'spuzunwyyivbpnbe'
        mail_text = 'Es gab einen Coronafall!'
        subject = 'Warnung!'

        
        MAIL_FROM = user
        RCPT_TO  = ", ".join(emails)
        DATA = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (MAIL_FROM, RCPT_TO, subject, mail_text)
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user, pwd)
        server.sendmail(MAIL_FROM, RCPT_TO, DATA)
        server.quit()
Website = Login()
Website.neu()
# Website.anmelden()