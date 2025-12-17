[app]
# الاسم
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

# الإصدار
version = 1.0

# المتطلبات (لاحظ إضافة android و pyjnius)
requirements = python3,kivy,android,pyjnius

# تعريف الخدمة (المحرك الخلفي)
services = SRSService:service.py

# الشاشة
orientation = portrait
fullscreen = 0

# الأذونات (شاملة)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,POST_NOTIFICATIONS

# إعدادات أندرويد (نستهدف 33 للاستقرار)
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

# شاشة البداية
android.presplash_color = #1f2330

[buildozer]
log_level = 2
warn_on_root = 1
