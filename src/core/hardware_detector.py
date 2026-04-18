import os
import sys
import subprocess
import shutil
import platform
import glob
from pathlib import Path
from typing import Any, Dict, List
import socket
from src.core.logger import get_logger
log = get_logger("hardware_detector")

def is_port_in_use(port: int, host: str = "localhost") -> bool:
    """Check if a specific TCP port is currently in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def is_ssd(device_name: str) -> bool:
    """Check if a device is an SSD (non-rotational)."""
    try:
        # device_name like 'sda'
        rotational_path = Path(f"/sys/block/{device_name}/queue/rotational")
        if rotational_path.exists():
            return rotational_path.read_text().strip() == "0"
    except Exception:
        pass
    return False

def get_pcie_generation(device_path: str) -> str:
    """Attempt to detect PCIe generation (3 vs 4) for a device."""
    try:
        pci_path = Path(f"/sys/class/block/{device_path}/device").resolve()
        current = pci_path
        for _ in range(5):
            speed_file = current / "max_link_speed"
            if speed_file.exists():
                speed = speed_file.read_text().strip()
                if "128.0 GT/s" in speed: return "PCIe 7"
                if "64.0 GT/s" in speed: return "PCIe 6"
                if "32.0 GT/s" in speed: return "PCIe 5"
                if "16.0 GT/s" in speed: return "PCIe 4"
                if "8.0 GT/s" in speed: return "PCIe 3"
                if "5.0 GT/s" in speed: return "PCIe 2"
                if "2.5 GT/s" in speed: return "PCIe 1"
                return speed
            current = current.parent
            if current == Path("/"): break
    except Exception:
        pass
    return "Unknown"

def is_network_mount(path: str) -> bool:
    """Check if a path is on a network mount (SMB/NFS)."""
    try:
        path_obj = Path(path).resolve()
        # Find mount point
        while not os.path.ismount(path_obj):
            path_obj = path_obj.parent
            if path_obj == Path("/"): break
            
        if Path("/proc/mounts").exists():
            with open("/proc/mounts", "r") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 3 and parts[1] == str(path_obj):
                        fs_type = parts[2]
                        if fs_type in ("nfs", "nfs4", "cifs", "smb3", "fuse.sshfs"):
                            return True
    except Exception:
        pass
    return False

def get_gpu_info(fast_mode: bool = False) -> Dict[str, Any]:
    """
    @brief Detects GPU type and available hardware encoders.
    @param fast_mode If True, skips slow subprocess calls (like ffmpeg -encoders).
    """
    gpu_type = "Unknown"
    is_intel = False
    encoders = []
    
    # 1. NVIDIA Check (Fast)
    if shutil.which("nvidia-smi"):
        gpu_type = "NVIDIA"
    
    # 2. Intel Check (Fast)
    if os.path.exists("/dev/dri/renderD128"):
        if gpu_type == "Unknown":
            gpu_type = "VAAPI-Generic"
        
        # Check for Intel specifically via lspci
        if shutil.which("lspci"):
            try:
                # Use a very short timeout for lspci
                pci_info = subprocess.run(["lspci"], capture_output=True, text=True, timeout=0.5).stdout.lower()
                if "intel" in pci_info:
                    is_intel = True
                    gpu_type = "Intel"
            except: pass

    # 3. Encoder & Decoder Check (Slow - Skip if fast_mode)
    decoders = []
    if not fast_mode and shutil.which("ffmpeg"):
        try:
            # Encoders
            res_e = subprocess.run(["ffmpeg", "-encoders"], capture_output=True, text=True, timeout=1.0)
            stdout_e = res_e.stdout if res_e.stdout else ""
            
            if gpu_type == "NVIDIA" and "h264_nvenc" in stdout_e:
                encoders.append("nvenc")
            
            if "h264_qsv" in stdout_e:
                encoders.append("qsv")
                if is_intel: gpu_type = "Intel (QSV)"
            
            if "h264_vaapi" in stdout_e:
                encoders.append("vaapi")
                if is_intel and "qsv" in encoders:
                    gpu_type = "Intel (QSV+VAAPI)"
                elif is_intel:
                    gpu_type = "Intel (VAAPI)"
            
            # Decoders (v1.46.048)
            res_d = subprocess.run(["ffmpeg", "-decoders"], capture_output=True, text=True, timeout=1.0)
            stdout_d = res_d.stdout if res_d.stdout else ""
            
            hw_dec_markers = ["_qsv", "_vaapi", "_cuvid", "_nvdec", "_v4l2m2m"]
            for marker in hw_dec_markers:
                if f"h264{marker}" in stdout_d: decoders.append(f"h264{marker}")
                if f"hevc{marker}" in stdout_d: decoders.append(f"hevc{marker}")
                if f"vp9{marker}" in stdout_d: decoders.append(f"vp9{marker}")
            
        except Exception:
            pass

    return {
        "type": gpu_type, 
        "encoders": encoders, 
        "decoders": decoders,
        "hevc_hw_decoding_available": any("hevc_" in d for d in decoders)
    }

def get_best_hw_encoder() -> str:
    """
    @brief Returns the best available HW encoder for H.264.
    @details Priority: QSV (Intel) > NVENC (NVIDIA) > VAAPI (Generic) > libx264 (Software)
    """
    try:
        hw = get_gpu_info()
        available = hw.get("encoders", [])
        
        if "qsv" in available: return "h264_qsv"
        if "nvenc" in available: return "h264_nvenc"
        if "vaapi" in available: return "h264_vaapi"
    except Exception:
        pass
    return "libx264"

def get_gpu_usage_safe() -> float:
    """
    @brief Returns precise GPU utilization (0-100%).
    @details Supports Intel Arc (gpu_busy_percent), AMD, and NVIDIA.
    """
    try:
        # 1. Intel Arc / AMD (sysfs)
        # kernel 6.1+ / Mesa 24+ for Arc
        cards = glob.glob('/sys/class/drm/card*/device/gpu_busy_percent')
        if cards:
            with open(cards[0], 'r') as f:
                val = int(f.read().strip())
                # Intel uses 0-1000 for busy_percent in some drivers
                if val > 100: return val / 10.0
                return float(val)

        # 2. Fallback iGPU (Frequency Proxy)
        freq_file = '/sys/class/drm/card0/gt_cur_freq_mhz'
        max_freq_file = '/sys/class/drm/card0/gt_max_freq_mhz'
        if os.path.exists(freq_file) and os.path.exists(max_freq_file):
            try:
                with open(freq_file, 'r') as f1, open(max_freq_file, 'r') as f2:
                    cur = int(f1.read().strip())
                    max_f = int(f2.read().strip())
                    return (cur / max_f) * 100.0 if max_f > 0 else 0.0
            except: pass

        # 3. NVIDIA (nvidia-smi)
        if shutil.which("nvidia-smi"):
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=1
            )
            if res.returncode == 0:
                return float(res.stdout.strip())
                
    except Exception:
        pass
    return 0.0

def get_hardware_info():
    """Compiles a summary of relevant hardware info for Desktop-Mode."""
    info: dict = {
        "disks": [],
        "os": sys.platform,
        "is_linux": sys.platform.startswith("linux"),
        "disk_type": "-",
        "pcie_gen": "-",
        "is_network_mount": False,
        "gpu_type": "Unknown",
        "encoders": []
    }
    
    if info["is_linux"]:
        try:
            # List block devices
            block_dir = Path("/sys/block")
            if block_dir.exists():
                for dev in block_dir.iterdir():
                    if dev.name.startswith(("sd", "nvme")):
                        disk_info = {
                            "name": dev.name,
                            "is_ssd": is_ssd(dev.name),
                            "pcie_gen": get_pcie_generation(dev.name) if "nvme" in dev.name else "N/A"
                        }
                        info["disks"].append(disk_info)
                
                if info["disks"]:
                    # Sort to get nvme first (usually boot drive)
                    info["disks"].sort(key=lambda x: 0 if "nvme" in x["name"] else 1)
                    m = info["disks"][0]
                    info["disk_type"] = "SSD" if m["is_ssd"] else "HDD"
                    info["pcie_gen"] = m["pcie_gen"]
        except Exception:
            pass
            
    # Add GPU / Encoder detection
    gpu = get_gpu_info()
    info["gpu_type"] = gpu["type"]
    info["encoders"] = gpu["encoders"]
    info["decoders"] = gpu["decoders"]
    info["hevc_hw_decoding_available"] = gpu["hevc_hw_decoding_available"]
    
    log.info(f"[HW-PULSE] Hardware Audit: GPU={info['gpu_type']} | HEVC-HW={info['hevc_hw_decoding_available']} | Encoders={info['encoders']}")
    
    return info

if __name__ == "__main__":
    import json
    print(json.dumps(get_hardware_info(), indent=2))
