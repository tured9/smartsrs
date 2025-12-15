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

# الأذونات القوية (إضافة POST_NOTIFICATIONS وFOREGROUND_SERVICE_MEDIA_PLAYBACK)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,POST_NOTIFICATIONS,FOREGROUND_SERVICE_MEDIA_PLAYBACK

# إعدادات أندرويد التقنية
android.api = 34
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

# منع شاشة الانتظار من الظهور طويلاً
android.presplash_color = #1f2330

# hook لتعديل Manifest تلقائيًا أثناء البناء (سيضيف foregroundServiceType)
p4a.hook = hook.py

[buildozer]
log_level = 2
warn_on_root = 1
