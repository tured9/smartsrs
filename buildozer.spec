# buildozer.spec -- SmartSRS (Kivy + pyjnius) کامل
# انسخ الملف التالي كما هو واحفظه باسم buildozer.spec

[app]

# (معلومات عامة للتطبيق)
title = SmartSRS
package.name = smartsrs
package.domain = org.example
version = 0.1
orientation = portrait
fullscreen = 0

# ملفات المصدر التي سيتم تضمينها في الحزمة
source.dir = .
# امتدادات الملفات التي تُضمّن تلقائياً
source.include_exts = py,png,jpg,kv,mp3,wav,txt,md,xml

# ضع هنا اسم أي ملف أيقونة لو لديك
# icon.filename = %(source.dir)s/data/icon.png

# Python requirements (ضروري: kivy و pyjnius لتشغيل service على Android)
requirements = python3,kivy,pyjnius

# Use the stable p4a branch
p4a.branch = stable

# ضبط ABI (يفضل تضمين arm64 لحداثة الأجهزة)
android.arch = armeabi-v7a, arm64-v8a

# Android API / min API
android.api = 33
android.minapi = 26

# لا تحدد ndk.version إلا إذا تعرف ما تفعل؛ نترك الافتراضات الافتراضية
# android.ndk = 25b

# Permissions المطلوبة (مهمة جداً للتشغيل في الخلفية وتشغيل الصوت من التخزين)
android.permissions = WAKE_LOCK, FOREGROUND_SERVICE, RECEIVE_BOOT_COMPLETED, MODIFY_AUDIO_SETTINGS, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, READ_MEDIA_AUDIO

# Services: ربط service.py كسيرفيس داخل الـ APK
# التنسيق: <service_name>:<relative/path/to/service.py>
# سوف يقوم buildozer بإدراج هذا الملف كسيرفيس يمكن تشغيله من الكود
android.services = smartsrs_service:service.py

# تضمين ملفات إضافية (في حال أردت تضمين مجلدات كاملة)
# source.include_patterns = assets/*, images/*

# Add extra Java packages or gradle dependencies if needed (حاليًا لا حاجة)
# android.gradle_dependencies = 'com.android.support:appcompat-v7:26.+'

# Icons / resources / presplash (اختر إن لزم)
# presplash.filename = %(source.dir)s/data/presplash.png

# Packaging
android.release = False
# whether to enable aaab (bundle) building; false => apk
# android.bundle = False

# Buildozer behaviour
log_level = 2
warn_on_root = 1

# (Optional) if تستخدم ملفات كبيرة، زد timeout
# android.bootstrap = sdl2

[buildozer]
# الصيغة هنا تختصر خيارات buildozer العامة
# يمكنك تركها كما هي أو تغيير المسار إلى مجلد .buildozer
# build_dir = ./.buildozer

# تكوين إضافي (إن أردت تضمين ملفات native أو Java sources)
# android.add_src = ./android/src

# --- نهاية الملف ---
