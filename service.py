from time import sleep, time
from jnius import autoclass, cast
from kivy.utils import platform
import os

# الفترات الزمنية
INTERVALS = [10, 60, 300, 1800, 3600]

def play_audio_professional(file_path):
    """
    طريقة الخبراء:
    1. طلب التركيز الصوتي (لخفض صوت التطبيقات الأخرى).
    2. رفع صوت المنبه للأعلى.
    3. التشغيل عبر قناة المنبه.
    """
    try:
        # استيراد كلاسات أندرويد الضرورية
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        AudioManager = autoclass('android.media.AudioManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        Builder = autoclass('android.media.AudioAttributes$Builder')

        # 1. الحصول على مدير الصوت
        am = cast(AudioManager, mService.getSystemService(Context.AUDIO_SERVICE))

        # 2. طلب التركيز الصوتي (Audio Focus)
        # AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK = 3
        # هذا يعني: اخفض صوت التطبيقات الأخرى مؤقتاً وشغل صوتي
        result = am.requestAudioFocus(None, 3, 3) # Stream Music (3), Gain Transient Duck (3)

        # 3. التأكد من أن صوت "المنبه" مرتفع (Max Volume)
        # STREAM_ALARM = 4
        max_vol = am.getStreamMaxVolume(4)
        current_vol = am.getStreamVolume(4)
        # رفع الصوت إلى 80% على الأقل إذا كان منخفضاً
        target_vol = int(max_vol * 0.8)
        if current_vol < target_vol:
            am.setStreamVolume(4, target_vol, 0)

        # 4. إعداد المشغل كمنبه (Alarm) ليخترق وضع الصامت
        # USAGE_ALARM = 4, CONTENT_TYPE_SONIFICATION = 4
        attributes = Builder().setUsage(4).setContentType(4).build()

        player = MediaPlayer()
        player.setAudioAttributes(attributes)
        player.setDataSource(file_path)
        player.prepare()
        player.start()
        
        # الانتظار حتى ينتهي
        duration = player.getDuration() / 1000
        time_end = time() + duration + 1
        while time() < time_end:
            sleep(0.5)
        
        player.release()
        
        # 5. التخلي عن التركيز الصوتي (إعادة الصوت للتطبيقات الأخرى)
        am.abandonAudioFocus(None)
        
        return True
    except Exception as e:
        print(f"Professional Play Error: {e}")
        return False

def run_service():
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        
        # --- القفل القوي (WakeLock) ---
        PowerManager = autoclass('android.os.PowerManager')
        pm = mService.getSystemService(Context.POWER_SERVICE)
        # PARTIAL_WAKE_LOCK = 1
        wakelock = pm.newWakeLock(1, "SmartSRS:ProLock")
        wakelock.acquire()
        # ------------------------------

        # الإشعار الدائم (Foreground)
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        
        channel_id = "SmartSRS_Pro"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        # IMPORTANCE_LOW = 2
        chan = NotificationChannel(channel_id, "SmartSRS Service", 2)
        nm.createNotificationChannel(chan)
        
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("Smart SRS Running") \
            .setContentText("Background Audio Active") \
            .setSmallIcon(17301659) \
            .build()
            
        mService.startForeground(1, notification)

    app_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(app_dir, "srs_config.txt")

    loaded_file = None
    next_play_time = 0
    current_step = 0

    while True:
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    content = f.read().strip()
                
                if content == "STOP":
                    loaded_file = None
                    os.remove(config_path)
                    if 'wakelock' in locals() and wakelock.isHeld():
                        wakelock.release()
                
                elif content and content != loaded_file:
                    loaded_file = content
                    current_step = 0
                    # تجربة الصوت فوراً
                    play_audio_professional(loaded_file)
                    next_play_time = time() + INTERVALS[0]
                    
                    if 'wakelock' in locals() and not wakelock.isHeld():
                        wakelock.acquire()
            except:
                pass

        if loaded_file and next_play_time > 0:
            # هامش دقة 1 ثانية
            if time() >= next_play_time:
                played = play_audio_professional(loaded_file)
                if played:
                    current_step += 1
                    if current_step < len(INTERVALS):
                        next_play_time = time() + INTERVALS[current_step]
                    else:
                        loaded_file = None
                        next_play_time = 0
                        if 'wakelock' in locals() and wakelock.isHeld():
                            wakelock.release()

        sleep(1)

if __name__ == '__main__':
    run_service()
