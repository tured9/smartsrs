[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 0.5
# إضافة مكتبات التعامل مع الطاقة والنظام
requirements = python3,kivy,android,pyjnius

# تعريف الخدمة
services = SRSService:service.py

orientation = portrait
fullscreen = 0
# الأذونات الكاملة لمشغل وسائط يعمل في الخلفية
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
# منع ضغط الصور للحفاظ على الجودة
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
