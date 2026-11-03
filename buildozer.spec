[app]

title = SMARTCHARGR
package.name = smartchargr
package.domain = com.bbasa21
source.dir = .
source.include_exts = py,kv,png,jpg,atlas,json,txt
version = 0.1.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

# Android target for the first Samsung ARM64 prototype.
android.api = 35
android.minapi = 23
android.ndk = 28c
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = False
android.private_storage = True

# Keep the first build minimal. Overlay and boot permissions will be added
# only when their Android-side implementation is ready.

[buildozer]
log_level = 2
warn_on_root = 1
