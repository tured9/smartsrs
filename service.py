from time import sleep, time
from jnius import autoclass
from kivy.utils import platform
import os

INTERVALS = [10, 60, 300, 1800, 3600]

def play_native_audio(file_path):
    try:
        MediaPlayer = autoclass('android.media.MediaPlayer')
        player = MediaPlayer()
        player.setDataSource(file_path)
        player.prepare()
        player.setVolume(1.0, 1.0)
        player.start()
        while player.isPlaying():
            sleep(0.5)
        player.release()
        return True
    except Exception as e:
        print(f"Audio Error: {e}")
        return False

def run_service():
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')

        # WakeLock
        pm = mService.getSystemService(Context.POWER_SERVICE)
        wakelock = pm.newWakeLock(1, "SmartSRS:Lock")
        wakelock.acquire()

        # Notification Channel
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        chan = NotificationChannel("SmartSRS_FG", "Background Service", 3)
        nm.createNotificationChannel(chan)

        # Notification
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        notification = NotificationBuilder(mService, "SmartSRS_FG") \
            .setContentTitle("Smart SRS") \
            .setContentText("Running...") \
            .setSmallIcon(17301569) \
            .setOngoing(True) \
            .build()
            
        mService.startForeground(101, notification)

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
                    play_native_audio(loaded_file)
                    next_play_time = time() + INTERVALS[0]
            except:
                pass

        if loaded_file and next_play_time > 0:
            if time() >= next_play_time:
                play_native_audio(loaded_file)
                current_step += 1
                if current_step < len(INTERVALS):
                    next_play_time = time() + INTERVALS[current_step]
                else:
                    loaded_file = None

        sleep(1)

if __name__ == '__main__':
    run_service()
