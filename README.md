# SMARTCHARGR

A Kivy-based Android battery precision display for Samsung devices.

## Build policy

APK builds use the official `ghcr.io/kivy/buildozer` Docker image through GitHub Actions. No Android Studio or alternate APK builder is used.

## Current prototype

- Reads Samsung's `/sys/class/power_supply/battery/batt_read_raw_soc` through `su`.
- Displays the raw-derived percentage with two decimal places.
- Uses a blue/white Kivy interface.

**Measurement note:** two decimal places are a display format, not a guarantee of 0.01% sensor accuracy. The observed gauge readings have so far changed in 0.10% steps.

## Roadmap

1. Build and install a baseline APK.
2. Verify root access and live battery readings inside the packaged APK.
3. Add charging-state and Samsung fast-charging detection based on verified device data.
4. Prototype a movable overlay using Android APIs from the Kivy app.
5. Investigate the separate SystemUI integration needed for a true Status Bar / Lock Screen percentage replacement. A normal Kivy window cannot directly replace Samsung SystemUI text.

## Build

Pushes to `main` and manual workflow dispatch run the Docker-based Android debug build. The APK is uploaded as a workflow artifact.
