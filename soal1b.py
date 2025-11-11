#include <DHT.h>  // Library sensor DHT

#define DHTPIN 8
#define DHTTYPE DHT22  // Ganti ke DHT22 jika pakai DHT22

// Inisialisasi objek DHT
DHT dht(DHTPIN, DHTTYPE);

// Definisi pin komponen
#define LED_HIJAU 5 
#define LED_KUNING 10
#define LED_MERAH 12
#define RELAY_POMPA 7
#define BUZZER 9

void setup() {
  Serial.begin(9600);
  dht.begin();

  // Set semua pin sebagai output
  pinMode(LED_HIJAU, OUTPUT);
  pinMode(LED_KUNING, OUTPUT);
  pinMode(LED_MERAH, OUTPUT);
  pinMode(RELAY_POMPA, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  // Pastikan semua komponen mati saat awal
  digitalWrite(LED_HIJAU, LOW);
  digitalWrite(LED_KUNING, LOW);
  digitalWrite(LED_MERAH, LOW);
  digitalWrite(RELAY_POMPA, LOW);
  digitalWrite(BUZZER, LOW);
}

void loop() {
  // Baca data suhu dan kelembapan dari sensor DHT
  float suhu = dht.readTemperature();
  float kelembapan = dht.readHumidity();

  // Pastikan data valid
  if (isnan(suhu) || isnan(kelembapan)) {
    Serial.println("Gagal membaca data dari sensor DHT!");
    delay(2000);
    return;
  }

  // Tampilkan hasil ke Serial Monitor
  Serial.print("Suhu: ");
  Serial.print(suhu);
  Serial.print(" °C  |  Kelembapan: ");
  Serial.print(kelembapan);
  Serial.println(" %");

  // Logika pengendalian suhu
  if (suhu > 35) {
    // Kondisi suhu tinggi
    digitalWrite(LED_MERAH, HIGH);
    digitalWrite(LED_KUNING, LOW);
    digitalWrite(LED_HIJAU, LOW);

    digitalWrite(RELAY_POMPA, HIGH);  // Pompa menyala
    digitalWrite(BUZZER, HIGH);       // Buzzer menyala

    Serial.println("⚠️ SUHU TINGGI! LED MERAH & BUZZER ON, Pompa ON");
  } 
  else if (suhu >= 30 && suhu <= 35) {
    // Kondisi suhu sedang
    digitalWrite(LED_KUNING, HIGH);
    digitalWrite(LED_MERAH, LOW);
    digitalWrite(LED_HIJAU, LOW);

    digitalWrite(RELAY_POMPA, HIGH);  // Pompa tetap ON
    digitalWrite(BUZZER, LOW);

    Serial.println("🌤 SUHU SEDANG! LED KUNING ON, Pompa ON");
  } 
  else {
    // Kondisi suhu rendah
    digitalWrite(LED_HIJAU, HIGH);
    digitalWrite(LED_KUNING, LOW);
    digitalWrite(LED_MERAH, LOW);

    digitalWrite(RELAY_POMPA, LOW);   // Pompa mati
    digitalWrite(BUZZER, LOW);

    Serial.println("✅ SUHU RENDAH! LED HIJAU ON, Pompa OFF");
  }

  // Delay pembacaan
  delay(2000);
}