#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Civilization VII - Türkçe Dil Paketi Kurulum Programı
Profesyonel GUI kurulum aracı
"""

import os
import sys
import json
import shutil
import hashlib
import threading
import datetime
import traceback
from pathlib import Path
from typing import Optional, List, Dict, Tuple

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import winreg
except ImportError:
    winreg = None

# ─── Sabitler ────────────────────────────────────────────────────────────────
APP_VERSION = "2.0.0"
PATCH_VERSION = "%95"
MANIFEST_NAME = "install_manifest.json"
BACKUP_DIR_NAME = "backup_installer"
DEFAULT_GAME_PATH = r"C:\Games\Civilization VII"

# Çok dilli metin sistemi
TEXTS = {
    "tr": {
        "app_title": "Civilization VII - Türkçe Dil Paketi",
        "window_title": "Civilization VII - Türkçe Dil Paketi Kurulumu",
        "header_line1": "⚔  Civilization VII",
        "header_line2": "Türkçe Dil Paketi Kurulumu",
        "subtitle": "Sürüm {version}  •  Çeviri Oranı: {patch}  •  Civ7 TR Çeviri Topluluğu",
        "game_version": "Oyun Sürümü: {version}",
        "game_version_unknown": "Oyun Sürümü: Tespit edilemedi",
        "existing_install_warn": "⚠  Mevcut kurulum tespit edildi (v{version} - {date})",
        "path_card_title": "Oyun Klasörü",
        "path_card_desc": "Civilization VII'nin kurulu olduğu klasörü seçin veya doğrulayın",
        "browse_btn": "📁 Gözat",
        "path_not_set": "⚠ Oyun yolu belirtilmedi",
        "path_valid": "✓ Oyun klasörü doğrulandı",
        "path_invalid_nodir": "✗ Belirtilen klasör bulunamadı",
        "path_invalid_nobase": "✗ 'Base' klasörü bulunamadı — doğru klasörü seçin",
        "path_invalid_nomod": "✗ 'Base/modules' bulunamadı",
        "info_card_title": "Kurulum Bilgileri",
        "info_calculating": "Dosyalar hesaplanıyor...",
        "info_select_path": "Lütfen oyun klasörünü seçin.",
        "info_summary": "Toplam {total} dosya ({size})  •  {xml} çeviri  •  {vtt} altyazı  •  {other} yapılandırma",
        "info_no_out": "HATA: 'out' klasörü bulunamadı!",
        "btn_install": "⬇  KURULUM",
        "btn_uninstall": "↩  Geri Al",
        "btn_close": "Kapat",
        "status_ready": "Hazır",
        "status_backing_up": "Mevcut dosyalar yedekleniyor...",
        "status_installing": "Türkçe dosyalar kuruluyor...",
        "status_verifying": "Kurulum doğrulanıyor...",
        "status_done": "Kurulum tamamlandı!",
        "status_removing": "Kurulan dosyalar kaldırılıyor...",
        "status_restoring": "Orijinal dosyalar geri yükleniyor...",
        "status_uninstall_done": "Geri alma tamamlandı",
        "status_failed": "İşlem tamamlanamadı",
        "confirm_install_title": "Kurulumu Onayla",
        "confirm_install_msg": "Türkçe dil paketi şu konuma kurulacak:\n\n{path}\n\nMevcut dosyalar otomatik olarak yedeklenecektir.\nDevam etmek istiyor musunuz?",
        "confirm_overwrite_title": "Mevcut Kurulum",
        "confirm_overwrite_msg": "Daha önce yapılmış bir kurulum tespit edildi.\nYeni kurulum önceki yedeğin üzerine yazacaktır.\n\nDevam etmek istiyor musunuz?",
        "confirm_uninstall_title": "Geri Almayı Onayla",
        "confirm_uninstall_msg": "Türkçe dil paketi kaldırılacak ve\norijinal dosyalar geri yüklenecektir.\n\nDevam etmek istiyor musunuz?",
        "success_install_title": "Başarılı!",
        "success_install_msg": "Türkçe dil paketi başarıyla kuruldu!\n\nOyunu başlatıp Ayarlar > Dil menüsünden\nTürkçe'yi seçmeyi unutmayın.",
        "success_uninstall_title": "Başarılı",
        "success_uninstall_msg": "Türkçe dil paketi başarıyla kaldırıldı.\nOyun orijinal haline döndürüldü.",
        "warn_errors_title": "Uyarı",
        "warn_errors_msg": "İşlem sırasında bazı hatalar oluştu.\nDetaylar için log alanını kontrol edin.",
        "err_no_out": "'out' klasörü bulunamadı!\nÖnce çeviri dosyalarını oluşturun.",
        "err_no_manifest": "Geri alınacak kurulum bulunamadı.",
        "close_while_running_title": "Uyarı",
        "close_while_running_msg": "İşlem devam ediyor. Çıkmak istediğinize emin misiniz?",
        "log_auto_detect": "Oyun yolu otomatik tespit edildi: {path}",
        "log_prev_install": "Önceki kurulumdan oyun yolu alındı: {path}",
        "log_total_files": "Toplam {count} dosya kurulacak.",
        "log_backup_dir": "Yedek klasörü: {path}",
        "log_step_backup": "ADIM 1: Yedekleme başlıyor...",
        "log_step_copy": "ADIM 2: Dosyalar kopyalanıyor...",
        "log_step_verify": "ADIM 3: Kurulum doğrulanıyor...",
        "log_backed_up": "  {count} dosya yedeklendi.",
        "log_verified": "  {verified}/{total} dosya doğrulandı.",
        "log_complete_ok": "Kurulum başarıyla tamamlandı!",
        "log_complete_err": "Kurulum tamamlandı ({count} hata ile).",
        "log_installed": "  Kurulan: {count} dosya",
        "log_backed": "  Yedeklenen: {count} dosya",
        "log_verified_count": "  Doğrulanan: {count} dosya",
        "log_uninstall_start": "Geri alma işlemi başlıyor...",
        "log_step_remove": "ADIM 1: Kurulan dosyalar kaldırılıyor...",
        "log_step_restore": "ADIM 2: Orijinal dosyalar geri yükleniyor...",
        "log_removed": "  {count} dosya silindi.",
        "log_restored": "  {count} dosya geri yüklendi.",
        "log_uninstall_done": "Geri alma işlemi tamamlandı!",
        "log_cancelled": "İşlem iptal edildi!",
        "log_error": "HATA: {msg}",
        "log_no_manifest": "HATA: Kurulum manifest dosyası bulunamadı!",
        "lang_label": "Dil / Language:",
    },
    "en": {
        "app_title": "Civilization VII - Turkish Language Pack",
        "window_title": "Civilization VII - Turkish Language Pack Setup",
        "header_line1": "⚔  Civilization VII",
        "header_line2": "Turkish Language Pack Setup",
        "subtitle": "Version {version}  •  Translation: {patch}  •  Civ7 TR Translation Community",
        "game_version": "Game Version: {version}",
        "game_version_unknown": "Game Version: Could not detect",
        "existing_install_warn": "⚠  Existing installation detected (v{version} - {date})",
        "path_card_title": "Game Folder",
        "path_card_desc": "Select or verify the Civilization VII installation folder",
        "browse_btn": "📁 Browse",
        "path_not_set": "⚠ Game path not specified",
        "path_valid": "✓ Game folder verified",
        "path_invalid_nodir": "✗ Specified folder not found",
        "path_invalid_nobase": "✗ 'Base' folder not found — select the correct folder",
        "path_invalid_nomod": "✗ 'Base/modules' not found",
        "info_card_title": "Installation Info",
        "info_calculating": "Calculating files...",
        "info_select_path": "Please select the game folder.",
        "info_summary": "Total {total} files ({size})  •  {xml} translations  •  {vtt} subtitles  •  {other} config",
        "info_no_out": "ERROR: 'out' folder not found!",
        "btn_install": "⬇  INSTALL",
        "btn_uninstall": "↩  Uninstall",
        "btn_close": "Close",
        "status_ready": "Ready",
        "status_backing_up": "Backing up existing files...",
        "status_installing": "Installing Turkish files...",
        "status_verifying": "Verifying installation...",
        "status_done": "Installation complete!",
        "status_removing": "Removing installed files...",
        "status_restoring": "Restoring original files...",
        "status_uninstall_done": "Uninstall complete",
        "status_failed": "Operation failed",
        "confirm_install_title": "Confirm Installation",
        "confirm_install_msg": "Turkish language pack will be installed to:\n\n{path}\n\nExisting files will be backed up automatically.\nDo you want to continue?",
        "confirm_overwrite_title": "Existing Installation",
        "confirm_overwrite_msg": "A previous installation was detected.\nNew installation will overwrite the previous backup.\n\nDo you want to continue?",
        "confirm_uninstall_title": "Confirm Uninstall",
        "confirm_uninstall_msg": "Turkish language pack will be removed and\noriginal files will be restored.\n\nDo you want to continue?",
        "success_install_title": "Success!",
        "success_install_msg": "Turkish language pack installed successfully!\n\nLaunch the game and select Turkish\nfrom Settings > Language.",
        "success_uninstall_title": "Success",
        "success_uninstall_msg": "Turkish language pack removed successfully.\nGame restored to original state.",
        "warn_errors_title": "Warning",
        "warn_errors_msg": "Some errors occurred during the operation.\nCheck the log for details.",
        "err_no_out": "'out' folder not found!\nBuild translation files first.",
        "err_no_manifest": "No installation found to uninstall.",
        "close_while_running_title": "Warning",
        "close_while_running_msg": "Operation in progress. Are you sure you want to exit?",
        "log_auto_detect": "Game path auto-detected: {path}",
        "log_prev_install": "Game path from previous install: {path}",
        "log_total_files": "Total {count} files to install.",
        "log_backup_dir": "Backup folder: {path}",
        "log_step_backup": "STEP 1: Backing up...",
        "log_step_copy": "STEP 2: Copying files...",
        "log_step_verify": "STEP 3: Verifying...",
        "log_backed_up": "  {count} files backed up.",
        "log_verified": "  {verified}/{total} files verified.",
        "log_complete_ok": "Installation completed successfully!",
        "log_complete_err": "Installation completed with {count} error(s).",
        "log_installed": "  Installed: {count} files",
        "log_backed": "  Backed up: {count} files",
        "log_verified_count": "  Verified: {count} files",
        "log_uninstall_start": "Uninstall starting...",
        "log_step_remove": "STEP 1: Removing installed files...",
        "log_step_restore": "STEP 2: Restoring original files...",
        "log_removed": "  {count} files removed.",
        "log_restored": "  {count} files restored.",
        "log_uninstall_done": "Uninstall completed!",
        "log_cancelled": "Operation cancelled!",
        "log_error": "ERROR: {msg}",
        "log_no_manifest": "ERROR: Install manifest not found!",
        "lang_label": "Dil / Language:",
    },
}

# Renk paleti
C = {
    "bg": "#1a1a2e", "bg2": "#16213e", "bg3": "#0f3460",
    "gold": "#d4a843", "gold2": "#e8c468",
    "white": "#ffffff", "light": "#c4c4c4", "dim": "#8a8a8a",
    "green": "#4ecca3", "yellow": "#ffc107", "red": "#e94560",
    "bar_bg": "#2a2a4a", "border": "#2a2a4a",
}


# ─── Yardımcı Fonksiyonlar ──────────────────────────────────────────────────
def get_script_dir() -> str:
    """EXE veya .py fark etmeksizin, dosyanın GERÇEK bulunduğu dizini döndür."""
    # Nuitka onefile: __nuitka_binary_dir global olarak tanımlı
    nuitka_dir = globals().get("__nuitka_binary_dir")
    if nuitka_dir:
        return nuitka_dir
    # Nuitka onefile alternatif: NUITKA_ONEFILE_PARENT env var
    nuitka_parent = os.environ.get("NUITKA_ONEFILE_PARENT")
    if nuitka_parent:
        # Bu PID, ondan exe yolunu bulmak zor — CWD kullan
        pass
    # EXE olarak çalışıyorsa (argv[0] .exe ile bitiyorsa)
    argv0 = os.path.abspath(sys.argv[0])
    if argv0.lower().endswith('.exe'):
        return os.path.dirname(argv0)
    # PyInstaller
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    # Normal Python
    return os.path.dirname(os.path.abspath(__file__))


def sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt_size(n: int) -> str:
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} TB"


def detect_game_version(game_path: str) -> Optional[str]:
    """Oyun sürümünü tespit et — exe dosya bilgisi veya modinfo'dan."""
    # Yöntem 1: Windows file version info
    try:
        import ctypes
        from ctypes import wintypes
        exe = os.path.join(game_path, "Base", "Binaries", "Win64",
                           "Civ7_Win64_DX12_FinalRelease.exe")
        if os.path.isfile(exe):
            size = ctypes.windll.version.GetFileVersionInfoSizeW(exe, None)
            if size:
                buf = ctypes.create_string_buffer(size)
                ctypes.windll.version.GetFileVersionInfoW(exe, 0, size, buf)
                p = ctypes.c_void_p()
                l = ctypes.c_uint()
                if ctypes.windll.version.VerQueryValueW(
                    buf, r"\VS_VERSION_INFO", ctypes.byref(p), ctypes.byref(l)
                ):
                    # VS_FIXEDFILEINFO yapısı offset 0'da
                    pass
                # Alternatif: ProductVersion string
                if ctypes.windll.version.VerQueryValueW(
                    buf, r"\StringFileInfo\040904B0\ProductVersion",
                    ctypes.byref(p), ctypes.byref(l)
                ):
                    ver = ctypes.wstring_at(p, l.value).strip('\x00')
                    if ver:
                        return ver
    except Exception:
        pass

    # Yöntem 2: Exe dosya boyutu ve tarihinden tahmini sürüm
    exe_paths = [
        os.path.join(game_path, "Base", "Binaries", "Win64", "Civ7_Win64_DX12_FinalRelease.exe"),
        os.path.join(game_path, "Base", "Binaries", "Win64", "Civ7_Win64_Vulkan_FinalRelease.exe"),
    ]
    for exe in exe_paths:
        if os.path.isfile(exe):
            mtime = os.path.getmtime(exe)
            dt = datetime.datetime.fromtimestamp(mtime)
            size_mb = os.path.getsize(exe) / (1024 * 1024)
            return f"Build {dt.strftime('%Y.%m.%d')} ({size_mb:.0f} MB)"

    return None


