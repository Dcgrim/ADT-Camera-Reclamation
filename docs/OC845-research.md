# Reclaiming ADT OC845 Cameras: Field Discovery and Local-Access Work Paper

**Status:** Reconstructed field notes, 13 November 2026. **Scope:** Owner-controlled ADT OC845 cameras on an isolated LAN. **Evidence categories:** recorded observation; reported success; published external research; hypothesis; unresolved.

## Abstract

Four outdoor ADT OC845 cameras were provisioned on a local TP-Link Deco network and recorded with administrator credentials and RTSP endpoints. The operator reports completing reset, Wi-Fi onboarding, and camera login in approximately 3–5 minutes per unit. These findings establish a useful operational workflow, and the MAC-derived administrator password algorithm was independently verified against four archived credential pairs. This does **not** prove root-shell access. The goal is local ownership and management without depending on the vendor cloud.

## Discovery keywords / index

`ADT`, `OC845`, `OC-845`, `Sercomm`, `Deco`, `tplink`, `[REDACTED PRIVATE IP]`, `192.168.68.x`, `WPS`, `reset`, `wireless setup`, `MAC`, `administrator`, `401 Unauthorized`, `HTTP Digest`, `RTSP`, `554`, `/img/media.sav`, `VLC`, `ONVIF`, `UART`, `Amboot`, `NAND`, `Nathan Higley`, `astr0n8t`, `Ghidra`, `firmware`, `offline camera helper`.

## Provenance and chronology

- **12 October 2026:** A recorded camera MAC was `[REDACTED CAMERA MAC]`. Its setup access point served `[REDACTED PRIVATE IP]`; the connecting PC received `[REDACTED PRIVATE IP]`. The camera was subsequently joined to an isolated TP-Link network at `[REDACTED PRIVATE IP]`. During an earlier probe, RTSP port 554 responded, but some HTTP and media requests returned `401 Unauthorized`; `admin/admin` was rejected. These are **point-in-time observations**, not proof that the final setup failed.
- **13 October 2026:** The test camera remained isolated from upstream internet connectivity while the local LAN remained operational. Recorded pages included `http://[REDACTED PRIVATE IP]/setup/wireless_m_language.html` and the camera's LAN web interface.
- **17 October 2026:** Another camera was recorded with MAC `[REDACTED CAMERA MAC]`, LAN IP `[REDACTED PRIVATE IP]`. Earlier notes described its credentials as unresolved at that time.
- **Later camera inventory:** A private `Camera.txt` records four camera IP/MAC/administrator-password tuples and the common RTSP path `rtsp://<host>:554/img/media.sav`. This is **credential documentation**, not independent packet-level validation of all streams.
- **13 November 2026 operator report:** All outdoor OC845s are now accessible; the reset, Wi-Fi onboarding, and login process takes approximately 3–5 minutes. **Operator-reported result**; reproducibility test and firmware versions not yet captured.

## Observed equipment and network architecture

The cameras were provisioned on a TP-Link Deco isolated local network, historically using the `[REDACTED PRIVATE IP]/24` address space with a gateway around `[REDACTED PRIVATE IP]`. The camera's temporary AP/setup address was `[REDACTED PRIVATE IP]`. DHCP addresses may change; identify a camera by its MAC and current lease rather than treating any IP as permanent. Keep cameras isolated from the internet while testing. Do not disturb any separate fire or safety monitoring system.

## Reconstructed field workflow (non-destructive)

1. Reset an **owned** OC845 using its physical reset/WPS controls; note the actual firmware behavior and timing on the device.
2. Join its temporary setup Wi-Fi and browse to `http://[REDACTED PRIVATE IP]/` (a historically observed setup path is `/setup/wireless_m_language.html`).
3. Configure the camera to join the isolated local Wi-Fi SSID. Allow it to reconnect.
4. Find the camera's new LAN IP in the Deco client/DHCP list; verify its MAC address.
5. Use the **known, authorized administrator credentials** for that device. A local credential inventory exists but is intentionally **not committed** to GitHub.
6. Check the web UI and, where supported, the RTSP endpoint `rtsp://<IP>:554/img/media.sav` with an RTSP client such as VLC. Record actual authentication and video results.
7. Record firmware build, model label, test date, access method, and any failures before moving to the next camera.

