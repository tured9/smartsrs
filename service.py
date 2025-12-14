from time import sleep, time
import os
from jnius import autoclass, cast
from kivy.utils import platform

INTERVALS = [10, 60, 300, 1800, 3600]  # ثواني

def play_audio_smart_mix(file_path):
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        AudioManager = autoclass('android.media.AudioManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        Builder = autoclass('android.media.AudioAttributes$Builder')

        am = cast(AudioManager, mService.getSystemService(Context.AUDIO_SERVICE))

        # طلب Audio Focus بشكل صحيح
        result = am.requestAudioFocus(None, AudioManager.STREAM_MUSIC, AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
        if result != AudioManager.AUDIOFOCUS_REQUEST_GRANTED:
            return False

        attributes = Builder().setUsage(AudioAttributes.USAGE_MEDIA).setContentType(AudioAttributes.CONTENT_TYPE_MUSIC).build()
        player = MediaPlayer()
        player.setAudioAttributes(attributes)
        player.setDataSource(file_path)
        player.prepare()
        player.start()

        duration = player.getDuration() / 1000
        time_end = time() + duration + 1
        while time() < time_end:
            sleep(0.5)

        player.release()
        am.abandonAudioFocus(None)
        return True
    except Exception as e:
        print("Smart Play Error:", e)
        return False

def run_service():
    if platform != 'android':
        return

    PythonService = autoclass('org.kivy.android.PythonService')
    mService = PythonService.mService
    Context = autoclass('android.content.Context')
    PowerManager = autoclass('android.os.PowerManager')

    pm = mService.getSystemService(Context.POWER_SERVICE)
    wakelock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "SmartSRS::WakeLock")
    wakelock.acquire()

    # إعداد الإشعار
    NotificationBuilder = autoclass('android.app.Notification$Builder')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    NotificationManager = autoclass('android.app.NotificationManager')
    channel_id = "SmartSRS_Channel"
    nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
    chan = NotificationChannel(channel_id, "SmartSRS", NotificationManager.IMPORTANCE_HIGH)
    nm.createNotificationChannel(chan)

    notification = NotificationBuilder(mService, channel_id) \
        .setContentTitle("SmartSRS") \
        .setContentText("Running in background...") \
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
                        if wakelock.isHeld():
                            wakelock.release()
                    elif content != loaded_file:
                        loaded_file = content
                        current_step = 0
                        play_audio_smart_mix(loaded_file)
                        next_play_time = time() + INTERVALS[0]
                        if not wakelock.isHeld():
                            wakelock.acquire()
            except:
                pass

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
                        if wakelock.isHeld():
                            wakelock.release()

        sleep(1)

if __name__ == '__main__':
    run_service()

