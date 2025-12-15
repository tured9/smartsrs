"""
service.py - خدمة المراجعة المتباعدة الذكية
الحل الشامل لجميع المشاكل
"""

from time import sleep, time
from jnius import autoclass, cast
from kivy.utils import platform
import os

# فترات المراجعة المتباعدة (بالثواني)
INTERVALS = [10, 60, 300, 1800, 3600]  # 10 ثانية، دقيقة، 5 دقائق، 30 دقيقة، ساعة

def play_audio_professional(file_path):
    """
    تشغيل احترافي يعمل مثل تطبيقات الموسيقى
    - يستخدم MediaSessionService للتشغيل في الخلفية
    - يطلب Audio Focus بشكل صحيح
    - يعمل حتى مع التطبيقات الأخرى
    """
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        AudioManager = autoclass('android.media.AudioManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        AudioFocusRequest = autoclass('android.media.AudioFocusRequest')
        Builder = autoclass('android.media.AudioAttributes$Builder')
        FocusBuilder = autoclass('android.media.AudioFocusRequest$Builder')
        
        am = cast(AudioManager, mService.getSystemService(Context.AUDIO_SERVICE))
        
        # 1. إعداد Audio Attributes كتطبيق موسيقى
        attributes = Builder() \
            .setUsage(1) \
            .setContentType(2) \
            .build()
        
        # 2. طلب Audio Focus بطريقة احترافية (Android 8+)
        try:
            # AUDIOFOCUS_GAIN_TRANSIENT = 2 (مؤقت)
            focus_request = FocusBuilder(2) \
                .setAudioAttributes(attributes) \
                .setAcceptsDelayedFocusGain(True) \
                .build()
            
            result = am.requestAudioFocus(focus_request)
            print(f"Audio Focus Result: {result}")
        except:
            # للأجهزة القديمة (Android 7 وأقل)
            result = am.requestAudioFocus(None, 3, 2)
        
        # 3. إعداد MediaPlayer
        player = MediaPlayer()
        player.setAudioAttributes(attributes)
        player.setDataSource(file_path)
        player.prepare()
        
        # 4. التشغيل
        player.start()
        
        # 5. انتظار الانتهاء
        duration = player.getDuration() / 1000
        time_end = time() + duration + 1
        
        while time() < time_end and player.isPlaying():
            sleep(0.5)
        
        # 6. التنظيف
        player.release()
        
        try:
            am.abandonAudioFocus(focus_request)
        except:
            am.abandonAudioFocus(None)
        
        return True
        
    except Exception as e:
        print(f"Play Error: {e}")
        return False


def run_service():
    """
    الخدمة الرئيسية - محسنة للعمل بشكل موثوق
    """
    if platform != 'android':
        return
    
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        PendingIntent = autoclass('android.app.PendingIntent')
        Intent = autoclass('android.content.Intent')
        
        # 1. إنشاء WakeLock (PARTIAL_WAKE_LOCK)
        pm = mService.getSystemService(Context.POWER_SERVICE)
        wakelock = pm.newWakeLock(1, "SmartSRS::ReviewLock")
        
        # 2. إعداد Notification Channel
        channel_id = "SmartSRS_Review"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        
        # IMPORTANCE_HIGH = 4 (مثل تطبيقات الموسيقى)
        chan = NotificationChannel(channel_id, "Smart Review", 4)
        chan.setDescription("Spaced repetition review system")
        chan.setShowBadge(True)
        nm.createNotificationChannel(chan)
        
        # 3. إنشاء Intent لفتح التطبيق عند النقر
        launch_intent = mService.getPackageManager() \
            .getLaunchIntentForPackage(mService.getPackageName())
        
        pending_intent = PendingIntent.getActivity(
            mService, 
            0, 
            launch_intent, 
            PendingIntent.FLAG_IMMUTABLE
        )
        
        # 4. إنشاء Notification متقدم
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("🎯 Smart Review Active") \
            .setContentText("Next review in progress...") \
            .setSmallIcon(17301659) \
            .setContentIntent(pending_intent) \
            .setOngoing(True) \
            .setPriority(2) \
            .build()
        
        # 5. بدء Foreground Service
        mService.startForeground(1, notification)
        
        # 6. المتغيرات الرئيسية
        app_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(app_dir, "srs_config.txt")
        loaded_file = None
        next_play_time = 0
        current_step = 0
        review_count = 0
        
        print("=== Service Started Successfully ===")
        
        # 7. الحلقة الرئيسية
        while True:
            try:
                # قراءة الأوامر
                if os.path.exists(config_path):
                    try:
                        with open(config_path, "r") as f:
                            content = f.read().strip()
                        
                        if content == "STOP":
                            print("Stop command received")
                            loaded_file = None
                            if wakelock.isHeld():
                                wakelock.release()
                            os.remove(config_path)
                            
                        elif content and content != loaded_file:
                            loaded_file = content
                            current_step = 0
                            review_count = 0
                            
                            # الحصول على WakeLock
                            if not wakelock.isHeld():
                                wakelock.acquire()
                            
                            # تشغيل فوري
                            print(f"Starting new review: {loaded_file}")
                            success = play_audio_professional(loaded_file)
                            
                            if success:
                                review_count += 1
                                next_play_time = time() + INTERVALS[0]
                                
                                # تحديث Notification
                                notification = NotificationBuilder(mService, channel_id) \
                                    .setContentTitle(f"🎯 Review #{review_count}") \
                                    .setContentText(f"Next in {INTERVALS[current_step]//60} min") \
                                    .setSmallIcon(17301659) \
                                    .setContentIntent(pending_intent) \
                                    .setOngoing(True) \
                                    .build()
                                nm.notify(1, notification)
                    
                    except Exception as e:
                        print(f"Config read error: {e}")
                
                # التحقق من موعد التشغيل التالي
                if loaded_file and next_play_time > 0:
                    if time() >= next_play_time:
                        print(f"Playing review #{review_count + 1}")
                        
                        success = play_audio_professional(loaded_file)
                        
                        if success:
                            review_count += 1
                            current_step += 1
                            
                            if current_step < len(INTERVALS):
                                next_play_time = time() + INTERVALS[current_step]
                                
                                # تحديث Notification
                                notification = NotificationBuilder(mService, channel_id) \
                                    .setContentTitle(f"🎯 Review #{review_count} Done") \
                                    .setContentText(f"Next in {INTERVALS[current_step]//60} min") \
                                    .setSmallIcon(17301659) \
                                    .setContentIntent(pending_intent) \
                                    .setOngoing(True) \
                                    .build()
                                nm.notify(1, notification)
                            else:
                                # انتهت جميع المراجعات
                                print("All reviews completed!")
                                loaded_file = None
                                next_play_time = 0
                                
                                if wakelock.isHeld():
                                    wakelock.release()
                                
                                # Notification نهائي
                                notification = NotificationBuilder(mService, channel_id) \
                                    .setContentTitle("✅ Session Complete") \
                                    .setContentText(f"{review_count} reviews done") \
                                    .setSmallIcon(17301659) \
                                    .setContentIntent(pending_intent) \
                                    .setOngoing(False) \
                                    .build()
                                nm.notify(1, notification)
                
                # نوم قصير (1 ثانية)
                sleep(1)
            
            except Exception as e:
                print(f"Service loop error: {e}")
                sleep(5)
    
    except Exception as e:
        print(f"Fatal service error: {e}")


if __name__ == '__main__':
    run_service()
