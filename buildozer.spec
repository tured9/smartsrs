[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,mp3,wav,ogg,m4a
version = 1.0

# Requirements - EXACT versions
requirements = python3,kivy==2.2.1,android,pyjnius

# Services
services = SRSService:service.py:foreground

# Orientation
orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM,FOREGROUND_SERVICE_MEDIA_PLAYBACK

# Android Settings - STABLE versions
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Architecture - Single for faster build
android.archs = arm64-v8a

# Advanced Settings
android.allow_backup = True
android.entrypoint = org.kivy.android.PythonActivity

# --- CRITICAL FIX ---
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
