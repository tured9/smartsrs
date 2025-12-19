[app]

# (str) Title of your application
title = Spaced Audio Repetition

# (str) Package name
package.name = spacedaudio

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy==master,pyjnius,plyer

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
services = audioservice:service/main.py:foreground

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# Android specific

# (list) Permissions
android.permissions = WAKE_LOCK,FOREGROUND_SERVICE,SCHEDULE_EXACT_ALARM,USE_EXACT_ALARM,VIBRATE,INTERNET

# (bool) Enable wakelock
android.wakelock = True

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25e

# (int) Android NDK API
android.ndk_api = 24

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity
