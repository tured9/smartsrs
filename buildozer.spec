[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,mp3,wav,ogg,m4a
version = 3.0

# استخدام نسخة مستقرة ومتوافقة
requirements = python3,kivy==2.1.0,pyjnius

# Service with foreground type
services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM

# API / NDK
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Architectures: لاحقًا يمكنك تفعيل الثانية بعد نجاح الأولى
android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True

# لا تعتمد على p4a.branch هنا — سيتم تثبيت نسخة محددة من p4a في الـ workflow
# p4a.branch = master

# Additional stability
android.entrypoint = org.kivy.android.PythonActivity
android.app_theme = @android:style/Theme.NoTitleBar

[buildozer]
log_level = 2
warn_on_root = 0
