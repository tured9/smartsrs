[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,mp3,wav,ogg,m4a
version = 3.0

# متوافق ومستقر
requirements = python3,kivy==2.2.1,pyjnius

services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

# ===== كل الأذونات بدون استثناء =====
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM

# ===== إعدادات Android الصحيحة =====
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# ابدأ بمعمارية واحدة (مهم جدًا)
android.archs = arm64-v8a

android.allow_backup = True

# REQUIRED مع الأذونات الحساسة
android.manifest_placeholders = \
  USE_EXACT_ALARM=true, \
  SCHEDULE_EXACT_ALARM=true

# REQUIRED مع Foreground Service
android.foreground_service_types = mediaPlayback,dataSync,location

android.entrypoint = org.kivy.android.PythonActivity
android.app_theme = @android:style/Theme.NoTitleBar

# يمنع مشاكل git و python-for-android
p4a.branch = stable

[buildozer]
log_level = 2
warn_on_root = 0
