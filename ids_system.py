# ids_system.py
import threading
import time
from flask import Flask, render_template, jsonify
import smtplib
from email.message import EmailMessage
import psutil

app = Flask(__name__)

# Global variables to store metrics
cpu_usage = []
memory_usage = []
anomalies = []

# Global flag to stop threads
stop_threads = False

class SystemSentinelAgent(threading.Thread):
    def __init__(self):
        super().__init__()
        self.model = AnomalyDetectionModel()
        self.last_alert_time = 0

    def run(self):
        while not stop_threads:
            data = self.collect_data()  # Collects real data here
            if self.model.predict(data):
                current_time = time.time()
                if current_time - self.last_alert_time > 60:
                    self.alert_admin("Potential threat detected!")
                    anomalies.append(f"Potential threat detected at {time.ctime()}")
                    self.last_alert_time = current_time
            time.sleep(1)

    def collect_data(self):
        # Collect CPU and memory usage data
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        cpu_usage.append(cpu)
        memory_usage.append(memory)
        if len(cpu_usage) > 100:
            cpu_usage.pop(0)
        if len(memory_usage) > 100:
            memory_usage.pop(0)
        return {'cpu': cpu, 'memory': memory}

    def alert_admin(self, message):
        print(message)
        send_email(message)

def send_email(message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "radhanishant5647@gmail.com"
    receiver_email = "nambiarvinay89@gmail.com"
    app_password = "nzsqvwuilthabxaj"  # Use the App Password generated

    email = EmailMessage()
    email.set_content(message)
    email['Subject'] = 'IDS Alert'
    email['From'] = sender_email
    email['To'] = receiver_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(email)
        print("Email alert sent successfully!")
    except Exception as e:
        print("Failed to send email alert:", e)
    finally:
        server.quit()

class SystemFaultEvaluationAgent(threading.Thread):
    def run(self):
        while not stop_threads:
            self.analyze_data()
            time.sleep(2)

    def analyze_data(self):
        print("Analyzing system data...")

class SystemReplicationAgent(threading.Thread):
    def run(self):
        while not stop_threads:
            self.manage_replication()
            time.sleep(3)

    def manage_replication(self):
        print("Managing replication and recovery...")

class ProfileDatabase:
    def update_database(self, data):
        print("Updating profile database with new data.")

class LSIA:
    def start_agents(self):
        print("Starting all agents...")
        agents = [SystemSentinelAgent(), SystemFaultEvaluationAgent(), SystemReplicationAgent()]
        for agent in agents:
            agent.start()

    def stop_agents(self):
        global stop_threads
        stop_threads = True
        print("Stopping all agents...")

class AnomalyDetectionModel:
    def predict(self, data):
        cpu_threshold = 4.0
        memory_threshold = 70.0
        if data['cpu'] > cpu_threshold or data['memory'] > memory_threshold:
            return True
        return False

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/metrics')
def metrics():
    anomaly = anomalies.pop(0) if anomalies else None
    return jsonify({
        'cpu': cpu_usage[-1] if cpu_usage else 0,
        'memory': memory_usage[-1] if memory_usage else 0,
        'anomaly': anomaly
    })

def main():
    lsia = LSIA()
    lsia.start_agents()
    
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        lsia.stop_agents()

if __name__ == "__main__":
    main()