from flask import Flask, jsonify, render_template
import mysql.connector
import json
import threading
import paho.mqtt.client as mqtt

# --- Setup Flask ---
app = Flask(__name__)

# --- Koneksi Database ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_cuaca"
)

# --- Fungsi untuk ambil data ---
@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_cuaca ORDER BY id DESC LIMIT 10")
    data = cursor.fetchall()
    return render_template('index.html', data=data)

@app.route('/api')
def api():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_cuaca ORDER BY id DESC LIMIT 10")
    data = cursor.fetchall()
    return jsonify(data)

# --- Callback MQTT ---
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        suhu = payload['suhu']
        humid = payload['humid']
        lux = payload['lux']

        sql = "INSERT INTO tb_cuaca (suhu, humid, lux) VALUES (%s, %s, %s)"
        cursor = db.cursor()
        cursor.execute(sql, (suhu, humid, lux))
        db.commit()
        print(f"✅ Data tersimpan: Suhu={suhu}, Humid={humid}, Lux={lux}")
    except Exception as e:
        print("❌ Error MQTT:", e)

# --- Fungsi Jalankan MQTT ---
def mqtt_listener():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("test.mosquitto.org", 1883, 60)
    client.subscribe("iot/db_cuaca")
    print("📡 MQTT Listener aktif...")
    client.loop_forever()

# --- Jalankan MQTT di thread terpisah ---
mqtt_thread = threading.Thread(target=mqtt_listener)
mqtt_thread.daemon = True
mqtt_thread.start()

# --- Jalankan Flask ---
if __name__ == '__main__':
    print("🚀 Flask & MQTT berjalan di http://127.0.0.1:5000")
    app.run(debug=True)