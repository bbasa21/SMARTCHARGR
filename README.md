# SMARTCHARGR

A Kivy-based Samsung battery precision display with a movable-to-be overlay prototype.

## Build policy

APK builds use only the official `ghcr.io/kivy/buildozer` Docker image through GitHub Actions. No Android Studio or alternate APK builder is used.

## Version 0.2.0

- Reads Samsung `/sys/class/power_supply/battery/batt_read_raw_soc` through `su`.
- Displays the raw-derived percentage with two decimal places.
- Requests Android's special "Display over other apps" permission.
- Adds a floating Android `TYPE_APPLICATION_OVERLAY` text window, updated from the live fuel-gauge reading.
- The overlay is currently tied to the app process and is removed when the app stops; a persistent foreground service is a later step.

## Important limitations

- Fast-charge detection is deliberately not claimed yet. The app does not show an "only while fast charging" behavior until a reliable Samsung A50 indicator is verified.
- Lock-screen visibility is not guaranteed for application overlays on Android 11 / One UI 3.1. A dedicated SystemUI/LSPosed integration is a separate development step.
- Two decimal places are a display format, not a guarantee of 0.01% sensor accuracy. Observed fuel-gauge readings have so far changed in 0.10% steps.

## Build

Pushes to `main` and manual workflow dispatch run the Docker-based Android debug build. The APK is uploaded as a workflow artifact.
