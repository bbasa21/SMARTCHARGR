[app]

title = SMARTCHARGR
package.name = smartchargr
package.domain = com.bbasa21
source.dir = .
source.include_exts = py,kv,png,jpg,atlas,json,txt
version = 0.2.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 24
android.ndk = 28c
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = False
android.private_storage = True
android.permissions = SYSTEM_ALERT_WINDOW

[buildozer]
log_level = 2
warn_on_root = 1
