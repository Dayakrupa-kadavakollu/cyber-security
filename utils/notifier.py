import smtplib

SENDER = "kadavakolludayakrupa@gmail.com"
PASSWORD = "godndmldklryhval"

def send_email(to, ip, decision):
    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(SENDER,PASSWORD)

        msg = f"Subject: Alert\n\nIP:{ip}\nStatus:{decision}"

        server.sendmail(SENDER,to,msg)
        server.quit()

    except:
        print("Email error")
