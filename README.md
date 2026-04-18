# 🎮 Civilization VII - Türkçe Dil Paketi

Sid Meier's Civilization VII için topluluk tarafından hazırlanan Türkçe çeviri paketi.

## 📊 Durum

| Bilgi | Detay |
|-------|-------|
| **Çeviri Oranı** | %95 |
| **Oyun Sürümü** | 1.3.2 (Build 1217315 - 25.02.2026) |
| **Paket Sürümü** | 2.0.0 |
| **İçerik** | Base oyun + 28 DLC |

## 📥 Kurulum

### Yöntem 1: İndir ve Kur (Önerilen)
1. [Releases](https://github.com/melih58g/civilization-vii-tr/releases) sayfasından **Civ7_Turkce_v2.0.0.zip** dosyasını indirin
2. ZIP dosyasını bir klasöre çıkartın
3. `setup.py` dosyasını çalıştırın (Python gerekli, aşağıya bakın)
4. Oyun klasörünüzü doğrulayın (varsayılan: `C:\Games\Civilization VII`)
5. **KURULUM** butonuna tıklayın
6. Oyunu açıp **Ayarlar > Dil > Türkçe** seçin

### Yöntem 2: Manuel Kurulum (Python gerektirmez)
ZIP içindeki `out` klasörünün içeriğini doğrudan oyun klasörünüze kopyalayın:
```
out\Base\...  →  C:\Games\Civilization VII\Base\...
out\DLC\...   →  C:\Games\Civilization VII\DLC\...
```

## 🐍 Python Kurulumu (setup.py için gerekli)

Setup programını kullanmak için Python 3.10 veya üzeri gereklidir.

1. **Python indirin:** [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Kurulum sırasında **"Add Python to PATH"** kutucuğunu mutlaka işaretleyin
3. Kurulumu tamamlayın
4. Komut satırında doğrulayın:
   ```
   python --version
   ```

> **Not:** Python kurmak istemiyorsanız Yöntem 2 (Manuel Kurulum) ile Python'a ihtiyaç duymadan kurulum yapabilirsiniz.

## 🔄 Geri Alma
Kurulum programındaki **Geri Al** butonunu kullanın. Tüm dosyalar otomatik olarak yedekten geri yüklenir.

Manuel kurulum yaptıysanız, oyunu Steam/Epic üzerinden "Dosya Bütünlüğünü Doğrula" seçeneği ile onarabilirsiniz.

## 📁 Dosya Yapısı
```
├── out/                    # Çeviri dosyaları (oyuna kopyalanacak)
│   ├── Base/               # Ana oyun çevirileri
│   │   ├── Assets/         # Dil yapılandırması (Languages.json, SQL)
│   │   └── modules/        # Modül çevirileri (core, age-*, base-standard)
│   └── DLC/                # DLC çevirileri (28 DLC)
├── setup.py                # GUI kurulum programı
├── build_exe.py            # EXE derleme scripti
├── LICENSE
└── README.md
```

## ⚠️ Antivirüs Uyarısı
EXE olarak derlenmiş sürüm kullanıyorsanız, imzasız olduğu için bazı antivirüs programları yanlış alarm verebilir. Kaynak kodu açıktır, güvenle kullanabilirsiniz.

Windows Defender uyarısı alırsanız: **Daha fazla bilgi** → **Yine de çalıştır**

## 🤝 Katkıda Bulunma
Çeviri hataları veya öneriler için [Issues](https://github.com/melih58g/civilization-vii-tr/issues) sayfasını kullanabilirsiniz.

## 📜 Lisans
MIT License
