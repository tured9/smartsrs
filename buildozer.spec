[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0

# Requirements
requirements = python3,kivy==2.2.1,android,pyjnius

# Service
services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

# Permissions for Android 14
android.permissions = INTERNET,READ_MEDIA_AUDIO,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,FOREGROUND_SERVICE_MEDIA_PLAYBACK,POST_NOTIFICATIONS,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM

# Android 14 compatible settings
android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

# arm64 only (your phone is Unisoc T603)
android.archs = arm64-v8a

android.allow_backup = True

# Android 14 needs this
android.gradle_dependencies = androidx.core:core:1.12.0

# Use master
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
