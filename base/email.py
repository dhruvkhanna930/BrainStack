

def resetPasswordMail(EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, TO_, OTP, USER):
    import smtplib as sm
    from email import encoders
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase

    try:
        smtpserver = sm.SMTP("smtp.gmail.com", EMAIL_PORT)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        from_ = EMAIL_HOST_USER
        message = MIMEMultipart("Alternative")
        message['Subject'] = "Password reset for BrainStack account"
        message["From"] = from_
        message["To"] = TO_

        html = f'''
            <div class="wrapper" style="margin: auto; margin-top: 3rem; width: 60%; border: 2px solid gray; background-color: aliceblue;">
                <h2 style="text-align: center;">Reset your BrainStack Password</h2>
                <div style="margin: auto; width: 80%;">
                    Dear User, <br>
                    Your user id is <span style="font-size: larger;"> {USER} </span> <br>
                    OTP in order to reset your password is <b style="font-size: x-large;">{OTP}</b>
                </div>
            </div>
        '''

        part2 = MIMEText(html, "html")
        message.attach(part2) 

        smtpserver.sendmail(from_, TO_, message.as_string())

        print("Successfully sent otp mail")

    except Exception as e:
        print(e)

if __name__ == '__main__':
    print("Hello")