from flask import Flask, request, render_template
from collections import defaultdict

from utils.detector import detect
from utils.notifier import send_email
from utils.blocker import is_blocked, block_ip
from utils.ip_tracker import get_ip_info
from utils.predictor import predict_next

app = Flask(__name__)

ip_requests = defaultdict(int)
history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/email')
def email_page():
    return render_template('email.html')

@app.route('/scan', methods=['POST'])
def scan():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_email = request.form.get('email')

    if is_blocked(ip):
        return "🚫 You are blocked"

    ip_requests[ip] += 1
    count = ip_requests[ip]

    decision = detect(count)
    info = get_ip_info(ip)
    prediction = predict_next(count)

    if decision == "BLOCK":
        block_ip(ip)

    try:
        send_email(user_email, ip, decision)
    except:
        print("Email failed")

    history.append({
        "ip": ip,
        "count": count,
        "decision": decision,
        "country": info["country"],
        "city": info["city"],
        "prediction": prediction
    })

    return render_template('result.html',
                           ip=ip,
                           count=count,
                           decision=decision,
                           info=info,
                           prediction=prediction)

@app.route('/dashboard')
def dashboard():
    safe = len([h for h in history if h["decision"] == "SAFE"])
    alert = len([h for h in history if h["decision"] == "ALERT"])
    block = len([h for h in history if h["decision"] == "BLOCK"])

    return render_template('dashboard.html',
                           history=history,
                           safe=safe,
                           alert=alert,
                           block=block)

if __name__ == "__main__":
    app.run(debug=True)
