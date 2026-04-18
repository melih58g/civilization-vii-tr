# 🎮 Civilization VII - Türkçe Dil Paketi

<p align="center">
  <img src="https://img.shields.io/badge/Çeviri_Oranı-%2595-brightgreen?style=for-the-badge" alt="Çeviri Oranı">
  <img src="https://img.shields.io/badge/Oyun_Sürümü-1.3.2-blue?style=for-the-badge" alt="Oyun Sürümü">
  <img src="https://img.shields.io/badge/Paket_Sürümü-2.0.0-orange?style=for-the-badge" alt="Paket Sürümü">
  <img src="https://img.shields.io/github/downloads/melih58g/civilization-vii-tr/total?style=for-the-badge&label=İndirme&color=purple" alt="İndirme">
</p>

Sid Meier's Civilization VII için topluluk tarafından hazırlanan Türkçe çeviri paketi. Base oyun ve 28 DLC içeriğini kapsar.

## 🖥️ Desteklenen Platformlar

| Platform | Durum | Oyun Yolu (Varsayılan) |
|----------|-------|------------------------|
| **Steam** | ✅ Destekleniyor | `Steam\steamapps\common\Sid Meier's Civilization VII` |
| **Epic Games** | ✅ Destekleniyor | `Epic Games\CivilizationVII` |
| **Xbox (PC Game Pass)** | ✅ Destekleniyor | `XboxGames\Sid Meier's Civilization VII\Content` |
| **Microsoft Store** | ✅ Destekleniyor | Otomatik tespit |
| **Manuel Kurulum** | ✅ Destekleniyor | Herhangi bir yol |

> Kurulum programı oyun yolunu otomatik olarak tespit eder. Bulamazsa manuel olarak seçebilirsiniz.

## 📥 Kurulum

### Yöntem 1: EXE ile Kurulum (Python gerektirmez — Önerilen)
1. [Releases](https://github.com/melih58g/civilization-vii-tr/releases/latest) sayfasından **Civ7_Turkce_Kurulum.exe** ve **Civ7_Turkce_v2.0.0.zip** dosyalarını indirin
2. ZIP dosyasını bir klasöre çıkartın
3. **Civ7_Turkce_Kurulum.exe** dosyasını çıkarttığınız klasöre kopyalayın (`out` klasörünün yanına)
4. EXE'yi çalıştırın, oyun klasörünüzü doğrulayın
5. **KURULUM** butonuna tıklayın
6. Oyunu açıp **Ayarlar > Dil > Türkçe** seçin

### Yöntem 2: Python ile Kurulum
1. [Python 3.10+](https://www.python.org/downloads/) indirip kurun
   - Kurulumda **"Add Python to PATH"** kutucuğunu mutlaka işaretleyin
2. ZIP dosyasını çıkartın ve komut satırında:
   ```
   python setup.py
   ```

### Yöntem 3: Manuel Kurulum (Hiçbir şey gerektirmez)
ZIP içindeki `out` klasörünün içeriğini doğrudan oyun klasörünüze kopyalayın:
```
out\Base\...  →  [Oyun Klasörü]\Base\...
out\DLC\...   →  [Oyun Klasörü]\DLC\...
```

## 🔄 Geri Alma

- **EXE/Python kurulumu yaptıysanız:** Kurulum programındaki **Geri Al** butonunu kullanın
- **Manuel kurulum yaptıysanız:**
  - **Steam:** Oyuna sağ tık → Özellikler → Yerel Dosyalar → Dosya Bütünlüğünü Doğrula
  - **Epic:** Kütüphane → Oyuna tık → ⋯ → Doğrula
  - **Xbox:** Ayarlar → Uygulamalar → Oyunu Onar

## 📁 Dosya Yapısı
```
├── out/                    # Çeviri dosyaları
│   ├── Base/               # Ana oyun (5 modül + yapılandırma)
│   └── DLC/                # 28 DLC çevirisi
├── setup.py                # GUI kurulum programı
├── build_exe.py            # EXE derleme scripti
├── LICENSE
└── README.md
```

## 📊 İçerik Detayı

| Kategori | Dosya Sayısı | Açıklama |
|----------|-------------|----------|
| Çeviri (XML) | ~33 | Tüm oyun metinleri |
| Altyazı (VTT) | ~340 | Lider konuşmaları, sinematikler |
| Yapılandırma | ~10 | Dil tanımları, modinfo |
| **Toplam** | **~383** | Base + 28 DLC |

## ⚠️ Antivirüs Uyarısı

EXE dosyası Nuitka ile derlenmiştir ve imzasız olduğu için bazı antivirüs programları yanlış alarm (false positive) verebilir. Kaynak kodu tamamen açıktır.

**Windows Defender uyarısı alırsanız:** Daha fazla bilgi → Yine de çalıştır

<details>
<summary>İmzasız ne demek? Neden imzasız?</summary>

Büyük yazılım şirketleri, programlarının güvenilir olduğunu kanıtlamak için "kod imzalama sertifikası" (code signing certificate) kullanır. Bu sertifika, bir sertifika otoritesinden (CA) yıllık 200-400$ ödenerek alınır ve programın kim tarafından yapıldığını doğrular.

Bu proje bireysel bir topluluk çalışmasıdır ve yapay zeka destekli araçlarla kodlanmıştır. Herhangi bir şirket veya kuruluş tarafından desteklenmediği için kod imzalama sertifikası maliyeti karşılanamamaktadır.

İmzasız olması programın zararlı olduğu anlamına gelmez — sadece Windows'un "bu programı tanımıyorum" demesidir. Kaynak kodumuz tamamen açıktır, `setup.py` dosyasını inceleyerek programın ne yaptığını satır satır görebilirsiniz. İmza sahibi olmak istemiyorsanız, Python ile doğrudan `setup.py` dosyasını çalıştırabilir veya manuel kurulum yapabilirsiniz.
</details>

## 🤝 Katkıda Bulunma

- Çeviri hataları için [Issues](https://github.com/melih58g/civilization-vii-tr/issues) açın
- Düzeltme göndermek için Pull Request oluşturun

## 📜 Lisans

MIT License — Özgürce kullanabilir, değiştirebilir ve dağıtabilirsiniz.
