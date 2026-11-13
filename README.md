# ADT Camera Reclamation
### Taking back control of cameras you already own

Research, documentation, and local-first tools for repurposing **ADT OC845 outdoor** and **RC845 indoor** IP cameras without relying on a vendor cloud.

> **Project status:** Active research. OC845 local access has been demonstrated on the project owner's equipment. RC845 support is being investigated separately; compatibility is **not** assumed.

## Why this exists

A functioning camera should not become e-waste just because a subscription ends or a vendor stops supporting it. This project documents what can be verified about these devices and builds practical tools to use them on a network you control.

**Goals**
- Recover and document local camera access on personally owned devices.
- View supported video streams through standard local software.
- Publish reproducible research, scripts, and troubleshooting notes.
- Preserve working firmware and configurations before changing anything.
- Distinguish tested behavior from hypotheses, especially across models and firmware revisions.

## Hardware and status

| Model | Form factor | Current project status |
| --- | --- | --- |
| **OC845** | Outdoor IP camera | Local access and RTSP use demonstrated on project devices; research and tooling in progress |
| **RC845** | Indoor IP camera | Identified as an additional research target; firmware, authentication, and stream compatibility still need independent validation |

**Do not assume the RC845 shares the OC845's credentials, firmware, recovery method, or endpoints.**

## What we've learned so far

On the tested OC845 devices, research identified a **MAC-dependent local credential derivation mechanism** and enabled local RTSP access. The project maintains an offline credential-recovery utility for authorized owners, along with a local camera dashboard and operational notes.

The recovery method is **firmware/model-specific until proven otherwise**. We will publish the implementation and test methodology with appropriate caveats, rather than claim universal compatibility.

The owner's working setup includes a local multi-camera dashboard on a Linux workstation. Public examples will use placeholders and sanitized configuration data.

## Planned repository layout

```text
ADT-Camera-Reclamation/
├── README.md
├── docs/
│   ├── OC845-research.md
│   ├── finding-the-correct-mac.md
│   ├── RC845-research.md
│   └── sd-card-investigation.md
├── tools/
│   └── oc845-password-recovery/
│       ├── README.md
│       └── camera_app.py
└── .gitignore
```

*These research documents and the offline helper are now committed. The multi-camera dashboard is still being prepared for a safe public release.*

## Get started

- [OC845 research and findings](docs/OC845-research.md)
- [Find the correct camera MAC and follow a fictional worked example](docs/finding-the-correct-mac.md)
- [Offline OC845 helper — installation and usage](tools/oc845-password-recovery/README.md)
- [Python application source](tools/oc845-password-recovery/camera_app.py)
- [RC845 indoor model research tracker](docs/RC845-research.md)
- [microSD investigation](docs/sd-card-investigation.md)

## Research roadmap

- [x] Identify and test OC845 local-access behavior on owned cameras
- [x] Demonstrate local video viewing on the tested OC845 setup
- [x] Publish a sanitized offline OC845 recovery utility (runtime testing still recommended)
- [x] Publish initial field research and helper setup instructions (more troubleshooting to come)
- [ ] Document the RC845's firmware and local interfaces independently
- [ ] Investigate microSD configuration and recovery behavior without destructive flashing
- [ ] Package the local multi-camera dashboard for repeatable installation
- [ ] Record firmware/version compatibility and known limitations

## Safety, scope, and privacy

This repository is intended for **devices you own or are expressly authorized to administer**. Work on an isolated or trusted network, back up configurations first, and understand that firmware modifications can permanently disable hardware.

Some camera firmware may derive predictable credentials from publicly observable identifiers. Treat that as a security weakness: **do not expose camera management or RTSP services to the public internet**. Segment these devices where practical.

No real camera MAC addresses, derived passwords, private IP addresses, authentication tokens, or identifiable video footage belong in public examples. Contributions should be sanitized before submission.

## Credit and prior work

A major inspiration and technical starting point is **Nathan Higley's** article:

**[Hacking Cheap IoT Cameras for Fun and No Profit](https://blog.nathanhigley.com/iotcamerahacking/)**

Nathan's published investigation of inexpensive IoT cameras and the ADT camera ecosystem helped inform the direction of this work. We want to make that lineage clear and distinguish his original findings from our own tests, extensions, and tools. This repository is independent and does not imply his endorsement.

## Contributing

Have an OC845 or RC845 with a different firmware version? Reproduced a result? Found a safer recovery path? Issues and pull requests are welcome. Please include the exact model, firmware version (if known), steps to reproduce, and **redacted** logs. Avoid posting live credentials or identifying network details.

## Project philosophy

**Repair it. Understand it. Document it. Keep it useful.**

The camera is hardware you bought. The goal is to make it useful for as long as the hardware itself lasts.

---

*Independent community research. Not affiliated with or endorsed by ADT or the camera manufacturer. Product names are used for identification.*
