from time import sleep, time
from jnius import autoclass, cast
from kivy.utils import platform
import os

# الفترات: 10ث، 1د، 5د، 30د، 1س
INTERVALS = [10, 60, 300, 1800, 3600]

def play_audio(file_path):
    try:
        # 1. إعداد الصوت
        MediaPlayer = autoclass('android.media.MediaPlayer')
        player = MediaPlayer()
        player.setDataSource(file_path)
        player.prepare()
        player.setVolume(1.0, 1.0)
        player.start()
        
        # 2. الانتظار حتى ينتهي
        while player.isPlaying():
            sleep(0.5)
        
        player.release()
        return True
    except:
        return False

def schedule_alarm(context, delay_sec, review_num):
    try:
        # جدولة المنبه (نسخة احتياطية قوية)
        AlarmManager = autoclass('android.app.AlarmManager')
        Intent = autoclass('android.content.Intent')
        PendingIntent = autoclass('android.app.PendingIntent')
        SystemClock = autoclass('android.os.SystemClock')
        
        am = cast(AlarmManager, context.getSystemService('alarm'))
        intent = Intent(context, autoclass('org.mysrs.smartsrs.ServiceSrsservice'))
        intent.setAction(f"ALARM_REV_{review_num}")
        
        # FLAG_IMMUTABLE = 67108864
        pi = PendingIntent.getService(context, review_num, intent, 67108864)
        
        trigger = SystemClock.elapsedRealtime() + (delay_sec * 1000)
        
        # محاولة استخدام المنبه الدقيق
        try:
            am.setExactAndAllowWhileIdle(2, trigger, pi)
        except:
            am.setExact(2, trigger, pi)
        return True
    except:
        return False

def run_service():
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        
        # 1. WakeLock (منع النوم)
        pm = mService.getSystemService(Context.POWER_SERVICE)
        wl = pm.newWakeLock(1, "SmartSRS:ServiceLock")
        wl.acquire()

        # 2. Notification (الإشعار الدائم)
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        
        chan = NotificationChannel("SmartSRS_FG", "Review Service", 4)
        chan.setSound(None, None)
        nm.createNotificationChannel(chan)
        
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        notif = NotificationBuilder(mService, "SmartSRS_FG") \
            .setContentTitle("Smart SRS Running") \
            .setSmallIcon(17301659) \
            .setOngoing(True) \
            .build()
        mService.startForeground(1, notif)

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
                    play_audio(loaded_file)
                    
                    # جدولة المنبهات كاحتياط
                    for i, interval in enumerate(INTERVALS):
                        schedule_alarm(mService, interval, i+1)
                        
                    next_play_time = time() + INTERVALS[0]
            except:
                pass

        # المشغل الأساسي (Timer)
        if loaded_file and next_play_time > 0:
            if time() >= next_play_time:
                play_audio(loaded_file)
                current_step += 1
                if current_step < len(INTERVALS):
                    next_play_time = time() + INTERVALS[current_step]
                else:
                    loaded_file = None
                    next_play_time = 0

        sleep(1)

if __name__ == '__main__':
    run_service()
