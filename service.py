from time import sleep, time
from jnius import autoclass
from kivy.utils import platform
import os

INTERVALS = [10, 60, 300, 1800, 3600]

def play_audio_android(file_path):
    """
    تشغيل الصوت بنمط 'المنبه' ليقاطع التطبيقات الأخرى
    """
    try:
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        Builder = autoclass('android.media.AudioAttributes$Builder')

        # 1. إعداد خصائص الصوت ليكون "منبه" (Alarm)
        # USAGE_ALARM = 4
        # CONTENT_TYPE_SONIFICATION = 4
        attributes = Builder().setUsage(4).setContentType(4).build()

        player = MediaPlayer()
        # تطبيق خصائص المنبه على المشغل
        player.setAudioAttributes(attributes)
        
        player.setDataSource(file_path)
        player.prepare()
        
        # 2. رفع الصوت إلى أقصى حد (1.0 = 100%)
        player.setVolume(1.0, 1.0)
        
        player.start()
        
        # الانتظار حتى ينتهي
        duration = player.getDuration() / 1000
        sleep(duration + 1)
        
        player.release()
        return True
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False

def run_service():
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        
        # معرف القناة
        channel_id = "SmartSRS_Channel"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        
        # أهمية عالية (IMPORTANCE_HIGH = 4) لضمان عدم القتل
        chan = NotificationChannel(channel_id, "SmartSRS Foreground", 4)
        nm.createNotificationChannel(chan)
        
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("Smart SRS Active") \
            .setContentText("Learning mode is ON") \
            .setSmallIcon(17301659) \
            .build()
            
        mService.startForeground(1, notification)

    # تحديد المسار
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
                
                elif content and content != loaded_file:
                    loaded_file = content
                    current_step = 0
                    # تشغيل تجريبي
                    play_audio_android(loaded_file)
                    next_play_time = time() + INTERVALS[0]
            except:
                pass

        if loaded_file and next_play_time > 0:
            if time() >= next_play_time:
                played = play_audio_android(loaded_file)
                if played:
                    current_step += 1
                    if current_step < len(INTERVALS):
                        next_play_time = time() + INTERVALS[current_step]
                    else:
                        loaded_file = None
                        next_play_time = 0

        # راحة
        sleep(2)

if __name__ == '__main__':
    run_service()
