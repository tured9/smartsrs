[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,wav,mp3,ogg,m4a
version = 1.0

# المكتبات
requirements = python3,kivy,android,pyjnius

# تعريف الخدمة
services = SRSService:service.py:foreground

orientation = portrait
fullscreen = 0

# الأذونات الكاملة (مثل تطبيقات الموسيقى)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,FOREGROUND_SERVICE_MEDIA_PLAYBACK,POST_NOTIFICATIONS,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY

# نوع الخدمة (مهم جداً في Android 14+)
android.service_class_name = org.mysrs.smartsrs.ServiceSrsservice
android.meta_data = android.app.services.FOREGROUND_SERVICE_TYPE=mediaPlayback

android.api = 33
android.minapi = 26
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

# لجعل الخدمة تعمل بشكل موثوق
android.gradle_dependencies = androidx.work:work-runtime:2.8.1

[buildozer]
log_level = 2
warn_on_root = 1
