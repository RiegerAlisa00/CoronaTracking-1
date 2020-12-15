import re #Bibliothek regex wird importiert. Ist für die Überprüfung der Eingaben.
import mysql.connector#Bibliothek mysql wird importiert. Ist für die Verbindung zur Datenbank.
import datetime#Bibliothek datetime wird importiert. Ist für die Prüfung vom Geburtsdatum.
import smtplib#Bibliothek smtplib wird importiert. Ist für den Zugriff und versendung der E-Mails zuständig.
import random#Bibliothek random wird importiert.Ist für die 5 Stellige Verefezierung für Passwort zurücksetzen.
import base64#Bibliothek für die Verschlüsselung
from tkinter import *#Bibliothek für die Obrfläche


class GUI:#Klasse der Oberfläche
    def __init__(self,surface):
        self.backend = Backend()#zugriff auf die Klasse Backend
        """ GUI Fenster """
        self.surface = surface
        self.title = 'Coronatracking-App'
        self.surface.title(self.title)
        #Hier werden alle Labels, Enterys, etc. erstellt die jemals im Programm verwendet wird, ohne ihre Eigenschaft zu bestimmen also Text, Farbe, usw.
        """ Hauptseit: Listenbox """
        self.listbox = Listbox(self.surface)
        self.index = None
        self.inhalt = None
        self.scroll = Scrollbar(self.surface,orient=VERTICAL)

        #regestrierung
        self.benutzername = Label(self.surface)
        self.pswt = Label(self.surface)
        self.pswt_w = Label(self.surface)
        self.vorname = Label(self.surface)
        self.nachname = Label(self.surface)
        self.email = Label(self.surface)

        self.e_benutzername = Entry(self.surface)
        self.e_pswt = Entry(self.surface,show="*")
        self.e_pswt_w = Entry(self.surface,show="*")
        self.e_vorname = Entry(self.surface)
        self.e_nachname = Entry(self.surface)
        self.e_email = Entry(self.surface)

        self.b_save = Button(self.surface)

        self.fehler = Label(self.surface)
        #login
        self.userLabel = Label(self.surface)
        self.userEntry = Entry(self.surface)
        self.passLabel = Label(self.surface)
        self.passEntry = Entry(self.surface,show="*")

        self.b_regestrieren = Button(self.surface)
        self.b_login = Button(self.surface)
        self.b_pswt_return = Button(self.surface)
        #startseite
        self.t_verlauf = Label(self.surface)

        self.b_logout = Button(self.surface)

        #Events erstellen (GUI Fenster)
        self.name = Label(self.surface)
        self.datum = Label(self.surface)
        self.zeit = Label(self.surface)

        self.ev_name = Entry(self.surface)
        self.ev_datum = Entry(self.surface)
        self.ev_zeit = Entry(self.surface)
        self.ev_button = Button(self.surface)
        self.ev_error = Label(self.surface)

    def clear_design(self):
        #hier werden alle Labels, Enterys, etc. ausgeblendet
        """ Hauptseit: Listenbox """
        self.listbox.grid_forget()
        self.scroll.grid_forget()

        #regestrieren
        self.benutzername.grid_forget()
        self.pswt.grid_forget()
        self.pswt_w.grid_forget()
        self.vorname.grid_forget()
        self.nachname.grid_forget()
        self.email.grid_forget()

        self.e_benutzername.grid_forget()
        self.e_pswt.grid_forget()
        self.e_pswt_w.grid_forget()
        self.e_vorname.grid_forget()
        self.e_nachname.grid_forget()
        self.e_email.grid_forget()

        self.b_save.grid_forget()

        self.fehler.grid_forget()
        #login
        self.userLabel.grid_forget()
        self.userEntry.grid_forget()
        self.passLabel.grid_forget()
        self.passEntry.grid_forget()

        self.b_regestrieren.grid_forget()
        self.b_login.grid_forget()
        self.b_pswt_return.grid_forget()

        #startseite
        self.t_verlauf.grid_forget()
        
        self.b_logout.grid_forget()

        #Events .grid_forget()
        self.name.grid_forget()
        self.datum.grid_forget()
        self.zeit.grid_forget()

        self.ev_name.grid_forget()
        self.ev_datum.grid_forget()
        self.ev_zeit.grid_forget()
        self.ev_button.grid_forget()
        self.ev_error.grid_forget()


    def regestrieren(self):
        self.clear_design()#ganzer Inhalt des Fensters wird ausgeblendet
        #der Text der Labels werden geändert
        self.benutzername.config(text='Benutzername:',bg="#005ca9", fg="white")
        self.pswt.config(text='Passwort:',bg="#005ca9", fg="white")
        self.pswt_w.config(text='Passwort wiederholen:',bg="#005ca9", fg="white")
        self.vorname.config(text='Vorname:',bg="#005ca9", fg="white")
        self.nachname.config(text='Nachname:',bg="#005ca9", fg="white")
        self.email.config(text='Email:',bg="#005ca9", fg="white")
        #Labels,Enterys, Buttons werden hier positioniert
        self.benutzername.grid(row=2, column=1, pady = (20,10),padx = (80))
        self.pswt.grid(row=4, column=1, pady = (0,10))
        self.pswt_w.grid(row=6, column=1, pady = (0,10))
        self.vorname.grid(row=8, column=1, pady = (0,10))
        self.nachname.grid(row=10, column=1, pady = (0,10))
        self.email.grid(row=14, column=1, pady = (0,10))

        self.e_benutzername.grid(row=2, column=2, pady = (20,10))
        self.e_pswt.grid(row=4, column=2, pady = (0,10))
        self.e_pswt_w.grid(row=6, column=2, pady = (0,10))
        self.e_vorname.grid(row=8, column=2, pady = (0,10))
        self.e_nachname.grid(row=10, column=2, pady = (0,10))
        self.e_email.grid(row=14, column=2, pady = (0,10))

        self.b_save.config(text='Erstellen', command=self.benutzer_erstellen,bg="green")#der Text vom Button wird geändert und festgelegt welche Methode aufgerufen wird, wenn der Button geklickt wird
        self.b_save.grid(row=18, column=1, pady = (12))
        self.fehler.grid(row=3, column=5)
        


        
    def benutzer_erstellen(self):
        #Inahlter der Eingabefelder werden rausgehohlt
        benutzername = self.e_benutzername.get()
        pswt = self.e_pswt.get()
        pswt_w = self.e_pswt_w.get()
        vorname = self.e_vorname.get()
        nachname = self.e_nachname.get()
        email = self.e_email.get()
        #Eingaben werden überprüft
        fehler_text = self.backend.neu(benutzername,pswt,pswt_w,vorname,nachname,email)
        
        if fehler_text != None:#Gibt es einen Fehler wird die Meldung angezeigt und man kommt nicht weiter
            self.fehler.config(text=fehler_text)
            
            self.regestrieren()
        else:#Inhalte der Eingabefelder werden entleert, Text vom Lable fehler wird geändert, man kommt auf die login Seite zurück
            self.fehler.config(text='')
            self.e_benutzername.delete(0,'end')
            self.e_pswt.delete(0,'end')
            self.e_pswt_w.delete(0,'end')
            self.e_vorname.delete(0,'end')
            self.e_nachname.delete(0,'end')
            self.e_email.delete(0,'end')
            self.login()

    def login(self):
        self.surface.configure(bg="#005ca9")
        self.surface.geometry("600x400")
        self.clear_design()#ganzer Inhalt des Fensters wird ausgeblendet
        #der Text der Labels werden geändert
        self.userLabel.config(text="Email/Benutzername:",bg="#005ca9", fg="white")
        self.passLabel.config(text="Passwort:",bg="#005ca9", fg="white")
        #die Labels werden positioniert
        self.userLabel.grid(row=1, column=0, padx = (50))
        self.userEntry.grid(row=1, column=1,pady = (20))
        self.passLabel.grid(row=2, column=0)
        self.passEntry.grid(row=2, column=1,pady = (10))
        #die Eigenschaften der Buttons werden geändert
        self.b_regestrieren.config(text='Regestrieren',command=self.regestrieren,bg="green")
        self.b_login.config(text='Login',command=self.login_pr,bg="green")
        self.b_pswt_return.config(text='Passwort zurücksetzen',command=self.pswt_r,bg="#33ccff")
        #die Buttons werden positioniert
        self.b_regestrieren.grid(row=2, column=1)
        self.b_login.grid(row=4, column=0)
        self.b_pswt_return.grid(row=3, column=1)
        self.fehler.grid(row=1, column=4)
        self.surface.mainloop()#fenster schließt sich nicht automatisch
    def login_pr(self):
        user = self.userEntry.get()
        pswt = self.passEntry.get()
        fehler_text = self.backend.anmelden(user, pswt)
        
        if fehler_text != None:
            print(fehler_text)
            self.fehler.config(text=fehler_text)
            
            self.login()
        else:
            self.fehler.config(text='')
            self.userEntry.delete(0,'end')
            self.passEntry.delete(0,'end')
            self.main()
    def main(self):
        self.clear_design()
        self.listbox.delete(0,'end')#alter Listbox stand wird gelöscht

        """Scrollbar wird zur Listbox hinzugefügt"""
        self.listbox["yscrollcommand"]=self.scroll.set
        self.scroll["command"]=self.listbox.yview
        
        for i in self.backend.kundenevent():#die aktuelle Liste wird in der Listbox angezeigt
            text = i[1]+" am "+str(i[2])+" um "+str(i[3])
            self.listbox.insert(END, text)
        #positionierung der Listbox und Scrollbar
        self.listbox.grid(row=1,column=1,columnspan=10,sticky=N+E+S+W)
        self.scroll.grid(row=1,column=10, sticky=E+N+S)

        self.t_verlauf.config(text='Verlauf',font = "Helvetica 16 bold italic")
 
        self.t_verlauf.grid(row = 0, column=1)
        self.b_logout.grid(row = 3, column=11)
        self.b_logout.config(text='Abmelden',command=self.logout)
    def logout(self):
        self.backend.logout()
        self.login()
    def pswt_r(self):
        pass
    #Fenster zum erstellen von Events
    def event_input(self):
        self.clear_design()
        self.name.config(text='Name:')
        self.datum.config(text='Datum:')
        self.zeit.config(text='Zeit:')
        self.ev_button.config(text="Event erstellen", command=self.event_erstellen)
        self.ev_error.config(text="")

        self.name.grid(row=0, column=0)
        self.datum.grid(row=1, column=0)
        self.zeit.grid(row=2, column=0)

        self.ev_name.grid(row=0, column=1)
        self.ev_datum.grid(row=1, column=1)
        self.ev_zeit.grid(row=2, column=1)

        self.ev_button.grid(row=3, column=1)
        self.ev_error.grid(row=4, column=0)
    def event_erstellen(self):
        #Input für den Eventnamen
        name = self.ev_name.get()
        #Input für das Eventdatum (YYYY-MM-DD Format, geht auch mit / oder .)
        datum = self.ev_datum.get()
        #Input für die Uhrzeit des Events (24:00 Format)
        zeit = self.ev_zeit.get()

        #Sind alle Felder ausgefüllt, wird das Event angelegt/erstellt.
        if name != None and datum != None and zeit != None:
            print("success")
            self.backend.evinput(name, datum, zeit)
        
        else:
            self.ev_error.config(text="Die Eingabe ist unvollständig!", fg="red")
            self.event_input()
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
    def insert_kunde(self,benutzername,pswt,vorname,nachname,email):#ein Neuer Kunde wird erstellt
        sql = "INSERT INTO `kunden`(`benutzername`, `passwort`, `vorname`, `nachname`, `email`) VALUES ('{}','{}','{}','{}','{}')".format(benutzername,pswt,vorname,nachname,email)
        self.cur.execute(sql)
        self.mydb.commit()
    def insert_kundenevent(self,kunden_id,event_id):
        sql="INSERT INTO `kundenevents` (`kID`, `eID`) VALUES ('{}', '{}');".format(kunden_id[0][0],event_id)
        self.cur.execute(sql)
        self.mydb.commit()
    def select_pswd(self,benutzername_email):#Hier wird das Passwort zurückgegeben was ich für die Anmeldung brauche
        sql = "SELECT passwort FROM `kunden` WHERE benutzername = '{}' or email = '{}'".format(benutzername_email, benutzername_email)
        self.cur.execute(sql)
        return self.cur.fetchall()
    def select_id(self,benutzername_email,pswd):
        sql = "SELECT id FROM kunden WHERE (`benutzername`='{}' or `email`='{}') and `passwort` = '{}' ".format(benutzername_email,benutzername_email,pswd)
        self.cur.execute(sql)
        return self.cur.fetchall()
    def select_benutzername(self,benutzername):
        sql = "SELECT COUNT(*) FROM kunden WHERE benutzername = '{}' ".format(benutzername)
        self.cur.execute(sql)
        return self.cur.fetchall()
    def select_mail(self,kunden_id,date):
        sql = "SELECT kunden.`email` FROM kunden JOIN kundenevents ON kunden.id=kundenevents.kID JOIN eventsentry on eventsentry.id = kundenevents.eID WHERE kunden.id != {} and eventsentry.datum >='{}'and eventsentry.id IN(SELECT eventsentry.id FROM eventsentry JOIN kundenevents ON eventsentry.id=kundenevents.eID JOIN kunden on kunden.id = kundenevents.kID WHERE kunden.id = {} and eventsentry.datum >='{}')".format(kunden_id[0][0],date,kunden_id[0][0],date)  
        self.cur.execute(sql)

        return self.cur.fetchall()  
    def select_user_email(self, kunden_id):
        sql = "SELECT `email` FROM kunden WHERE id = {}".format(kunden_id)
        self.cur.execute(sql)
        return self.cur.fetchall() 
    def update_pswd(self, pswd,email):
        sql = "UPDATE `kunden` SET `passwort`='{}' WHERE `email` = '{}'".format(pswd,email)
        self.cur.execute(sql)
        self.mydb.commit()
    def close(self):#die Verbindung zur DB wird getrennt
        self.cur.close()
        self.mydb.close()
    def eventinsert(self, name, datum, zeit):#Neues Event anlegen
        sql = "INSERT INTO `eventsentry`(`name`, `datum`, `zeit`) VALUES ('{}', '{}', '{}')".format(name, datum, zeit)
        self.cur.execute(sql)
        self.mydb.commit()
    
    def eventoutput(self, name):
        sql = "SELECT * FROM `eventsentry` WHERE `eventsentry`.`name` = '{}'".format(name)
        self.cur.execute(sql)
        return self.cur.fetchall()
    def eventout(self):
        sql = "SELECT * FROM `eventsentry`"
        self.cur.execute(sql)
        return self.cur.fetchall()
    def verlauf(self,kunden_id):
        print(kunden_id)
        sql = "SELECT * FROM eventsentry WHERE id IN (SELECT eID FROM kundenevents WHERE kID = {})".format(kunden_id[0][0])
        self.cur.execute(sql)
        return self.cur.fetchall()

