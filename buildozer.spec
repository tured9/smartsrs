[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,mp3,wav,ogg,m4a
version = 4.0

# المتطلبات
requirements = python3,kivy==2.2.1,android,pyjnius

# الخدمة
services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

# الأذونات الكاملة
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM

# إعدادات Android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

# إعدادات متقدمة
android.manifest_placeholders = {"USE_EXACT_ALARM": "true", "SCHEDULE_EXACT_ALARM": "true"}
android.entrypoint = org.kivy.android.PythonActivity

# --- هذا السطر هو الأهم: استخدام نسخة المطورين من P4A ---
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
