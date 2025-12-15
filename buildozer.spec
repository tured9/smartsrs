[app]
# اسم التطبيق والحزمة
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

# الإصدار
version = 1.0

# المكتبات الضرورية (pyjnius هو الجسر للنظام)
requirements = python3,kivy,android,pyjnius

# تعريف الخدمة الخلفية (هذا السطر هو الأهم)
services = SRSService:service.py

# إعدادات الشاشة
orientation = portrait
fullscreen = 0

# الأذونات القوية (لاحظ إذن FOREGROUND_SERVICE)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY

# إعدادات أندرويد التقنية
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

# منع شاشة الانتظار من الظهور طويلاً
android.presplash_color = #1f2330

[buildozer]
log_level = 2
warn_on_root = 1
