[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0

# Requirements - STABLE versions
requirements = python3,kivy==2.2.1,android,pyjnius

# Service
services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM

# Android settings - API 31 (STABLE!)
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Single architecture for faster build
android.archs = arm64-v8a

android.allow_backup = True

# Use master branch
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
