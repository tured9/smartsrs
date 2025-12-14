from time import sleep, time
from jnius import autoclass, cast
from kivy.utils import platform
import os

INTERVALS = [10, 60, 300, 1800, 3600]

def play_audio_adhan_style(file_path):
    """
    تشغيل الصوت بنمط الأذان (Adhan Mode):
    1. اختراق وضع الصامت.
    2. إيقاف التطبيقات الأخرى (YouTube/Facebook) تماماً وليس خفضها.
    3. استخدام قناة التنبيهات القصوى.
    """
    try:
        # استدعاء مكتبات النظام
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        AudioManager = autoclass('android.media.AudioManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        Builder = autoclass('android.media.AudioAttributes$Builder')

        # 1. السيطرة على الصوت (Audio Focus - Gain Transient)
        # AUDIOFOCUS_GAIN_TRANSIENT = 2 (هذا يوقف يوتيوب مؤقتاً ولا يخفضه فقط)
        am = cast(AudioManager, mService.getSystemService(Context.AUDIO_SERVICE))
        am.requestAudioFocus(None, 4, 2) # Stream Alarm (4), Focus Gain (2)

        # 2. رفع صوت المنبه للأعلى (Force Max Volume)
        max_vol = am.getStreamMaxVolume(4) # 4 = STREAM_ALARM
        am.setStreamVolume(4, max_vol, 0)

        # 3. إعداد خصائص الصوت (السر في Flag 1)
        # USAGE_ALARM = 4
        # CONTENT_TYPE_SONIFICATION = 4
        # FLAG_AUDIBILITY_ENFORCED = 1 (هذا هو سر تطبيقات الأذان!)
        # هذا الفلاج يجبر الصوت على الخروج حتى لو كان الهاتف صامتاً
        attributes = Builder() \
            .setUsage(4) \
            .setContentType(4) \
            .setFlags(1) \
            .build()

        player = MediaPlayer()
        player.setAudioAttributes(attributes)
        player.setDataSource(file_path)
        player.prepare()
        player.start()
        
        # انتظار انتهاء الصوت
        duration = player.getDuration() / 1000
        time_end = time() + duration + 1
        while time() < time_end:
            sleep(0.5)
        
        player.release()
        
        # إرجاع الصوت للتطبيقات الأخرى
        am.abandonAudioFocus(None)
        return True

    except Exception as e:
        print(f"Adhan Mode Error: {e}")
        return False

def run_service():
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        
        # --- القفل القوي جداً (WakeLock) ---
        PowerManager = autoclass('android.os.PowerManager')
        pm = mService.getSystemService(Context.POWER_SERVICE)
        # PARTIAL_WAKE_LOCK = 1
        wakelock = pm.newWakeLock(1, "SmartSRS:AdhanLock")
        wakelock.acquire()

        # إشعار دائم
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        
        channel_id = "SmartSRS_Adhan"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        chan = NotificationChannel(channel_id, "SmartSRS Service", 4) # Importance High
        nm.createNotificationChannel(chan)
        
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("Smart SRS Active") \
            .setContentText("Mode: Adhan/Alarm Priority") \
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
                    play_audio_adhan_style(loaded_file)
                    next_play_time = time() + INTERVALS[0]
                    if 'wakelock' in locals() and not wakelock.isHeld():
                        wakelock.acquire()
            except:
                pass

        if loaded_file and next_play_time > 0:
            if time() >= next_play_time:
                played = play_audio_adhan_style(loaded_file)
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
