from time import sleep, time
from jnius import autoclass
from kivy.utils import platform
import os

# فترات التكرار (ثواني)
INTERVALS = [10, 60, 300, 1800, 3600]

def play_audio_android(file_path):
    """تشغيل الصوت باستخدام مشغل أندرويد الأصلي"""
    try:
        MediaPlayer = autoclass('android.media.MediaPlayer')
        player = MediaPlayer()
        player.setDataSource(file_path)
        player.prepare()
        player.start()
        
        # الانتظار حتى ينتهي الصوت (حتى لا يتداخل)
        duration = player.getDuration() / 1000  # تحويل من ميلي ثانية إلى ثانية
        sleep(duration + 1)
        
        player.release() # تنظيف الذاكرة
        return True
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False

def run_service():
    # 1. إعداد الإشعار (كما كان سابقاً لضمان البقاء في الخلفية)
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        
        channel_id = "SmartSRS_Channel"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        chan = NotificationChannel(channel_id, "SmartSRS Background", NotificationManager.IMPORTANCE_LOW)
        nm.createNotificationChannel(chan)
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("Smart SRS") \
            .setContentText("Active & Listening...") \
            .setSmallIcon(17301659) \
            .build()
        mService.startForeground(1, notification)

    # 2. حلقة العمل الرئيسية
    config_file = "srs_config.txt"
    # تحديد المسار المطلق للملف لضمان قراءته بشكل صحيح
    # (هذا المسار هو المجلد الخاص بالتطبيق)
    app_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(app_dir, config_file)

    loaded_file = None
    next_play_time = 0
    current_step = 0

    while True:
        # قراءة الأوامر من الملف
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    content = f.read().strip()
                
                # إيقاف الخدمة
                if content == "STOP":
                    loaded_file = None
                    os.remove(config_path)
                
                # تحميل ملف جديد
                elif content and content != loaded_file:
                    loaded_file = content
                    current_step = 0
                    # تشغيل فوري للتجربة ثم جدولة
                    play_audio_android(loaded_file)
                    next_play_time = time() + INTERVALS[0]
                    
            except Exception as e:
                print(f"Config Read Error: {e}")

        # التحقق من الوقت وتشغيل الصوت
        if loaded_file and next_play_time > 0:
            if time() >= next_play_time:
                # تشغيل الصوت
                played = play_audio_android(loaded_file)
                
                if played:
                    current_step += 1
                    if current_step < len(INTERVALS):
                        next_play_time = time() + INTERVALS[current_step]
                    else:
                        # إعادة التكرار من البداية أو الإنهاء (هنا ننهي)
                        loaded_file = None
                        next_play_time = 0

        # راحة للمعالج
        sleep(2)

if __name__ == '__main__':
    run_service()
