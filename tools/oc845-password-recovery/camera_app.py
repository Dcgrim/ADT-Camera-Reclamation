#!/usr/bin/env python3
"""Offline OC845 camera helper. No credentials persisted."""
import hashlib
import ipaddress
import re
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from urllib.parse import quote

RTSP_PATH = "/img/media.sav"
FIRMWARE_CONSTANT = "06D58FFA826502BA52D3317A95169346"

def normalize_mac(raw):
    compact = re.sub(r"[:-]", "", raw.strip())
    if not re.fullmatch(r"[0-9a-fA-F]{12}", compact):
        raise ValueError("MAC must contain 12 hexadecimal digits")
    return ":".join(compact[i:i+2] for i in range(0, 12, 2)).upper()

def camera_password(mac):
    compact = normalize_mac(mac).replace(":", "")
    return hashlib.sha1((compact + FIRMWARE_CONSTANT).encode("ascii")).hexdigest()[:12]

def rtsp_url(ip, username, password):
    address = ipaddress.ip_address(ip.strip())
    if address.version != 4:
        raise ValueError("This version expects an IPv4 camera address")
    if not username or not password:
        raise ValueError("Enter username and password")
    return f'rtsp://{quote(username, safe="")}:{quote(password, safe="")}@{address}:554{RTSP_PATH}'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OC845 Offline Camera Helper")
        self.geometry("560x415")
        self.resizable(False, False)
        self.mac = tk.StringVar()
        self.ip = tk.StringVar()
        self.user = tk.StringVar(value="administrator")
        self.password = tk.StringVar()
        ttk.Label(self, text="ADT OC845 — local stream helper", font=("TkDefaultFont", 14, "bold")).pack(pady=(18, 10))
        form = ttk.Frame(self)
        form.pack(fill="x", padx=25)
        for i, (label, var) in enumerate([
            ("Camera MAC", self.mac), ("Camera IPv4", self.ip),
            ("Username", self.user), ("Known password", self.password)
        ]):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=7)
            ttk.Entry(form, textvariable=var, width=42, show="*" if i == 3 else "").grid(row=i, column=1, sticky="ew", padx=12)
        ttk.Button(self, text="Calculate password from MAC", command=self.calculate).pack(pady=(12, 4))
        ttk.Button(self, text="Validate & copy RTSP URL", command=self.make_url).pack(pady=4)
        ttk.Button(self, text="Open in VLC", command=self.open_vlc).pack(pady=4)
        self.status = ttk.Label(self, text="Offline only; test with a camera you own.", wraplength=510)
        self.status.pack(pady=(14, 4))
        ttk.Label(self, text="Credentials are not saved. Clear your clipboard after use.").pack()
    def calculate(self):
        try:
            self.password.set(camera_password(self.mac.get()))
            self.status.config(text="Candidate password calculated locally; verify on your camera.")
        except ValueError as exc:
            messagebox.showerror("Check MAC", str(exc))
    def make_url(self):
        try:
            normalize_mac(self.mac.get())
            url = rtsp_url(self.ip.get(), self.user.get(), self.password.get())
            self.clipboard_clear()
            self.clipboard_append(url)
            self.status.config(text="RTSP URL copied to clipboard. Keep it private.")
            return url
        except ValueError as exc:
            messagebox.showerror("Check details", str(exc))
            return None
    def open_vlc(self):
        url = self.make_url()
        if not url:
            return
        vlc = shutil.which("vlc")
        if not vlc:
            messagebox.showinfo("VLC missing", "Install VLC. Your URL is on the clipboard.")
            return
        subprocess.Popen([vlc, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    App().mainloop()
