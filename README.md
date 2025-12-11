# Neon Russian Typing Defender — PC Build

Pygame tabanlı bir Rusça kelime yazma/atış oyunu. Şu an **sadece masaüstü (Windows/macOS/Linux) için** tasarlandı; web veya mobil paketleme yoktur. Proje geliştirme aşamasındadır.

## Gereksinimler
- Python 3.10+ (3.12 ile test edildi)
- `pip`
- Bağımlılıklar: `pygame` (requirements.txt içinde)

## Kurulum ve Çalıştırma (Windows için örnek)
```powershell
cd C:\Users\yahya\spacegame
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
macOS/Linux için `source .venv/bin/activate` kullanın.

## Oynanış / Kontroller
- Düşen kelimeler: Ekranın üstünden düşer, yazdıkça ilerler.
- Yazma: Klavyeden doğru harfleri girerek kelimeyi tamamlayın.
- Ateş: `Space` veya sol tık, ekrandaki ilk kelimeye mermi yollar.
- Çıkış: `Esc`.
- Skor: Kelime tamamlandıkça puan eklenir; patlama efekti gösterilir.

## Durum
- Geliştirme aşamasında: Dalga geçişleri, menüler ve denge ayarları henüz basit. Şu an PC’de çalışır, mobil/web paketleme yapılmıyor.

## Sorun Giderme
- Pencere açılmazsa veya ses/görüntü sorunları varsa `pygame`’i yeniden kurun: `pip install --upgrade pygame`.
- Siyah ekran veya kelime yoksa konsoldaki hata mesajlarını kontrol edin; eksik bağımlılık veya Python sürümü uyumsuz olabilir.
