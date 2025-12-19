[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0

# STABLE requirements
requirements = python3==3.10.9,kivy==2.2.1,android,pyjnius

# Service
services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

# Essential permissions only
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS

# STABLE Android settings
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Single arch for speed
android.archs = arm64-v8a

android.allow_backup = True

# IMPORTANT: Use master branch
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
