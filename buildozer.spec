[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.2
# هنا كان الخطأ: أضفنا pyjnius و android
requirements = python3,kivy,android,pyjnius

orientation = portrait
fullscreen = 0
# تأكدنا من كافة الأذونات
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
