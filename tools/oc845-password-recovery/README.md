# OC845 Offline Camera Helper

A small Python/Tkinter desktop application for authorized owners of compatible ADT OC845 cameras.

## Requirements

- Python 3 with Tkinter (standard library; on Debian/Parrot: `sudo apt install python3-tk`)
- Optional: VLC for direct RTSP playback

## Start

```bash
python3 camera_app.py
```

On Windows, use `py camera_app.py` after installing Python with Tk support.

First, follow [the MAC identification guide](../../docs/finding-the-correct-mac.md) to distinguish the camera's Wi-Fi client MAC from its setup hotspot BSSID or other interface identifiers. **Do not assume a different address is fake.**

Enter the camera's MAC address, its current local IPv4 address, and the account name. Click **Calculate password from MAC** to generate a candidate password for the tested OC845 firmware, then **Validate & copy RTSP URL** or **Open in VLC**.

The app does not scan the network, write credentials to disk, or connect to a camera until you choose to open VLC. **The copied RTSP URL contains credentials**: do not paste it into issues, screenshots, logs, or public chat. Clear the clipboard afterward.

## Limits

Tested algorithm: four archived OC845 camera credential pairs matched. This is **not** a claim of support for all OC845 firmware, or any RC845 variant. Root-shell access is not established. See [field research](../../docs/OC845-research.md).

Original research inspiration: [Nathan Higley](https://blog.nathanhigley.com/iotcamerahacking/).

## Fictional example

For the non-real MAC `02:00:00:00:00:01`, the algorithm produces `c60efd543377`. This tests the calculation, **not** any camera login. See the [worked example](../../docs/finding-the-correct-mac.md).
