[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 0.6
# المكتبات المطلوبة
requirements = python3,kivy,android,pyjnius

# تعريف الخدمة الخلفية
services = SRSService:service.py

orientation = portrait
fullscreen = 0

# --- التعديل الهام هنا (الأذونات الجديدة) ---
# MODIFY_AUDIO_SETTINGS: للتحكم في رفع الصوت
# ACCESS_NOTIFICATION_POLICY: للتعامل مع وضع عدم الإزعاج
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY

android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