def detect_game_path() -> Optional[str]:
    """Oyun yolunu otomatik tespit et — Steam, Epic, Xbox/MS Store, manuel."""
    # 1) Varsayılan yol
    if os.path.isdir(DEFAULT_GAME_PATH):
        return DEFAULT_GAME_PATH

    # 2) Steam
    if winreg:
        steam_paths = []
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\WOW6432Node\Valve\Steam")
            sp, _ = winreg.QueryValueEx(key, "InstallPath")
            steam_paths.append(sp)
            winreg.CloseKey(key)
        except (OSError, FileNotFoundError):
            pass

        for sp in list(steam_paths):
            lib_file = os.path.join(sp, "steamapps", "libraryfolders.vdf")
            if os.path.isfile(lib_file):
                try:
                    with open(lib_file, "r", encoding="utf-8") as f:
                        for line in f:
                            if '"path"' in line:
                                parts = line.strip().split('"')
                                if len(parts) >= 4:
                                    steam_paths.append(parts[3])
                except Exception:
                    pass

        for sp in steam_paths:
            for name in ("Sid Meier's Civilization VII", "Civilization VII"):
                candidate = os.path.join(sp, "steamapps", "common", name)
                if os.path.isdir(candidate):
                    return candidate

    # 3) Epic Games
    if winreg:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\WOW6432Node\Epic Games\EpicGamesLauncher")
            epic_path, _ = winreg.QueryValueEx(key, "AppDataPath")
            winreg.CloseKey(key)
        except (OSError, FileNotFoundError):
            epic_path = None

        epic_dirs = []
        if epic_path:
            manifests = os.path.join(epic_path, "..", "Manifests")
            if os.path.isdir(manifests):
                epic_dirs.append(manifests)

        # Yaygın Epic yolları
        for drv in "CDEFG":
            for edir in (
                f"{drv}:\\Program Files\\Epic Games",
                f"{drv}:\\Epic Games",
            ):
                for name in ("CivilizationVII", "Civilization VII", "Sid Meier's Civilization VII"):
                    candidate = os.path.join(edir, name)
                    if os.path.isdir(candidate):
                        return candidate

    # 4) Xbox / Microsoft Store (PC Game Pass)
    for drv in "CDEFG":
        xbox_paths = [
            f"{drv}:\\XboxGames\\Sid Meier's Civilization VII\\Content",
            f"{drv}:\\XboxGames\\Civilization VII\\Content",
            f"{drv}:\\XboxGames\\Sid Meier's Civilization VII",
        ]
        for xp in xbox_paths:
            if os.path.isdir(xp):
                return xp

    # WindowsApps (MS Store modifiable path)
    local_app = os.environ.get("LOCALAPPDATA", "")
    if local_app:
        ms_path = os.path.join(local_app, "Packages")
        if os.path.isdir(ms_path):
            for d in os.listdir(ms_path):
                if "civilization" in d.lower() or "firaxis" in d.lower():
                    candidate = os.path.join(ms_path, d, "LocalCache", "Local")
                    if os.path.isdir(candidate):
                        return candidate

    # 5) Yaygın manuel kurulum yolları
    for drv in "CDEFG":
        for p in (
            f"{drv}:\\Games\\Civilization VII",
            f"{drv}:\\Games\\Sid Meier's Civilization VII",
            f"{drv}:\\Program Files\\Civilization VII",
            f"{drv}:\\Program Files (x86)\\Civilization VII",
            f"{drv}:\\Program Files\\2K Games\\Civilization VII",
        ):
            if os.path.isdir(p):
                return p

    return None


