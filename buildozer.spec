[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,mp3,wav,ogg,m4a
version = 3.0

# ثابت ومستقر مع p4a r25b
requirements = python3,kivy==2.1.0,pyjnius

services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM

android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# نبدأ ببناء arm64 أولاً ثم نوسّع إذا نجح
android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True

android.entrypoint = org.kivy.android.PythonActivity
android.app_theme = @android:style/Theme.NoTitleBar

[buildozer]
log_level = 2
warn_on_root = 0
