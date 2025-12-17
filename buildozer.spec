[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,mp3,wav,ogg,m4a
version = 2.0

# المكتبات - إصدارات محددة ومستقرة
requirements = python3,kivy==2.2.1,android,pyjnius

# تعريف الخدمة مع نوع foreground
services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

# الأذونات الكاملة (جميع ما نحتاجه)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY

# إعدادات API محسّنة
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# دعم معماريتين للتوافق الأوسع
android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True

# استخدام أحدث إصدار من p4a
p4a.branch = master

# إعدادات إضافية للاستقرار
android.entrypoint = org.kivy.android.PythonActivity
android.app_theme = @android:style/Theme.NoTitleBar

[buildozer]
log_level = 2
warn_on_root = 0