def validate_game_path(path: str) -> Tuple[bool, str]:
    if not os.path.isdir(path):
        return False, "nodir"
    if not os.path.isdir(os.path.join(path, "Base")):
        return False, "nobase"
    if not os.path.isdir(os.path.join(path, "Base", "modules")):
        return False, "nomod"
    return True, "ok"


def collect_files(out_dir: str) -> List[Dict]:
    files = []
    for root, _, filenames in os.walk(out_dir):
        for fname in filenames:
            full = os.path.join(root, fname)
            files.append({
                "source": full,
                "relative": os.path.relpath(full, out_dir),
                "size": os.path.getsize(full),
            })
    return files


# ─── Manifest ────────────────────────────────────────────────────────────────
class Manifest:
    def __init__(self, path: str):
        self.path = path
        self.data: Dict = {}

    def load(self) -> bool:
        if os.path.isfile(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                return True
            except Exception:
                return False
        return False

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def create(self, game_path: str, total: int, backup_dir: str):
        self.data = {
            "version": APP_VERSION,
            "date": datetime.datetime.now().isoformat(),
            "game_path": game_path,
            "backup_dir": backup_dir,
            "installed": [],
            "backed_up": [],
            "total": total,
            "status": "in_progress",
        }

    def add_installed(self, rel: str, dest: str, h: str):
        self.data["installed"].append({"rel": rel, "dest": dest, "hash": h})

    def add_backup(self, orig: str, bak: str, h: str):
        self.data["backed_up"].append({"orig": orig, "bak": bak, "hash": h})

    def complete(self):
        self.data["status"] = "completed"
        self.data["completed_date"] = datetime.datetime.now().isoformat()

    def is_installed(self) -> bool:
        return self.data.get("status") == "completed"

    @property
    def version(self): return self.data.get("version", "?")
    @property
    def date(self): return self.data.get("date", "?")
    @property
    def game_path(self): return self.data.get("game_path", "")
    @property
    def backup_dir(self): return self.data.get("backup_dir", "")


# ─── Kurulum Motoru ─────────────────────────────────────────────────────────
class Engine:
    def __init__(self, game_path: str, out_dir: str, backup_base: str):
        self.game_path = game_path
        self.out_dir = out_dir
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = os.path.join(backup_base, f"backup_{ts}")
        self.manifest = Manifest(os.path.join(backup_base, MANIFEST_NAME))
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def install(self, on_progress=None, on_log=None, on_status=None):
        files = collect_files(self.out_dir)
        total = len(files)
        if not total:
            if on_log: on_log("ERROR: No files found!", "error")
            return False

        self.manifest.create(self.game_path, total, self.backup_dir)
        if on_log:
            on_log(on_log.__self__.t("log_total_files", count=total) if hasattr(on_log, '__self__') else f"Total {total} files.", "info")
        if on_log: on_log(f"Backup: {self.backup_dir}", "info")

        # Yedekleme
        if on_status: on_status("backup")
        os.makedirs(self.backup_dir, exist_ok=True)
        backed = 0
        for i, f in enumerate(files):
            if self._cancel: return False
            dest = os.path.join(self.game_path, f["relative"])
            if os.path.isfile(dest):
                bak = os.path.join(self.backup_dir, f["relative"])
                os.makedirs(os.path.dirname(bak), exist_ok=True)
                shutil.copy2(dest, bak)
                self.manifest.add_backup(dest, bak, sha256(dest))
                backed += 1
            if on_progress: on_progress(i + 1, total * 2, f["relative"])

        # Kopyalama
        if on_status: on_status("copy")
        installed = 0
        errors = []
        for i, f in enumerate(files):
            if self._cancel: return False
            dest = os.path.join(self.game_path, f["relative"])
            try:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(f["source"], dest)
                self.manifest.add_installed(f["relative"], dest, sha256(dest))
                installed += 1
            except Exception as e:
                errors.append(str(e))
                if on_log: on_log(f"  ERR: {f['relative']} - {e}", "error")
            if on_progress: on_progress(total + i + 1, total * 2, f["relative"])

        # Doğrulama
        if on_status: on_status("verify")
        verified = 0
        for fi in self.manifest.data["installed"]:
            if os.path.isfile(fi["dest"]) and sha256(fi["dest"]) == fi["hash"]:
                verified += 1

        self.manifest.complete()
        self.manifest.save()

        if on_progress: on_progress(total * 2, total * 2, "OK")
        return len(errors) == 0, {"installed": installed, "backed": backed, "verified": verified, "errors": len(errors)}

    def uninstall(self, on_progress=None, on_log=None, on_status=None):
        if not self.manifest.load():
            if on_log: on_log("No manifest!", "error")
            return False

        inst = self.manifest.data.get("installed", [])
        baks = self.manifest.data.get("backed_up", [])
        total = len(inst) + len(baks)
        if not total:
            return True

        # Sil
        if on_status: on_status("remove")
        removed = 0
        for i, fi in enumerate(inst):
            if os.path.isfile(fi["dest"]):
                try:
                    os.remove(fi["dest"])
                    removed += 1
                    p = os.path.dirname(fi["dest"])
                    while p != self.manifest.game_path:
                        if os.path.isdir(p) and not os.listdir(p):
                            os.rmdir(p)
                            p = os.path.dirname(p)
                        else:
                            break
                except Exception:
                    pass
            if on_progress: on_progress(i + 1, total, fi.get("rel", ""))

        # Geri yükle
        if on_status: on_status("restore")
        restored = 0
        for i, fi in enumerate(baks):
            if os.path.isfile(fi["bak"]):
                try:
                    os.makedirs(os.path.dirname(fi["orig"]), exist_ok=True)
                    shutil.copy2(fi["bak"], fi["orig"])
                    restored += 1
                except Exception:
                    pass
            if on_progress: on_progress(len(inst) + i + 1, total, os.path.basename(fi["orig"]))

        self.manifest.data["status"] = "uninstalled"
        self.manifest.save()
        if on_progress: on_progress(total, total, "OK")
        return True, {"removed": removed, "restored": restored}


# ─── GUI ─────────────────────────────────────────────────────────────────────
class SetupApp:
    def __init__(self):
        self.lang = "tr"
        self.root = tk.Tk()
        self.root.title(self.t("window_title"))
        self.root.geometry("780x640")
        self.root.minsize(700, 580)
        self.root.configure(bg=C["bg"])
        self.root.resizable(True, True)

        # İkon
        try:
            ico = os.path.join(get_script_dir(), "..", "icon.ico")
            if not os.path.isfile(ico):
                ico = os.path.join(get_script_dir(), "icon.ico")
            if os.path.isfile(ico):
                self.root.iconbitmap(ico)
        except Exception:
            pass

        self.script_dir = get_script_dir()
        self.out_dir = os.path.join(self.script_dir, "out")
        self.backup_base = os.path.join(self.script_dir, BACKUP_DIR_NAME)
        self.game_path_var = tk.StringVar()
        self.engine: Optional[Engine] = None
        self._thread: Optional[threading.Thread] = None

        self.manifest = Manifest(os.path.join(self.backup_base, MANIFEST_NAME))
        self._has_install = self.manifest.load() and self.manifest.is_installed()

        self._setup_styles()
        self._build_ui()
        self._auto_detect()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def t(self, key: str, **kwargs) -> str:
        txt = TEXTS.get(self.lang, TEXTS["tr"]).get(key, key)
        if kwargs:
            txt = txt.format(**kwargs)
        return txt

    def _setup_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Dark.TFrame", background=C["bg"])
        s.configure("Card.TFrame", background=C["bg2"])
        s.configure("Title.TLabel", background=C["bg"], foreground=C["gold"],
                     font=("Segoe UI", 20, "bold"))
        s.configure("Sub.TLabel", background=C["bg"], foreground=C["light"],
                     font=("Segoe UI", 10))
        s.configure("Head.TLabel", background=C["bg2"], foreground=C["white"],
                     font=("Segoe UI", 11, "bold"))
        s.configure("Info.TLabel", background=C["bg2"], foreground=C["light"],
                     font=("Segoe UI", 9))
        s.configure("Status.TLabel", background=C["bg"], foreground=C["dim"],
                     font=("Segoe UI", 9))
        s.configure("Warn.TLabel", background=C["bg"], foreground=C["yellow"],
                     font=("Segoe UI", 10))
        s.configure("Ok.TLabel", background=C["bg2"], foreground=C["green"],
                     font=("Segoe UI", 9))
        s.configure("Err.TLabel", background=C["bg2"], foreground=C["red"],
                     font=("Segoe UI", 9))
        s.configure("GameVer.TLabel", background=C["bg"], foreground=C["dim"],
                     font=("Segoe UI", 9))
        s.configure("Bar.Horizontal.TProgressbar", troughcolor=C["bar_bg"],
                     background=C["gold"], thickness=20)

    def _build_ui(self):
        main = ttk.Frame(self.root, style="Dark.TFrame")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # ── Üst: Başlık + Dil seçici ──
        top = ttk.Frame(main, style="Dark.TFrame")
        top.pack(fill=tk.X, pady=(0, 12))

        left = ttk.Frame(top, style="Dark.TFrame")
        left.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(left, text=self.t("header_line1"), style="Title.TLabel").pack(anchor="w")
        ttk.Label(left, text=self.t("header_line2"), style="Title.TLabel").pack(anchor="w")
        self.subtitle_lbl = ttk.Label(left,
            text=self.t("subtitle", version=APP_VERSION, patch=PATCH_VERSION),
            style="Sub.TLabel")
        self.subtitle_lbl.pack(anchor="w", pady=(4, 0))

        self.game_ver_lbl = ttk.Label(left, text="", style="GameVer.TLabel")
        self.game_ver_lbl.pack(anchor="w", pady=(2, 0))

        # Dil seçici (sağ üst)
        lang_frame = ttk.Frame(top, style="Dark.TFrame")
        lang_frame.pack(side=tk.RIGHT, anchor="ne")

        ttk.Label(lang_frame, text=self.t("lang_label"), style="Sub.TLabel").pack(anchor="e")
        self.lang_var = tk.StringVar(value="Türkçe")
        lang_combo = tk.OptionMenu(lang_frame, self.lang_var, "Türkçe", "English",
                                    command=self._change_lang)
        lang_combo.configure(bg=C["bg2"], fg=C["light"], activebackground=C["bg3"],
                             activeforeground=C["white"], relief="flat", bd=0,
                             font=("Segoe UI", 9), highlightthickness=0)
        lang_combo["menu"].configure(bg=C["bg2"], fg=C["light"],
                                      activebackground=C["gold"], activeforeground=C["bg"])
        lang_combo.pack(anchor="e", pady=(2, 0))

        # ── Mevcut kurulum uyarısı ──
        if self._has_install:
            self.warn_lbl = ttk.Label(main,
                text=self.t("existing_install_warn",
                            version=self.manifest.version,
                            date=self.manifest.date[:10]),
                style="Warn.TLabel")
            self.warn_lbl.pack(fill=tk.X, pady=(0, 8))

        # ── Oyun Yolu Kartı ──
        pc = ttk.Frame(main, style="Card.TFrame")
        pc.pack(fill=tk.X, pady=(0, 10))
        pi = ttk.Frame(pc, style="Card.TFrame")
        pi.pack(fill=tk.X, padx=15, pady=12)

        self.path_title_lbl = ttk.Label(pi, text=self.t("path_card_title"), style="Head.TLabel")
        self.path_title_lbl.pack(anchor="w")
        self.path_desc_lbl = ttk.Label(pi, text=self.t("path_card_desc"), style="Info.TLabel")
        self.path_desc_lbl.pack(anchor="w", pady=(2, 8))

        row = ttk.Frame(pi, style="Card.TFrame")
        row.pack(fill=tk.X)

        self.path_entry = tk.Entry(row, textvariable=self.game_path_var,
                                   font=("Segoe UI", 10), bg=C["bg"], fg=C["white"],
                                   insertbackground=C["white"], relief="flat", bd=6)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        self.browse_btn = tk.Button(row, text=self.t("browse_btn"),
                                    font=("Segoe UI", 9, "bold"),
                                    bg=C["bg3"], fg=C["white"],
                                    activebackground=C["gold"], activeforeground=C["bg"],
                                    relief="flat", bd=0, padx=14, pady=6,
                                    cursor="hand2", command=self._browse)
        self.browse_btn.pack(side=tk.RIGHT)

        self.path_status_lbl = ttk.Label(pi, text="", style="Info.TLabel")
        self.path_status_lbl.pack(anchor="w", pady=(6, 0))

        # ── Bilgi Kartı ──
        ic = ttk.Frame(main, style="Card.TFrame")
        ic.pack(fill=tk.X, pady=(0, 10))
        ii = ttk.Frame(ic, style="Card.TFrame")
        ii.pack(fill=tk.X, padx=15, pady=12)

        self.info_title_lbl = ttk.Label(ii, text=self.t("info_card_title"), style="Head.TLabel")
        self.info_title_lbl.pack(anchor="w")
        self.info_lbl = ttk.Label(ii, text=self.t("info_calculating"),
                                  style="Info.TLabel", wraplength=680)
        self.info_lbl.pack(anchor="w", pady=(6, 0))

        # ── İlerleme ──
        pf = ttk.Frame(main, style="Dark.TFrame")
        pf.pack(fill=tk.X, pady=(0, 6))

        self.prog_var = tk.DoubleVar(value=0)
        self.prog_bar = ttk.Progressbar(pf, variable=self.prog_var, maximum=100,
                                         style="Bar.Horizontal.TProgressbar")
        self.prog_bar.pack(fill=tk.X, pady=(0, 3))

        prog_row = ttk.Frame(pf, style="Dark.TFrame")
        prog_row.pack(fill=tk.X)
        self.prog_lbl = ttk.Label(prog_row, text="", style="Status.TLabel")
        self.prog_lbl.pack(side=tk.LEFT)
        self.status_lbl = ttk.Label(prog_row, text=self.t("status_ready"), style="Status.TLabel")
        self.status_lbl.pack(side=tk.RIGHT)

        # ── Log ──
        lf = ttk.Frame(main, style="Dark.TFrame")
        lf.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.log = tk.Text(lf, height=7, bg=C["bg2"], fg=C["light"],
                           font=("Consolas", 9), relief="flat", bd=8,
                           wrap=tk.WORD, state=tk.DISABLED,
                           selectbackground=C["gold"])
        self.log.pack(fill=tk.BOTH, expand=True)
        self.log.tag_configure("info", foreground=C["light"])
        self.log.tag_configure("success", foreground=C["green"])
        self.log.tag_configure("warning", foreground=C["yellow"])
        self.log.tag_configure("error", foreground=C["red"])

        # ── Butonlar ──
        bf = ttk.Frame(main, style="Dark.TFrame")
        bf.pack(fill=tk.X)

        self.install_btn = tk.Button(bf, text=self.t("btn_install"),
            font=("Segoe UI", 12, "bold"), bg=C["gold"], fg=C["bg"],
            activebackground=C["gold2"], activeforeground=C["bg"],
            relief="flat", bd=0, padx=30, pady=10, cursor="hand2",
            command=self._do_install)
        self.install_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.uninstall_btn = tk.Button(bf, text=self.t("btn_uninstall"),
            font=("Segoe UI", 10), bg=C["bg3"], fg=C["white"],
            activebackground=C["red"], activeforeground=C["white"],
            relief="flat", bd=0, padx=20, pady=10, cursor="hand2",
            command=self._do_uninstall)
        self.uninstall_btn.pack(side=tk.LEFT, padx=(0, 8))

        if not self._has_install:
            self.uninstall_btn.configure(state=tk.DISABLED, bg=C["border"], fg=C["dim"])

        self.close_btn = tk.Button(bf, text=self.t("btn_close"),
            font=("Segoe UI", 10), bg=C["border"], fg=C["light"],
            activebackground=C["red"], activeforeground=C["white"],
            relief="flat", bd=0, padx=20, pady=10, cursor="hand2",
            command=self._on_close)
        self.close_btn.pack(side=tk.RIGHT)

        self.root.after(200, self._update_info)

    def _change_lang(self, selection):
        self.lang = "en" if selection == "English" else "tr"
        # Tüm metinleri güncelle
        self.root.title(self.t("window_title"))
        self.subtitle_lbl.configure(text=self.t("subtitle", version=APP_VERSION, patch=PATCH_VERSION))
        self.path_title_lbl.configure(text=self.t("path_card_title"))
        self.path_desc_lbl.configure(text=self.t("path_card_desc"))
        self.browse_btn.configure(text=self.t("browse_btn"))
        self.info_title_lbl.configure(text=self.t("info_card_title"))
        self.install_btn.configure(text=self.t("btn_install"))
        self.uninstall_btn.configure(text=self.t("btn_uninstall"))
        self.close_btn.configure(text=self.t("btn_close"))
        self.status_lbl.configure(text=self.t("status_ready"))
        self._update_info()

    def _auto_detect(self):
        detected = detect_game_path()
        if detected:
            self.game_path_var.set(detected)
            self._add_log(self.t("log_auto_detect", path=detected), "success")
        elif self._has_install:
            self.game_path_var.set(self.manifest.game_path)
            self._add_log(self.t("log_prev_install", path=self.manifest.game_path), "info")
        else:
            # Varsayılan yolu göster
            self.game_path_var.set(DEFAULT_GAME_PATH)

    def _browse(self):
        p = filedialog.askdirectory(title="Civilization VII",
                                    initialdir=self.game_path_var.get() or "C:\\")
        if p:
            self.game_path_var.set(p)
            self._update_info()

    def _update_info(self):
        gp = self.game_path_var.get()
        if not gp:
            self.path_status_lbl.configure(text=self.t("path_not_set"), foreground=C["yellow"])
            self.info_lbl.configure(text=self.t("info_select_path"))
            self.game_ver_lbl.configure(text="")
            return

        ok, code = validate_game_path(gp)
        if ok:
            self.path_status_lbl.configure(text=self.t("path_valid"), foreground=C["green"])
            # Oyun sürümü
            ver = detect_game_version(gp)
            if ver:
                self.game_ver_lbl.configure(text=self.t("game_version", version=ver))
            else:
                self.game_ver_lbl.configure(text=self.t("game_version_unknown"))
        else:
            err_key = f"path_invalid_{code}"
            self.path_status_lbl.configure(text=self.t(err_key), foreground=C["red"])
            self.info_lbl.configure(text=self.t(err_key))
            self.game_ver_lbl.configure(text="")
            return

        if os.path.isdir(self.out_dir):
            files = collect_files(self.out_dir)
            total_size = sum(f["size"] for f in files)
            xml_c = sum(1 for f in files if f["relative"].endswith(".xml"))
            vtt_c = sum(1 for f in files if f["relative"].endswith(".vtt"))
            other = len(files) - xml_c - vtt_c
            self.info_lbl.configure(text=self.t("info_summary",
                total=len(files), size=fmt_size(total_size),
                xml=xml_c, vtt=vtt_c, other=other))
        else:
            self.info_lbl.configure(text=self.t("info_no_out"))

    def _add_log(self, msg: str, level: str = "info"):
        self.log.configure(state=tk.NORMAL)
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        icon = {"info": "ℹ", "success": "✓", "warning": "⚠", "error": "✗"}.get(level, "•")
        self.log.insert(tk.END, f"[{ts}] {icon} {msg}\n", level)
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _log_safe(self, msg: str, level: str = "info"):
        self.root.after(0, lambda: self._add_log(msg, level))

    def _prog(self, cur: int, total: int, name: str):
        if total > 0:
            pct = (cur / total) * 100
            short = name if len(name) < 55 else "..." + name[-52:]
            self.root.after(0, lambda: self.prog_var.set(pct))
            self.root.after(0, lambda: self.prog_lbl.configure(text=f"{cur}/{total}  •  {short}"))

    def _set_status(self, key: str):
        self.root.after(0, lambda: self.status_lbl.configure(text=self.t(f"status_{key}")))

    def _lock(self, locked: bool):
        if locked:
            self.install_btn.configure(state=tk.DISABLED, bg=C["border"])
            self.uninstall_btn.configure(state=tk.DISABLED, bg=C["border"])
            self.path_entry.configure(state=tk.DISABLED)
        else:
            self.install_btn.configure(state=tk.NORMAL, bg=C["gold"])
            self.path_entry.configure(state=tk.NORMAL)
            if self._has_install:
                self.uninstall_btn.configure(state=tk.NORMAL, bg=C["bg3"], fg=C["white"])

    def _do_install(self):
        gp = self.game_path_var.get()
        ok, code = validate_game_path(gp)
        if not ok:
            messagebox.showerror("Error", self.t(f"path_invalid_{code}"))
            return
        if not os.path.isdir(self.out_dir):
            messagebox.showerror("Error", self.t("err_no_out"))
            return
        if self._has_install:
            if not messagebox.askyesno(self.t("confirm_overwrite_title"),
                                        self.t("confirm_overwrite_msg")):
                return
        if not messagebox.askyesno(self.t("confirm_install_title"),
                                    self.t("confirm_install_msg", path=gp)):
            return

        self._lock(True)
        self.prog_var.set(0)
        self.engine = Engine(gp, self.out_dir, self.backup_base)

        def run():
            try:
                self._log_safe(self.t("log_total_files", count=len(collect_files(self.out_dir))), "info")
                self._log_safe(self.t("log_backup_dir", path=self.engine.backup_dir), "info")
                self._log_safe("─" * 45, "info")

                self._log_safe(self.t("log_step_backup"), "info")
                self._set_status("backing_up")

                result = self.engine.install(
                    on_progress=self._prog,
                    on_log=self._log_safe,
                    on_status=lambda s: self._set_status({"backup": "backing_up", "copy": "installing", "verify": "verifying"}.get(s, s)),
                )

                if isinstance(result, tuple):
                    success, stats = result
                else:
                    success, stats = result, {}

                self._log_safe("─" * 45, "info")
                if success:
                    self._log_safe(self.t("log_complete_ok"), "success")
                else:
                    self._log_safe(self.t("log_complete_err", count=stats.get("errors", 0)), "warning")

                self._log_safe(self.t("log_installed", count=stats.get("installed", 0)), "info")
                self._log_safe(self.t("log_backed", count=stats.get("backed", 0)), "info")
                self._log_safe(self.t("log_verified_count", count=stats.get("verified", 0)), "info")

                self.root.after(0, lambda: self._install_done(success))
            except Exception as e:
                self._log_safe(f"Exception: {e}", "error")
                self._log_safe(traceback.format_exc(), "error")
                self.root.after(0, lambda: self._install_done(False))

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def _install_done(self, success: bool):
        self._lock(False)
        self._has_install = True
        self.uninstall_btn.configure(state=tk.NORMAL, bg=C["bg3"], fg=C["white"])
        if success:
            self._set_status("done")
            messagebox.showinfo(self.t("success_install_title"), self.t("success_install_msg"))
        else:
            self._set_status("failed")
            messagebox.showwarning(self.t("warn_errors_title"), self.t("warn_errors_msg"))

    def _do_uninstall(self):
        if not self._has_install:
            messagebox.showinfo("Info", self.t("err_no_manifest"))
            return
        if not messagebox.askyesno(self.t("confirm_uninstall_title"),
                                    self.t("confirm_uninstall_msg")):
            return

        self._lock(True)
        self.prog_var.set(0)
        self.engine = Engine(self.manifest.game_path, self.out_dir, self.backup_base)

        def run():
            try:
                self._log_safe(self.t("log_uninstall_start"), "info")
                self._log_safe("─" * 45, "info")
                self._log_safe(self.t("log_step_remove"), "info")

                result = self.engine.uninstall(
                    on_progress=self._prog,
                    on_log=self._log_safe,
                    on_status=lambda s: self._set_status({"remove": "removing", "restore": "restoring"}.get(s, s)),
                )

                if isinstance(result, tuple):
                    success, stats = result
                else:
                    success, stats = result, {}

                self._log_safe("─" * 45, "info")
                self._log_safe(self.t("log_removed", count=stats.get("removed", 0)), "success")
                self._log_safe(self.t("log_restored", count=stats.get("restored", 0)), "success")
                self._log_safe(self.t("log_uninstall_done"), "success")

                self.root.after(0, lambda: self._uninstall_done(success))
            except Exception as e:
                self._log_safe(f"Exception: {e}", "error")
                self.root.after(0, lambda: self._uninstall_done(False))

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def _uninstall_done(self, success: bool):
        self._lock(False)
        if success:
            self._has_install = False
            self.uninstall_btn.configure(state=tk.DISABLED, bg=C["border"], fg=C["dim"])
            self._set_status("uninstall_done")
            messagebox.showinfo(self.t("success_uninstall_title"), self.t("success_uninstall_msg"))
        else:
            self._set_status("failed")
            messagebox.showwarning(self.t("warn_errors_title"), self.t("warn_errors_msg"))

    def _on_close(self):
        if self._thread and self._thread.is_alive():
            if not messagebox.askyesno(self.t("close_while_running_title"),
                                        self.t("close_while_running_msg")):
                return
            if self.engine:
                self.engine.cancel()
        self.root.destroy()

    def run(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"+{x}+{y}")
        self.root.mainloop()


# ─── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SetupApp()
    app.run()
