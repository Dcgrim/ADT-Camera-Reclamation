# Finding the correct camera MAC address

The OC845 offline credential helper uses a **12-hex-digit MAC address** as input. During setup, a camera may expose several different identifiers. **Do not assume the temporary Wi-Fi setup access point's BSSID is the same as the MAC used by the firmware's credential routine.** A MAC visible in a router client list, printed on a sticker, or reported by a camera interface may differ. Which specific interface the firmware uses must be verified for the hardware and firmware being tested.

## Identify the address without relying on a particular router

The camera may show a **changing or apparently dynamic MAC-like identifier** during normal discovery or provisioning. The original operator recalls needing to dig deeper, possibly while connected to the camera's own setup access point (AP), to find the identifier that worked for credential derivation. **That recollection is a research lead, not yet a verified step-by-step procedure.**

1. **Check the physical label.** A printed MAC may be twelve hexadecimal characters with no punctuation (for example `A1B2C3D4E5F6`). This is the same length as `A1:B2:C3:D4:E5:F6`, just written without separators. Note the label value privately, but don't assume it is the credential input until tested.
2. **Check your router or access point's connected-device list.** Any brand is fine: look for a page named *Connected devices*, *Clients*, *DHCP leases*, *Device list*, or similar. Match the camera's local IP to the associated client MAC. Some systems randomize or display virtual MAC addresses.
3. **Inspect the camera's temporary setup Wi-Fi/AP separately.** During authorized provisioning, record its advertised BSSID and any identifiers visible in the local setup interface. The operator recalls this being a useful discovery stage on the first OC845, but the exact method still needs reproduction.
4. **Cross-check from a computer on the same local network.** On Linux, run `ip neigh show`; on Windows, run `arp -a`. Neighbor tables associate an IP with a link-layer address, but don't prove which identifier the camera firmware uses internally.
5. **Keep the sources distinct.** Label each candidate as *sticker*, *router/DHCP*, *setup AP/BSSID*, or *device interface*. Do not assume that a changing advertised identifier is necessarily the hardware MAC, or that a different identifier is fake.
6. **Test the candidate against your own camera** using the offline helper. Record which identifier source succeeds, with firmware version and test conditions. A successful login is stronger evidence than a visual match alone.

### Twelve hex digits versus twelve password characters

A conventional 48-bit MAC address is **12 hexadecimal digits** regardless of punctuation. The OC845 algorithm strips punctuation and derives a **different** 12-character hexadecimal password. A shorter-looking string on a label may simply be the MAC without colons.

### What remains to verify

- Whether the changing advertised identifier is genuinely randomized, a different interface's MAC, or another discovery identifier.
- Whether the camera's printed MAC, setup AP identifier, or another internal MAC is the reliable input for the tested firmware.
- The exact setup-AP steps used in the original first-camera discovery.

Until reproduced, this document deliberately does not claim one universal 'real MAC' discovery trick.

### Example (fictional values)

| Source | Example | Meaning |
| --- | --- | --- |
| Candidate camera MAC | `02:00:00:00:00:01` | **Illustrative candidate**; source must be verified |
| Setup AP BSSID | `02:00:00:00:00:02` | A separate illustrative interface identifier |
| Camera LAN IP | `192.0.2.10` | Documentation-only example address |

**None of these example values belongs to a real camera.** `02:` is a locally administered MAC prefix and `192.0.2.0/24` is reserved for documentation.

## Worked example of the OC845 derivation

Given fictional MAC `02:00:00:00:00:01`:

1. Remove colons and uppercase: `020000000001`.
2. Append the firmware-derived ASCII constant: `06D58FFA826502BA52D3317A95169346`.
3. Compute SHA-1 of the concatenated **ASCII text**, not decoded hexadecimal bytes.
4. Take the first 12 lowercase hex characters.

Result: `c60efd543377`.

Reproduce locally:

```python
import hashlib

mac = "02:00:00:00:00:01"  # fictional, locally administered MAC
constant = "06D58FFA826502BA52D3317A95169346"
normalized = mac.replace(":", "").replace("-", "").upper()
candidate = hashlib.sha1((normalized + constant).encode("ascii")).hexdigest()[:12]
assert candidate == "c60efd543377"
print(candidate)
```

This test vector verifies the **software calculation only**. It does **not** establish that a particular camera uses that MAC, that the RC845 shares the mechanism, or that the candidate will authenticate to any camera.

Keep real identifiers, passwords, and RTSP URLs out of public GitHub issues and screenshots.
