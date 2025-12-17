[app]
# الاسم والإعدادات الأساسية
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,mp3,wav,ogg,m4a
version = 3.1

# المتطلبات (تحديد Kivy مهم)
requirements = python3,kivy==2.2.1,android,pyjnius

# تعريف الخدمة
services = SRSService:service.py

# الشاشة
orientation = portrait
fullscreen = 0

# الأذونات الكاملة (للمنبه والخدمة)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM

# إعدادات Android (33 هو الأكثر استقراراً مع Kivy حالياً)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

# خيارات متقدمة
android.manifest_placeholders = {"USE_EXACT_ALARM": "true", "SCHEDULE_EXACT_ALARM": "true"}
android.entrypoint = org.kivy.android.PythonActivity
# إزالة التحديد اليدوي لـ p4a branch ليعمل تلقائياً
# p4a.branch = stable

[buildozer]
log_level = 2
warn_on_root = 1
