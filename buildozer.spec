[app]
title = SmartSRS
package.name = smartsrs
package.domain = org.mysrs
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0
requirements = python3,kivy,android,pyjnius,Cython==0.29.33
services = SRSService:service.py
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,MODIFY_AUDIO_SETTINGS,ACCESS_NOTIFICATION_POLICY,POST_NOTIFICATIONS,FOREGROUND_SERVICE_MEDIA_PLAYBACK,READ_MEDIA_AUDIO
android.api = 34
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True
android.presplash_color = #1f2330
p4a.hook = hook.py
[buildozer]
log_level = 2
warn_on_root = 1
