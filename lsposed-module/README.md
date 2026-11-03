# SMARTCHARGR SystemUI Probe

This is a diagnostic-only legacy Xposed module intended for the existing LSPosed 1.9.2 installation on the Samsung Galaxy A50 (Android 11 / One UI 3.1).

## Safety

- Scope is limited to `com.android.systemui`.
- It only observes class loading and writes matching class names to the LSPosed log.
- It does not hook battery values, alter views, replace resources, or change charging behavior.
- Disable the module in LSPosed and reboot to stop it.

## Build

The `LSPosed SystemUI Probe APK` GitHub Actions workflow builds `app-debug.apk` and publishes it as `SMARTCHARGR-SystemUI-Probe-debug`.

## Device test

1. Install the APK and enable it in LSPosed.
2. Confirm the only selected scope is System UI (`com.android.systemui`).
3. Reboot the phone.
4. Unlock the phone, open and close Quick Settings, visit the lock screen, and wait briefly.
5. In LSPosed Manager, open the module log and collect lines prefixed with `SMARTCHARGR-PROBE`.

Do not enable this probe for any other package. This build is for class discovery only, not for changing the status bar or lock screen.
