from time import sleep, time
from jnius import autoclass, cast
from kivy.utils import platform
import os

# الفترات الزمنية (بالثواني)
INTERVALS = [5, 20, 30 , 40, 120]

def play_audio(file_path):
    """تشغيل الصوت مع معالجة أخطاء أفضل"""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        AudioManager = autoclass('android.media.AudioManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        
        am = cast(AudioManager, mService.getSystemService(Context.AUDIO_SERVICE))
        
        # طلب Audio Focus
        result = am.requestAudioFocus(None, 3, 2)
        print(f"Audio Focus Request: {result}")
        
        player = MediaPlayer()
        player.setDataSource(file_path)
        player.prepare()
        player.start()
        
        # الانتظار حتى ينتهي التشغيل
        duration = player.getDuration() / 1000
        end_time = time() + duration + 1
        
        while time() < end_time and player.isPlaying():
            sleep(0.5)
        
        player.stop()
        player.release()
        am.abandonAudioFocus(None)
        
        print("Audio played successfully")
        return True
        
    except Exception as e:
        print(f"Play error: {e}")
        return False

def run_service():
    """الخدمة الرئيسية مع معالجة أفضل"""
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
        
        # WakeLock محسّن
        pm = mService.getSystemService(Context.POWER_SERVICE)
        wakelock = pm.newWakeLock(
            PowerManager.PARTIAL_WAKE_LOCK,
            "SmartSRS::ReviewLock"
        )
        wakelock.setReferenceCounted(False)
        
        # Notification قوي
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        chan = NotificationChannel("SmartSRS", "Smart Review", 4)
        chan.setDescription("Spaced repetition review")
        chan.setShowBadge(True)
        nm.createNotificationChannel(chan)
        
        notification = NotificationBuilder(mService, "SmartSRS") \
            .setContentTitle("🎯 Smart Review Active") \
            .setContentText("Background review running") \
            .setSmallIcon(17301659) \
            .setOngoing(True) \
            .setPriority(2) \
            .build()
        
        mService.startForeground(1, notification)
        
        # المتغيرات
        app_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(app_dir, "srs_config.txt")
        loaded_file = None
        next_play_time = 0
        current_step = 0
        review_count = 0
        
        print("=== Service Started ===")
        
        # الحلقة الرئيسية
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
                            next_play_time = 0
                            current_step = 0
                            
                            if wakelock.isHeld():
                                wakelock.release()
                            
                            os.remove(config_path)
                            
                            # إشعار الإيقاف
                            notification = NotificationBuilder(mService, "SmartSRS") \
                                .setContentTitle("⏹️ Stopped") \
                                .setContentText(f"Completed {review_count} reviews") \
                                .setSmallIcon(17301659) \
                                .setOngoing(False) \
                                .build()
                            nm.notify(1, notification)
                            
                            review_count = 0
                        
                        elif content and content != loaded_file:
                            print(f"New file loaded: {content}")
                            loaded_file = content
                            current_step = 0
                            review_count = 0
                            
                            # الحصول على WakeLock
                            if not wakelock.isHeld():
                                wakelock.acquire()
                                print("WakeLock acquired")
                            
                            # تشغيل فوري
                            success = play_audio(loaded_file)
                            
                            if success:
                                review_count += 1
                                next_play_time = time() + INTERVALS[current_step]
                                
                                print(f"Review #{review_count} played")
                                print(f"Next review in {INTERVALS[current_step]} seconds")
                                
                                # تحديث الإشعار
                                notification = NotificationBuilder(mService, "SmartSRS") \
                                    .setContentTitle(f"🎯 Review #{review_count} Done") \
                                    .setContentText(f"Next in {INTERVALS[current_step]//60} min") \
                                    .setSmallIcon(17301659) \
                                    .setOngoing(True) \
                                    .setPriority(2) \
                                    .build()
                                nm.notify(1, notification)
                            else:
                                print("First play failed")
                    
                    except Exception as e:
                        print(f"Config read error: {e}")
                
                # التحقق من موعد التشغيل التالي
                if loaded_file and next_play_time > 0:
                    current_time = time()
                    
                    if current_time >= next_play_time:
                        # تأكد من WakeLock
                        if not wakelock.isHeld():
                            wakelock.acquire()
                            print("WakeLock re-acquired")
                        
                        print(f"Playing review #{review_count + 1}")
                        
                        success = play_audio(loaded_file)
                        
                        if success:
                            review_count += 1
                            current_step += 1
                            
                            if current_step < len(INTERVALS):
                                next_play_time = time() + INTERVALS[current_step]
                                
                                print(f"Review #{review_count} done")
                                print(f"Next in {INTERVALS[current_step]} seconds")
                                
                                # تحديث الإشعار
                                notification = NotificationBuilder(mService, "SmartSRS") \
                                    .setContentTitle(f"🎯 Review #{review_count} Done") \
                                    .setContentText(f"Next in {INTERVALS[current_step]//60} min") \
                                    .setSmallIcon(17301659) \
                                    .setOngoing(True) \
                                    .setPriority(2) \
                                    .build()
                                nm.notify(1, notification)
                            else:
                                # انتهت جميع المراجعات
                                print(f"All {review_count} reviews completed!")
                                
                                loaded_file = None
                                next_play_time = 0
                                current_step = 0
                                
                                if wakelock.isHeld():
                                    wakelock.release()
                                    print("WakeLock released")
                                
                                # إشعار الإكمال
                                notification = NotificationBuilder(mService, "SmartSRS") \
                                    .setContentTitle("✅ Session Complete") \
                                    .setContentText(f"{review_count} reviews done!") \
                                    .setSmallIcon(17301659) \
                                    .setOngoing(False) \
                                    .build()
                                nm.notify(1, notification)
                                
                                review_count = 0
                        else:
                            print("Play failed, retrying next cycle")
                
                # نوم قصير
                sleep(1)
            
            except Exception as e:
                print(f"Loop error: {e}")
                sleep(2)
    
    except Exception as e:
        print(f"Fatal service error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_service()
