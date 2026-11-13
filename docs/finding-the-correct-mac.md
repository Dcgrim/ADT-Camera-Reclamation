# Finding the correct camera MAC address

The OC845 offline credential helper uses a **12-hex-digit MAC address** as input. During setup, a camera may expose several different identifiers. **Do not assume the temporary Wi-Fi setup access point's BSSID is the same as the MAC used by the firmware's credential routine.** A MAC visible in a router client list, printed on a sticker, or reported by a camera interface may differ. Which specific interface the firmware uses must be verified for the hardware and firmware being tested.

## Safe identification procedure

1. **Check the physical camera label** for a MAC or wireless MAC. Record it privately alongside the exact model and firmware version, if known.
2. **Connect the camera to your isolated Wi-Fi network** using its normal provisioning flow. Do not confuse the temporary setup hotspot (AP/BSSID) with the camera's station/client MAC on the ranch Wi-Fi.
3. **Open your router's client/DHCP list** (for example, the TP-Link Deco client list). Identify the camera by its device entry and IP address, and record the **client MAC** associated with that lease. Router entries may be stale; refresh/reconnect if needed.
4. **Cross-check on the same LAN**, where possible, with the local ARP/neighbor table. On Linux: `ip neigh show`. On Windows: `arp -a`. These show the link-layer neighbor associated with an IP **on the local segment**; they do not independently prove which MAC is embedded in firmware.
5. **Compare the identifiers.** If the label, DHCP/client MAC, setup AP BSSID, and interface-reported MAC differ, keep each labeled separately. Do not automatically add/subtract 1, change digits, or assume one is 'fake'. Vendors can assign distinct legitimate MACs to separate interfaces.
6. **Verify the candidate using your own camera** and document which source produced the successful result. Only a verified match, or firmware analysis confirming the input interface, establishes the correct value for that device.

### Example (fictional values)

| Source | Example | Meaning |
| --- | --- | --- |
| Camera Wi-Fi client MAC | `02:00:00:00:00:01` | **Illustrative candidate** to test |
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
