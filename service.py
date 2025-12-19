"""
Smart SRS Service - ULTIMATE with Forced Timer
English Logs
"""

from time import sleep, time
from jnius import autoclass, cast
from kivy.utils import platform
import os

INTERVALS = [10, 60, 300, 1800, 3600]  # Customize as needed

def play_audio(file_path):
    try:
        MediaPlayer = autoclass('android.media.MediaPlayer')
        player = MediaPlayer()
        player.setDataSource(file_path)
        player.prepare()
        player.start()
        
        while player.isPlaying():
            sleep(0.5)
        
        player.release()
        return True
    except Exception as e:
        print(f"Play error: {e}")
        return False

def run_service():
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        
        pm = mService.getSystemService(Context.POWER_SERVICE)
        wakelock = pm.newWakeLock(1, "SmartSRS:Lock")
        wakelock.acquire()

        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        chan = NotificationChannel("SmartSRS_CH", "Review Service", 4)
        nm.createNotificationChannel(chan)
        
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        notif = NotificationBuilder(mService, "SmartSRS_CH") \
            .setContentTitle("Smart SRS Running") \
            .setContentText("Background reviews active") \
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
                    if wakelock.isHeld():
                        wakelock.release()
                elif content and content != loaded_file:
                    loaded_file = content
                    current_step = 0
                    play_audio(loaded_file)  # Immediate play
                    next_play_time = time() + INTERVALS[0]
            except:
                pass

        if loaded_file and next_play_time > 0:
            remaining = next_play_time - time()
            if remaining <= 0:
                play_audio(loaded_file)
                current_step += 1
                if current_step < len(INTERVALS):
                    next_play_time = time() + INTERVALS[current_step]
                else:
                    loaded_file = None
                    next_play_time = 0
            else:
                # Forced timer check every second to enforce
                sleep(1)

if __name__ == '__main__':
    run_service()
