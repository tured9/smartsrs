from jnius import autoclass
from time import sleep

MediaPlayer = autoclass('android.media.MediaPlayer')
AudioManager = autoclass('android.media.AudioManager')
PowerManager = autoclass('android.os.PowerManager')
Context = autoclass('android.content.Context')
Notification = autoclass('android.app.Notification')
NotificationBuilder = autoclass('android.app.Notification$Builder')
PythonService = autoclass('org.kivy.android.PythonService')
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')

# جعل الخدمة foreground
context = PythonService.mService
intent = Intent(context, PythonService.mService.getClass())
pending_intent = PendingIntent.getActivity(context, 0, intent, 0)
notification_builder = NotificationBuilder(context)
notification_builder.setContentTitle('تشغيل صوت المراجعة')
notification_builder.setContentText('جاري تشغيل الملف الصوتي...')
notification_builder.setSmallIcon(context.getApplicationInfo().icon)
notification_builder.setContentIntent(pending_intent)
notification = notification_builder.build()
context.startForeground(1, notification)

# اكتساب WakeLock
pm = cast(PowerManager, context.getSystemService(Context.POWER_SERVICE))
wl = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, 'spaced_audio:wakelock')
wl.acquire()

# استخراج الملف من الintent
audio_file = PythonService.mService.getIntent().getStringExtra('audio_file')

# تشغيل الصوت
mPlayer = MediaPlayer()
mPlayer.setDataSource(audio_file)
mPlayer.setAudioStreamType(AudioManager.STREAM_ALARM)  # مثل المنبه
mPlayer.prepare()
mPlayer.start()

# انتظر انتهاء الصوت
sleep(mPlayer.getDuration() / 1000 + 1)

# تحرير الموارد
mPlayer.release()
wl.release()

# إيقاف الخدمة
context.stopSelf()