class Backend:#Hier passiert alles was im hintergrund der Webseite
    def __init__(self):
        self.db = DB('root','root','localhost','8889','coronatracking')#hier kann ich die Klasse DB verwenden bzw. hier wird sie aufgerufen
        self.id = None
    def anmelden(self,benutzername_email,pswt):#anmelde funktion

        fehlerfrei = "ok"
        
        benutzername_email = benutzername_email.strip()#Leerzeichen werden am Anfang und am Ende entfernt
        self.db.connect()#Verbindung zur DB wird erstellt
        pswd_sql = self.db.select_pswd(benutzername_email)#das Passwort was zum Benutzername/E-Mail passt was in der DB gespeichert wurde wird hier zurückgegeben

        if len(pswd_sql) != 0:
            encoded_pswd = pswd_sql[0][0].encode('ascii')
            encoded_byte = base64.b64decode(encoded_pswd)
            pswd = encoded_byte.decode('ascii')
            if pswt != pswd:#hier wird geschaut ob das Passwort im Eingabefeld das gleiche Passwort ist wie in der DB. Stimmt es nicht kommt eine Fehlermeldung.
                fehler_medlung = "Fehler! Benutzername/E-Mail oder Passwort stimmt nicht."
                fehlerfrei = ""
                return fehler_medlung
                
            
            if fehlerfrei == 'ok':
                print('benutz:',benutzername_email)
                print(pswd)
                self.id = self.db.select_id(benutzername_email,pswd_sql[0][0])
                print('anmelden',self.id)
                self.db.close()#Verbindung zur DB wird getrennt
        else:
            fehler_medlung = "Fehler! Benutzername/E-Mail oder Passwort stimmt nicht."
            fehlerfrei = ""
            return fehler_medlung
            
       

    def neu(self, benutzername,pswt,pswt_w,vorname,nachname,email):

        fehlerfrei = "ok"
       


        benutzername = benutzername.strip()#Leerzeichen werden am Anfang und am Ende entfernt
        vorname = vorname.strip()#Leerzeichen werden am Anfang und am Ende entfernt
        nachname = nachname.strip()#Leerzeichen werden am Anfang und am Ende entfernt

        p_email = "^([a-zA-Z0-9]+([-_\.]?[a-zA-Z0-9])+@[a-zA-Z0-9]+([-_\.]?[a-zA-Z0-9])+\.[a-z]{2,4}){0,}$"
        p_name = "^[a-zA-ZäüöÄÜÖ]+$"
        p_pswd = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$"

        self.db.connect()#verbindung zur DB wird erstellt
        exist_benutzername = self.db.select_benutzername(benutzername)
        exist_benutzername = exist_benutzername[0][0]
        if exist_benutzername !=0:
            #print('Dieser Benutzername exestiert schon')
            fehlerfrei = ""
            return "Dieser Benutzername exestiert schon"

        if pswt != pswt_w:#Hier wird geschaut ob in den Passwortfelder das gleiche drinnen steht, wenn nicht kommt eine Fehlermeldung
            fehler_medlung = "Fehler! Passwortfelder stimmen nicht überein."
            fehlerfrei = ""
            #print(fehler_medlung)
            return fehler_medlung
        if not re.search(p_pswd,pswt):  
            fehlerfrei = ""
            #print('Keine gültiges Passwort! min. 6 Zeichen lang,min. 1 Großbuchstaben, min. 1 Kleinbuchstaben und min. 1 Ziffer enthalten.')
            return 'Keine gültiges Passwort! min. 6 Zeichen lang,min. 1 Großbuchstaben, min. 1 Kleinbuchstaben und min. 1 Ziffer enthalten.'
            
        # geburtsdatum = datetime.datetime.strptime(geburtsdatum, '%Y-%m-%d')#wird zum type datetime conventiert
        # if geburtsdatum > datetime.datetime.today():#schaut ob du schon geboren wurdest, wenn nicht fehler meldung
        #     print('Geburtsdatum stimmt nicht!')
        if not re.search(p_name,vorname):  
           
            fehlerfrei = ""
            #print('Kein gültiger Vorname. Es sind nur Buchstaben erlaubt.')
            return 'Kein gültiger Vorname. Es sind nur Buchstaben erlaubt.'
        if not re.search(p_name,nachname):  
            
            fehlerfrei = ""
            #print('Kein gültiger Nachname. Es sind nur Buchstaben erlaubt.')
            return 'Kein gültiger Nachname. Es sind nur Buchstaben erlaubt.'
        if not re.search(p_email,email):  
           
            fehlerfrei = ""
            #print('Keine gültige Email Adresse')
            return 'Keine gültige Email Adresse'

       
        
        if fehlerfrei == 'ok':

            pswd_byte = pswt.encode('ascii')
            encoded_byte = base64.b64encode(pswd_byte)
            encoded_pswd = encoded_byte.decode('ascii')


            self.db.insert_kunde(benutzername,encoded_pswd,vorname,nachname,email)#neues Konot wird erstellt

            self.db.close()#Verbindung zur DB wird getrentt






        
    def kunde_id(self,benutzername_email,pswt):
        self.db.connect()#Verbindung zur DB wird erstellt
        self.id = self.db.select_id(benutzername_email,pswt)
        self.id = self.id[0][0]
        self.db.close()#Verbindung zur DB wird getrent
    
    def kundenevent(self):#Verlauf erstellen
        self.db.connect()#Verbindung zur DB wird erstellt

        #SQL-State wo ich die ID vom Event bekomme was ich auswähle

        print(self.id)
        events = self.db.verlauf(self.id)

        self.db.close()#Verbindung zur DB wird getrent
        return events
    def mail(self):
        user = 'alisa6rieger@gmail.com'
        pwd = 'spuzunwyyivbpnbe'
        mail_text = 'Es gab einen Coronafall!'
        subject = 'Warnung!'

        #emails sind alle Emails von den Usern, ausgenommen der die Meldung sendete, die auch bei den Events waren wo auch der erkrankte User 3 Tage vor dem 1 Syntom tag war
        heute = datetime.date.today()
        tage = datetime.timedelta(days=3)

        date = heute-tage
        self.db.connect()
        emails = []
        for i in self.db.select_mail(self.id,date):
            for e in i:
                emails.append(e)
        self.db.close()

        FROM = user
        # to  = ", ".join(emails)
        # print('to: ',to)
        # DATA = 'From:{}\nTo:{}\nSubject:{}\n\n{}'.format(FROM, to, subject, mail_text)
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user, pwd)
        # server.sendmail(FROM, to, DATA)
        


        header = 'To:' + ", ".join(emails) + '\n' + 'From: ' + FROM + '\n' + 'Subject: ' + subject + '\n'
        msg = header + '\n' + mail_text + '\n\n'
        server.sendmail(FROM, emails, msg)
        server.quit()
        server.close()

        #Die verbindung wird geschlossen
        server.close()
    def passwort_email(self,email):
        user = 'alisa6rieger@gmail.com'
        pwd = 'spuzunwyyivbpnbe'
        subject = 'Verifizierungs Email'

        #eindeutige Nummer für die Passwort zurücksetzung wird erstellt.
        #im ergebnis steht die eindeutige nummer die als inhalt der email geschickt wird
        mail_text = ""
        for x in range(5):
            mail_text += str(random.randint(1,9))

        MAIL_FROM = user
        self.db.connect()
        #email = self.db.select_user_email(self.id)
        self.db.close()
        RCPT_TO  = email#[0][0]#email ist die Email vom User der das Passwort ändern möchte. Diese Information bekomme ich aus der DB
        DATA = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (MAIL_FROM, RCPT_TO, subject, mail_text)
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user, pwd)
        server.sendmail(MAIL_FROM, RCPT_TO, DATA)
        server.quit()
        #Die verbindung wird geschlossen
        server.close()
        fehlerfrei = "ok"
        #ein SQL-State wo das Passwort geändert wird
        code = input('Code: ')#request.POST.get('name_eingabefeld')
        if code == mail_text:
            pswt = input('neues Passwort: ')#Eingabefeld vom Passwort #request.POST.get('name_eingabefeld')
            pswt_w = input('neues Passwort wiederholen: ')#Eingabefeld vom Passwort wiederholen     #request.POST.get('name_eingabefeld')
            p_pswd = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$"

            if pswt != pswt_w:#Hier wird geschaut ob in den Passwortfelder das gleiche drinnen steht, wenn nicht kommt eine Fehlermeldung
                    fehler_medlung = "Fehler! Passwortfelder stimmen nicht überein."
                    fehlerfrei = ""
                    print(fehler_medlung)
            if not re.search(p_pswd,pswt):  
                print('Keine gültiges Passwort! min. 6 Zeichen lang,min. 1 Großbuchstaben, min. 1 Kleinbuchstaben und min. 1 Ziffer enthalten.')
                fehlerfrei = ""
            if fehlerfrei == 'ok':
                self.db.connect()
                self.db.update_pswd(pswt,email)
                self.db.close()
                print('Passwort wurde zurückgesetzt')
        else:
            print('Code ist falsch und kann man jetzt nicht mehr verwenden')

    def evinput(self, name, datum, zeit):
        
        if datum != None:
            #Checkt ob das Datum richtig formatiert ist, falls nicht, wird es korregiert. (YYYY-MM-DD)
            for i in datum:
                if i == "/" or i == ".":
                    datum = datum.replace(i, "-")

            #Checkt, ob das Datum im "date"-Format der MySQL Datenbank geschrieben wurde.
            date_p = "^\d{4}(?P<sep>[\/.-])\d{2}(?P=sep)(\d{2})$"
            date = re.match(date_p, datum)
                
            #Falls alle Daten nicht None sind, wird das Event hinzugefügt.
            if date != None and name != None and zeit != None:
                self.db.connect()
                self.db.eventinsert(name, datum, zeit)
                self.db.close()
                
            else:
                fehler = "Die Eingabe ist unvollständig!"
                return fehler
                #Popup Fenster das sagt: "Daten Fehlen", am besten so, dass angegeben wird, was genau fehlt.


    #Funktion um Events aus der Datenbank zu holen.
    def evoutput(self, name):
        
        if name != None:
            self.db.connect()
            out = self.db.eventoutput(name)
            output = []
            for i in out[0]:
                output.append(str(i))
            print(output)
            self.db.close()
    def event(self):
        self.db.connect()
        out = self.db.eventout()
        output = []
        for i in out:
            output.append(i)
        self.db.close()
        return output
    def logout(self):
        self.id = None




surface = Tk()
Website = GUI(surface)
Website.login()



