# OC845 microSD and embedded-Linux investigation

**Status:** Research plan, not a demonstrated SD-card exploit or Linux shell.

## Recorded leads

The camera web interface has been reported to expose `/sd/sdctrl.cgi`, including `action=format` and `action=safe_rm`, an `SDCARD` configuration group, and JavaScript/UI references to SD-card management. A format operation appeared to run, but successful filesystem mounting and recording were **not** established. These observations should be reproduced on a known firmware revision and logged before being labeled verified.

## Three hypotheses to test separately

1. **Detection and mounting:** Is the inserted card detected by the hardware and mounted by the running Linux firmware?
2. **Recovery media:** Does the bootloader recognize a specific microSD recovery image? No boot-from-SD or recovery format has been confirmed.
3. **Execution:** Does the firmware execute scripts or binaries from the card? No autorun or arbitrary execution behavior has been confirmed.

## Initial non-destructive experiment

On an owner-controlled test camera, record the model, firmware build, SD-card capacity/filesystem, and current UI state. Compare status before insertion, after insertion, and after a normal camera restart. Query available read-only SD-card status/configuration controls and record HTTP status and sanitized responses. Do **not** trigger format, firmware upload, or bootloader operations during this first experiment. If a format test is later approved, use an expendable card and document data-loss risk.

## Evidence ledger

| Claim | Status | Evidence needed |
|---|---|---|
| SD-card management route exists | Reported from UI/source inspection | Saved firmware/version-specific HTTP or HTML evidence |
| Camera recognizes inserted card | Unconfirmed | Status before/after insertion |
| Linux mounts the card | Unconfirmed | Mount status or equivalent reliable observation |
| Bootloader loads SD recovery image | Unconfirmed | Boot logs and documented recovery behavior |
| Firmware executes files from SD | Unconfirmed | Controlled proof on isolated device |

## Attribution

Primary external background: Nathan Higley (`astr0n8t`), [*Hacking Cheap IoT Cameras for Fun and No Profit*](https://blog.nathanhigley.com/iotcamerahacking/), 14 October 2025. His documented UART/Amboot and firmware work is not evidence of an SD-card exploit. Credit his work for the firmware research foundation, and distinguish our SD observations and future experiments as separate contributions.