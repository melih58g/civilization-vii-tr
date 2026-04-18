#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Civilization VII Türkçe Dil Paketi - EXE Derleme Scripti

Bu script setup.py'yi tek bir .exe dosyasına derler.
Nuitka kullanır — PyInstaller'a göre çok daha az false positive üretir.

Kullanım:
    python build_exe.py

Gereksinimler:
    pip install nuitka

Not: İlk derleme biraz uzun sürebilir (C derleyici indirmesi).
     Nuitka otomatik olarak MinGW64 C derleyicisini indirir.
"""

import os
import sys
import subprocess
import shutil


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    setup_py = os.path.join(script_dir, "setup.py")
    dist_dir = os.path.join(script_dir, "dist")
    icon_path = os.path.join(script_dir, "..", "icon.ico")

    if not os.path.isfile(icon_path):
        icon_path = os.path.join(script_dir, "icon.ico")

    print("=" * 55)
    print("  Civilization VII - Türkçe Dil Paketi EXE Builder")
    print("=" * 55)
    print()

    # Nuitka kontrolü
    try:
        subprocess.run([sys.executable, "-m", "nuitka", "--version"],
                       capture_output=True, check=True)
        print("[OK] Nuitka bulundu.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[!] Nuitka bulunamadı. Kuruluyor...")
        subprocess.run([sys.executable, "-m", "pip", "install", "nuitka", "ordered-set"],
                       check=True)
        print("[OK] Nuitka kuruldu.")

    print()
    print("Derleme başlıyor... (ilk seferde 3-5 dakika sürebilir)")
    print()

    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=tk-inter",
        "--windows-console-mode=disable",
        f"--output-dir={dist_dir}",
        "--output-filename=Civ7_Turkce_Kurulum.exe",
        "--company-name=Civ7 TR Çeviri Topluluğu",
        "--product-name=Civilization VII Türkçe Dil Paketi",
        f"--product-version={get_version()}",
        f"--file-version={get_version()}",
        "--file-description=Civilization VII Türkçe Dil Paketi Kurulum Programı",
        "--copyright=Civ7 TR Çeviri Topluluğu © 2025-2026",
        "--assume-yes-for-downloads",
    ]

    if os.path.isfile(icon_path):
        cmd.append(f"--windows-icon-from-ico={icon_path}")
        print(f"[OK] İkon: {icon_path}")

    cmd.append(setup_py)

    print(f"[>>] Komut: {' '.join(cmd[:5])}...")
    print()

    result = subprocess.run(cmd, cwd=script_dir)

    if result.returncode == 0:
        exe_path = os.path.join(dist_dir, "Civ7_Turkce_Kurulum.exe")
        if os.path.isfile(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print()
            print("=" * 55)
            print(f"  BAŞARILI! EXE oluşturuldu.")
            print(f"  Konum: {exe_path}")
            print(f"  Boyut: {size_mb:.1f} MB")
            print("=" * 55)
            print()
            print("ÖNEMLİ: Dağıtım için 'dist' klasörünün içine")
            print("'out' klasörünü de kopyalamanız gerekir.")
            print()
            print("Dağıtım yapısı:")
            print("  Civ7_Turkce_Kurulum.exe")
            print("  out/")
            print("    Base/...")
            print("    DLC/...")
        else:
            print("[!] EXE dosyası bulunamadı.")
    else:
        print()
        print("[HATA] Derleme başarısız oldu!")
        print("Hata kodu:", result.returncode)

    # Alternatif: PyInstaller ile de derleme seçeneği
    print()
    print("-" * 55)
    print("Alternatif: PyInstaller ile derlemek isterseniz:")
    print("  pip install pyinstaller")
    print('  pyinstaller --onefile --windowed --name="Civ7_Turkce_Kurulum" setup.py')
    print()
    print("NOT: Nuitka, PyInstaller'a göre antivirüs false positive")
    print("oranını önemli ölçüde azaltır.")


def get_version():
    """setup.py'den sürüm bilgisini al."""
    try:
        with open(os.path.join(os.path.dirname(__file__), "setup.py"), "r", encoding="utf-8") as f:
            for line in f:
                if "APP_VERSION" in line and "=" in line:
                    return line.split('"')[1]
    except Exception:
        pass
    return "2.0.0"


if __name__ == "__main__":
    main()
