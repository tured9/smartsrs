from time import sleep, time
from jnius import autoclass
from kivy.utils import platform
import os

# الفترات الزمنية (ثواني)
INTERVALS = [10, 60, 300, 1800, 3600]

def play_native_audio(file_path):
    """تشغيل الصوت باستخدام مشغل النظام الأصلي"""
    try:
        MediaPlayer = autoclass('android.media.MediaPlayer')
        player = MediaPlayer()
        player.setDataSource(file_path)
        player.prepare()
        player.setVolume(1.0, 1.0) # صوت كامل
        player.start()
        
        # الانتظار حتى ينتهي المقطع
        while player.isPlaying():
            sleep(0.5)
            
        player.release()
        return True
    except Exception as e:
        print(f"Service Audio Error: {e}")
        return False

def run_service():
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')

        # 1. تفعيل WakeLock (يمنع المعالج من النوم 100%)
        pm = mService.getSystemService(Context.POWER_SERVICE)
        wakelock = pm.newWakeLock(1, "SmartSRS:ForeverLock")
        wakelock.acquire()

        # 2. إنشاء قناة الإشعارات (ضروري لأندرويد 8+)
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        channel_id = "SmartSRS_Foreground"
        
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        # IMPORTANCE_DEFAULT = 3 (يظهر في الشريط الرئيسي دون إخفاء)
        chan = NotificationChannel(channel_id, "SmartSRS Background", 3)
        nm.createNotificationChannel(chan)

        # 3. بناء الإشعار مع MediaStyle
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        MediaStyle = autoclass('android.app.Notification$MediaStyle')

        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("Smart SRS is Running") \
            .setContentText("Listening in background...") \
            .setSmallIcon(17301569)  # أيقونة أفضل: ic_media_play (بدلاً من 17301659)
            .setStyle(MediaStyle())  # أسلوب وسائط ليكون دائمًا مرئيًا
            .setOngoing(True) \
            .build()
            
        # 4. تشغيل الخدمة في المقدمة (هذا ما يمنع النظام من قتلها)
        mService.startForeground(101, notification)

    # تحديد مسار ملف الأوامر
    app_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(app_dir, "srs_config.txt")

    loaded_file = None
    next_play_time = 0
    current_step = 0

    # حلقة لانهائية
    while True:
        # قراءة الأوامر
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    content = f.read().strip()
                
                # أمر التوقف
                if content == "STOP":
                    loaded_file = None
                    os.remove(config_path)
                    
                # أمر ملف جديد
                elif content and content != loaded_file:
                    loaded_file = content
                    current_step = 0
                    # تشغيل فوري للتأكيد
                    play_native_audio(loaded_file)
                    next_play_time = time() + INTERVALS[0]
            except:
                pass

        # التحقق من الموعد
        if loaded_file and next_play_time > 0:
            if time() >= next_play_time:
                play_native_audio(loaded_file)
                
                current_step += 1
                if current_step < len(INTERVALS):
                    next_play_time = time() + INTERVALS[current_step]
                else:
                    loaded_file = None # انتهت الجلسة

        # راحة قصيرة للمعالج
        sleep(1)

if __name__ == '__main__':
    run_service()
