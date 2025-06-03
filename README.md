# Hamming Code Simulator (Turkish)

Bu program, Hamming SEC-DED (Tek Hata Düzeltme, Çift Hata Tespit) kodunun simülasyonunu yapar. Program, veri iletiminde hataları tespit etme ve düzeltme için kullanılan Hamming kodunu görsel bir arayüzle gösterir.

## Özellikler

- 8, 16 veya 32 bitlik veri boyutları için Hamming kod oluşturma
- Tek, çift ve üçlü hata simülasyonu
- Otomatik hata ekleme
- Hata tespit ve düzeltme
- Görsel bit gösterimi
- Konsol çıktısı

## Kullanım

1. Programı çalıştırın:
```bash
python hamming_gui_turkish.py
```

2. Program arayüzünde:
   - "Veri Boyutu" seçeneğinden 8, 16 veya 32 bit seçin
   - "Hata Tipi" seçeneğinden hata tipini seçin (Tek Hata, Çift Hata veya Üçlü Hata)
   - "Orijinal Veri" kutusuna 0 ve 1'lerden oluşan veri girin
   - "Kodu Oluştur" butonuna tıklayın
   - "Rastgele Hata Ekle" butonuna tıklayın
   - "Kodu Çöz" butonuna tıklayın

## Arayüz Elemanları

- **Orijinal Veri**: 0 ve 1'lerden oluşan giriş verisi
- **Kodlanmış Veri**: Hamming kodu ile kodlanmış veri
- **Hatalı Veri**: Hata eklendiğinde oluşan veri
- **Çözülen Veri**: Hatalar düzeltildikten sonra elde edilen veri
- **Tespit Edilen Hata Pozisyonu**: Hatanın tespit edildiği pozisyon
- **Konsol Çıktısı**: Tüm işlemlerin detaylı kaydı

## Teknik Detaylar

- Hamming SEC-DED kodu, tek hataları düzeltme ve çift hataları tespit etme yeteneğine sahiptir
- Program otomatik olarak rastgele hata pozisyonları seçer
- Her düzeltme biti (P) belirli pozisyonlardaki bitleri kontrol eder
- Tek hatalar otomatik olarak düzeltilebilir
- Çift hatalar tespit edilebilir ancak düzeltilemez

## Örnek Kullanım

1. 8 bitlik veri girin (örn: "10101010")
2. "Tek Hata" seçin
3. "Kodu Oluştur" butonuna tıklayın
4. "Rastgele Hata Ekle" butonuna tıklayın
5. "Kodu Çöz" butonuna tıklayın

Bu işlem, Hamming kodunun nasıl çalıştığını gösterecektir.
