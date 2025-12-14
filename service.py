from time import sleep, time
from jnius import autoclass, cast
from kivy.utils import platform
import os

INTERVALS = [10, 60, 300, 1800, 3600]

def play_audio_smart_mix(file_path):
    """
    التشغيل الذكي (Smart Mix):
    - يحترم إعدادات صوت الهاتف الحالية.
    - يقوم بخفض صوت التطبيقات الأخرى مؤقتاً (Ducking) بدلاً من قطعها.
    """
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        AudioManager = autoclass('android.media.AudioManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        Builder = autoclass('android.media.AudioAttributes$Builder')

        # 1. إدارة التركيز الصوتي (Audio Focus)
        am = cast(AudioManager, mService.getSystemService(Context.AUDIO_SERVICE))
        
        # AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK = 3
        # هذا الخيار يقول للنظام: "اخفض صوت يوتيوب قليلاً، لا توقفه، ودعني أتكلم"
        am.requestAudioFocus(None, 3, 3) 

        # 2. إعداد المشغل كـ "وسائط" (Media) عادية
        # USAGE_MEDIA = 1
        # CONTENT_TYPE_MUSIC = 2
        attributes = Builder().setUsage(1).setContentType(2).build()

        player = MediaPlayer()
        player.setAudioAttributes(attributes)
        player.setDataSource(file_path)
        player.prepare()
        
        # لا نضع setVolume هنا، نترك التحكم لأزرار الهاتف
        player.start()
        
        # انتظار انتهاء المقطع
        duration = player.getDuration() / 1000
        time_end = time() + duration + 1
        while time() < time_end:
            sleep(0.5)
        
        player.release()
        
        # إعادة الصوت الطبيعي للتطبيقات الأخرى
        am.abandonAudioFocus(None)
        
        return True
    except Exception as e:
        print(f"Smart Play Error: {e}")
        return False

def run_service():
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')

        # --- WakeLock (لمنع النظام من النوم) ---
        pm = mService.getSystemService(Context.POWER_SERVICE)
        # PARTIAL_WAKE_LOCK = 1
        wakelock = pm.newWakeLock(1, "SmartSRS:SmartLock")
        wakelock.acquire()

        # إعداد الإشعار (مهم جداً للبقاء في الخلفية)
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        
        channel_id = "SmartSRS_Mix"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        chan = NotificationChannel(channel_id, "SmartSRS Service", 2)
        nm.createNotificationChannel(chan)
        
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("Smart SRS Running") \
            .setContentText("Background Review Active") \
            .setSmallIcon(17301659) \
            .build()
            
        mService.startForeground(1, notification)

    app_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(app_dir, "srs_config.txt")

    loaded_file = None
    next_play_time = 0
    current_step = 0

    # حلقة العمل الرئيسية
    while True:
        # قراءة الأوامر (محمية بـ try لمنع التوقف)
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    content = f.read().strip()
                
                if content == "STOP":
                    loaded_file = None
                    os.remove(config_path)
                    # تحرير القفل عند التوقف الكامل
                    if 'wakelock' in locals() and wakelock.isHeld():
                        wakelock.release()
                
                elif content and content != loaded_file:
                    loaded_file = content
                    current_step = 0
                    # تجربة فورية
                    play_audio_smart_mix(loaded_file)
                    next_play_time = time() + INTERVALS[0]
                    
                    if 'wakelock' in locals() and not wakelock.isHeld():
                        wakelock.acquire()
            except:
                pass

        # التحقق من الوقت
        if loaded_file and next_play_time > 0:
            if time() >= next_play_time:
                played = play_audio_smart_mix(loaded_file)
                if played:
                    current_step += 1
                    if current_step < len(INTERVALS):
                        next_play_time = time() + INTERVALS[current_step]
                    else:
                        loaded_file = None
                        next_play_time = 0
                        if 'wakelock' in locals() and wakelock.isHeld():
                            wakelock.release()

        # راحة للمعالج
        sleep(1)

if __name__ == '__main__':
    run_service()
