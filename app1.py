import requests
from flask import Flask,render_template,request
from twilio.rest import Client

account_id = "AC6b02d23e6ede4a766ab2ed96c022daa3"
auth_token = "06ee0477957cd446d8231792fbc93a67"
client = Client(account_id,auth_token)

app = Flask(__name__,static_url_path="/static")

@app.route("/")
def registration_form():
    return render_template("form.html")

@app.route("/registration_page",methods = ["POST","GET"])
def registration_details():
    name = request.form["name"]
    dest_state = request.form["state"]
    src_district = request.form["src_dist"]
    dest_district = request.form["dest_dist"]
    date = request.form["date"]
    phone = request.form["phno"]
    reason = request.form["reason"]
    r = requests.get("https://api.covid19india.org/v4/data.json")
    data = r.json()
    count = data[dest_state]["districts"][dest_district]["total"]["confirmed"]
    population = data[dest_state]["districts"][dest_district]["meta"]["population"]
    percent = (count/population)*100
    if(percent<30 and request.method=="POST"):
        status = "CONFIRMED"
        client.messages\
            .create(to="whatsapp:+91"+phone,
            from_ = "whatsapp:+14155238886",
            body = "Hello "+name+"! Your Travel From "+src_district+" to "+dest_district+" on "+date+" has been confirmed"
        )
        return render_template("registration_details.html",Name = name,Phone = phone,State = dest_state,Src_Dist = src_district,Dest_Dist = dest_district,Status = status,Date = date,Reason = reason)
    else:
        status = "DECLINED"
        client.messages.create(to="whatsapp:+91"+phone,
            from_ = "whatsapp:+14155238886",
            body = "Hello "+name+"! Your Travel From "+src_district+" to "+dest_district+" on "+date+" has been declined, Apply later"
        )
        return render_template("registration_details.html",Name = name,Phone = phone,State = dest_state,Src_Dist = src_district,Dest_Dist = dest_district,Status = status,Reason = reason)

if(__name__=="__main__"):
    app.run(port = 5000,debug = True)