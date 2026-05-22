from flask import Flask, request, redirect, url_for

import smtplib

app = Flask(__name__)

# ---------------- LOGIN PAGE ----------------
@app.route("/", methods=["GET"])
def login():
    return '''
    <h2>🔐 Login</h2>
    <form action="/mail" method="get">
        <input name="email" placeholder="Your Gmail"><br><br>
        <input name="password" placeholder="App Password"><br><br>
        <button type="submit">Login</button>
    </form>
    '''

# ---------------- MAIL PAGE ----------------
@app.route("/mail", methods=["GET"])
def mail_page():
    email = request.args.get("email")
    password = request.args.get("password")

    return f'''
    <h2>📧 Bulk Mail Sender</h2>

    <form action="/send" method="post">
        <input type="hidden" name="email" value="{email}">
        <input type="hidden" name="password" value="{password}">

        <input name="to" placeholder="Emails (comma separated)" style="width:300px"><br><br>
        <input name="subject" placeholder="Subject" style="width:300px"><br><br>

        <textarea name="message" placeholder="Message" style="width:300px;height:120px"></textarea><br><br>

        <button type="submit">🚀 Send Bulk Mail</button>
    </form>
    '''

# ---------------- SEND MAIL ----------------
@app.route("/send", methods=["POST"])
def send():

    email = request.form["email"]
    password = request.form["password"]

    to_list = request.form["to"].split(",")
    subject = request.form["subject"]
    message = request.form["message"]

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)

    for to in to_list:
        to = to.strip()
        text = f"Subject: {subject}\n\n{message}"
        server.sendmail(email, to, text)

    server.quit()

    return "<h2>✅ All Emails Sent Successfully!</h2>"

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)