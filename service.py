# service.py — SmartSRS foreground service (Kivy + pyjnius)
from time import sleep, time
from jnius import autoclass, cast, JavaException
import os

INTERVALS = [10, 60, 300, 1800, 3600]

# Java classes
Context = autoclass('android.content.Context')
AudioManager = autoclass('android.media.AudioManager')
MediaPlayer = autoclass('android.media.MediaPlayer')
PowerManager = autoclass('android.os.PowerManager')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')

# Kivy PythonService (معطل عند التشغيل محلياً على الكمبيوتر)
PythonService = None
try:
    PythonService = autoclass('org.kivy.android.PythonService')
except Exception:
    pass

def request_audio_focus(am):
    try:
        AFBuilder = autoclass('android.media.AudioFocusRequest$Builder')
        AFRequest = AFBuilder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
        focusRequest = AFRequest.build()
        res = am.requestAudioFocus(focusRequest)
        return res == AudioManager.AUDIOFOCUS_REQUEST_GRANTED
    except JavaException:
        res = am.requestAudioFocus(None, AudioManager.STREAM_MUSIC, AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
        return res == AudioManager.AUDIOFOCUS_REQUEST_GRANTED

def play_audio_smart_mix(file_path, mService):
    try:
        if not os.path.exists(file_path):
            print("File not found:", file_path)
            return False

        am = cast(AudioManager, mService.getSystemService(Context.AUDIO_SERVICE))
        pm = cast(PowerManager, mService.getSystemService(Context.POWER_SERVICE))

        player = MediaPlayer()
        player.setAudioStreamType(AudioManager.STREAM_MUSIC)
        player.setWakeMode(mService.getApplicationContext(), PowerManager.PARTIAL_WAKE_LOCK)
        player.setDataSource(file_path)
        player.prepare()

        try:
            request_audio_focus(am)
        except Exception:
            pass

        player.start()

        duration = player.getDuration() / 1000.0
        if duration <= 0:
            duration = 1.0
        t_end = time() + duration + 1
        while time() < t_end:
            sleep(0.5)

        try:
            player.stop()
            player.release()
        except Exception:
            pass

        try:
            am.abandonAudioFocus(None)
        except Exception:
            pass

        return True
    except Exception as e:
        print("Smart Play Error:", e)
        return False

def run_service():
    # When run inside Android service context:
    if PythonService:
        mService = PythonService.mService
        # Start foreground notification ASAP
        channel_id = "SmartSRS_Mix"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        try:
            chan = NotificationChannel(channel_id, "SmartSRS Service", 2)
            nm.createNotificationChannel(chan)
        except Exception:
            pass
        try:
            notification = NotificationBuilder(mService, channel_id) \
                .setContentTitle("SmartSRS Running") \
                .setContentText("Background review active") \
                .setSmallIcon(17301659) \
                .build()
            mService.startForeground(1, notification)
        except Exception:
            pass
    else:
        # fallback for local testing (no Android)
        mService = None

    config_path = "/sdcard/SmartSRS/srs_config.txt"
    loaded_file = None
    next_play_time = 0
    current_step = 0

    while True:
        try:
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    content = f.read().strip()
                if content == "STOP":
                    loaded_file = None
                    os.remove(config_path)
                    next_play_time = 0
                elif content and content != loaded_file:
                    loaded_file = content
                    current_step = 0
                    if mService:
                        play_audio_smart_mix(loaded_file, mService)
                    else:
                        print("Would play (no mService):", loaded_file)
                    next_play_time = time() + INTERVALS[0]

            if loaded_file and next_play_time > 0 and time() >= next_play_time:
                if mService:
                    played = play_audio_smart_mix(loaded_file, mService)
                else:
                    print("Would play now (no mService):", loaded_file)
                    played = True
                if played:
                    current_step += 1
                    if current_step < len(INTERVALS):
                        next_play_time = time() + INTERVALS[current_step]
                    else:
                        loaded_file = None
                        next_play_time = 0
        except Exception as e:
            print("Service loop error:", e)
        sleep(1)

if __name__ == '__main__':
    run_service()
