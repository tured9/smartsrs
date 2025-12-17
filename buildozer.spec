[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,mp3,wav,ogg,m4a

version = 3.5
requirements = python3,kivy==2.2.1,android,pyjnius

# الخدمة تعمل في المقدمة
services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

# الأذونات الكاملة (المنبه، الصوت، الخدمة)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM

# استهداف أندرويد 13 (الأكثر استقراراً)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

# إعدادات متقدمة للمنبه
android.manifest_placeholders = {"USE_EXACT_ALARM": "true", "SCHEDULE_EXACT_ALARM": "true"}
android.entrypoint = org.kivy.android.PythonActivity

# استخدام نسخة المطورين لحل مشاكل البناء
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
