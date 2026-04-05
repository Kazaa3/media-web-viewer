import logging
import platform
import shutil
import subprocess
import sys
from typing import Optional

logger = logging.getLogger("file_dialogs")


def _try_pyqt_dialog() -> Optional[str]:
    # Try PyQt6 then PyQt5
    for mod in ("PyQt6.QtWidgets", "PyQt5.QtWidgets"):
        try:
            parts = mod.split(".")
            mod_root = __import__(parts[0])
            for p in parts[1:]:
                mod_root = getattr(mod_root, p)
            QApplication = getattr(mod_root, "QApplication")
            QFileDialog = getattr(mod_root, "QFileDialog")
            app = QApplication.instance()
            created = False
            if app is None:
                app = QApplication(sys.argv or [])
                created = True
            folder = QFileDialog.getExistingDirectory(None, "Select folder")
            if created:
                try:
                    app.quit()
                except Exception:
                    pass
            if folder:
                return str(folder)
        except Exception:
            continue
    return None


def _try_zenity_kdialog() -> Optional[str]:
    # Linux graphical dialog via zenity or kdialog
    if shutil.which("zenity"):
        cmd = ["zenity", "--file-selection", "--directory", "--title=Select folder"]
    elif shutil.which("kdialog"):
        cmd = ["kdialog", "--getexistingdirectory", ".", "--title", "Select folder"]
    else:
        return None
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True, timeout=30)
        path = out.strip()
        return path or None
    except Exception as e:
        logger.debug("zenity/kdialog folder pick failed: %s", e)
        return None


def _try_macos_dialog() -> Optional[str]:
    if platform.system() != "Darwin":
        return None
    try:
        cmd = [
            "osascript",
            "-e",
            'POSIX path of (choose folder with prompt "Select folder" without invisibles)'
        ]
        out = subprocess.check_output(cmd, text=True, timeout=30)
        path = out.strip()
        return path or None
    except Exception as e:
        logger.debug("osascript folder pick failed: %s", e)
        return None


def _try_powershell_dialog() -> Optional[str]:
    if platform.system() != "Windows":
        return None
    ps = r"""
Add-Type -AssemblyName System.Windows.Forms
$dlg = New-Object System.Windows.Forms.FolderBrowserDialog
$dlg.Description = 'Select folder'
$ok = $dlg.ShowDialog()
if ($ok -eq [System.Windows.Forms.DialogResult]::OK) { Write-Output $dlg.SelectedPath }
"""
    try:
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps], text=True, timeout=30)
        path = out.strip()
        return path or None
    except Exception as e:
        logger.debug("powershell folder pick failed: %s", e)
        return None


def pick_folder() -> Optional[str]:
    """
    Cross-platform folder picker. Tries, in order:
      - PyQt6 / PyQt5 native QFileDialog
      - zenity / kdialog (Linux)
      - macOS osascript chooser
      - Windows PowerShell FolderBrowserDialog
      - (fallback) None
    Returns selected path or None.
    """
    # 1) PyQt native dialog (preferred)
    try:
        path = _try_pyqt_dialog()
        if path:
            return path
    except Exception as e:
        logger.debug("PyQt folder dialog failed: %s", e)

    # 2) Desktop dialogs (zenity/kdialog)
    try:
        path = _try_zenity_kdialog()
        if path:
            return path
    except Exception:
        pass

    # 3) macOS native
    try:
        path = _try_macos_dialog()
        if path:
            return path
    except Exception:
        pass

    # 4) Windows powershell
    try:
        path = _try_powershell_dialog()
        if path:
            return path
    except Exception:
        pass

    logger.debug("No native folder picker available, returning None")
    return None