## Password calculation: recovered and independently verified

A recovered firmware constant is `06D58FFA826502BA52D3317A95169346`. Normalize the camera MAC to uppercase hexadecimal without separators; append the constant as ASCII text; SHA-1 hash the concatenation; and use the first 12 lowercase hexadecimal characters as the administrator password. On 13 November 2026, this calculation was independently reproduced against all **four** privately archived MAC/password pairs (4/4 exact matches). A fifth match was reported by a separate conversation, but its test pair has not been independently inspected here.

```python
import hashlib

def camera_password(mac):
    key = "06D58FFA826502BA52D3317A95169346"
    mac = mac.replace(":", "").replace("-", "").upper()
    return hashlib.sha1((mac + key).encode("ascii")).hexdigest()[:12]
```

**Attribution note:** The operator reports recovering the constant from research associated with Nathan Higley. Before publication, verify the specific source passage or code that establishes its provenance; do not assume his documented 16-bit `id2pwd` Linux-login investigation is the same mechanism. The password calculator applies to the tested web/RTSP administrator credentials, not a demonstrated Linux root shell.

## Related independent research

Nathan Higley (`astr0n8t`), *Hacking Cheap IoT Cameras for Fun and No Profit* (14 October 2025): https://blog.nathanhigley.com/iotcamerahacking/ . He documents OC845 and OC432 devices, UART boot logs, firmware inspection, the `id2pwd` investigation, and access to the Amboot bootloader. His hardware-level path is a **different access route** from the operator's reported network provisioning workflow. His success does not establish that root shell access is available through the web UI.

Earlier Sercomm background: https://github.com/edent/Sercomm-API .

## Results, limitations, and next experiments

**Recorded:** four camera MAC/IP/password associations in a private file; common RTSP path; at least one camera's temporary AP and TP-Link onboarding; prior HTTP 401 responses; operator report that all four cameras were accessible.

**Not yet established:** derivation across untested firmware revisions, firmware/build uniformity, whether all four RTSP streams currently play, ONVIF support, durable Linux shell/root access, cloud independence after extended operation, and whether the operator's setup method transfers to other firmware revisions.

Suggested non-destructive validation: record each firmware version; re-check current IP and authenticated RTSP playback; save sanitized screenshots/logs; verify offline operation with WAN disconnected; and validate the MAC derivation against an additional, previously unseen camera.

## Application deliverable

`camera_app.py` is an offline Python/Tkinter helper for Linux and Windows. It validates a MAC and IPv4 address, calculates a candidate administrator password from the MAC or accepts a known credential, generates the RTSP URL, copies it to the clipboard, and optionally opens VLC. The algorithm has been verified against four private test vectors; the program does not probe cameras or change settings. See `README.md`.

## Publication and security

Do not commit `Camera.txt`, passwords, embedded-password RTSP URLs, private network inventory, or exported session cookies. This document deliberately avoids the four live password values. Public research should focus on reproducible methods and non-secret evidence. The application stores no credentials.

## Embedded-Linux and microSD research direction

The SD-card management route `/sd/sdctrl.cgi`, the `SDCARD` configuration group, and the reported `format`/`safe_rm` actions motivate a separate investigation. Their presence does not demonstrate a mounted filesystem, bootable recovery media, or execution of files placed on microSD. See [SD_CARD_RESEARCH.md](SD_CARD_RESEARCH.md) for the evidence ledger and first non-destructive test. Nathan Higley remains the primary external firmware-research reference; his UART/Amboot work is distinguished from the proposed microSD experiments.