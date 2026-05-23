from flask import Flask, request
import smtplib

app = Flask(__name__)

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return '''
    <html>

    <head>
        <title>Bulk Mail Dashboard</title>

        <style>

            body{
                background:#f4f4f4;
                font-family:Arial;
                padding:40px;
            }

            .box{
                background:white;
                max-width:600px;
                margin:auto;
                padding:30px;
                border-radius:10px;
                box-shadow:0px 0px 10px rgba(0,0,0,0.1);
            }

            h2{
                text-align:center;
            }

            input, textarea{
                width:100%;
                padding:12px;
                margin-top:10px;
                border:1px solid #ccc;
                border-radius:5px;
            }

            button{
                width:100%;
                padding:12px;
                margin-top:20px;
                background:#007bff;
                color:white;
                border:none;
                border-radius:5px;
                font-size:16px;
                cursor:pointer;
            }

            button:hover{
                background:#0056b3;
            }

        </style>

    </head>

    <body>

        <div class="box">

            <h2>📧 Bulk Mail Dashboard</h2>

            <form action="/send" method="post">

                <input type="text" name="name" placeholder="First Name">

                <input type="email" name="email" placeholder="Send From (Your Gmail)">

                <input type="password" name="password" placeholder="App Password">

                <input type="text" name="subject" placeholder="Subject">

                <textarea name="message" rows="8" placeholder="Body"></textarea>

                <textarea name="to" rows="5" placeholder="Mails (comma separated)"></textarea>

                <button type="submit">🚀 Send Emails</button>

            </form>

        </div>

    </body>

    </html>
    '''

# ---------------- SEND MAIL ----------------
@app.route("/send", methods=["POST"])
def send():

    try:

        email = request.form["email"]
        password = request.form["password"]

        subject = request.form["subject"]
        message = request.form["message"]

        to_list = request.form["to"].split(",")

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(email, password)

        for to in to_list:

            text = f"Subject: {subject}\n\n{message}"

            server.sendmail(email, to.strip(), text)

        server.quit()

        return """
        <script>

        alert("✅ Emails Sent Successfully");

        window.location.href="/";

        </script>
        """

    except Exception as e:

        return f"""
        <script>

        alert("❌ Failed To Send Mail\\n\\n{str(e)}");

        window.location.href="/";

        </script>
        """

# ---------------- RUN ----------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)