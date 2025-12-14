from time import sleep, time
from jnius import autoclass
from kivy.utils import platform
import os

# --- فترات التكرار (الذكية) ---
# المرة الأولى: بعد 10 ثواني
# المرة الثانية: بعد دقيقة
# المرة الثالثة: بعد 5 دقائق
# المرة الرابعة: بعد 30 دقيقة
# المرة الخامسة: بعد ساعة
INTERVALS = [10, 60, 300, 1800, 3600]

def play_audio_force(file_path):
    """تشغيل الصوت بقوة واختراق الصمت"""
    try:
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        Builder = autoclass('android.media.AudioAttributes$Builder')

        # جعل الصوت بنمط "الوسائط" (Music) ليتوافق مع الخلفية
        # ولكن مع رفع الصوت
        attributes = Builder().setUsage(1).setContentType(2).build() # USAGE_MEDIA

        player = MediaPlayer()
        player.setAudioAttributes(attributes)
        player.setDataSource(file_path)
        player.prepare()
        player.setVolume(1.0, 1.0) # صوت كامل
        player.start()
        
        # الانتظار الذكي (بدون تجميد)
        duration = player.getDuration() / 1000
        time_end = time() + duration + 1
        while time() < time_end:
            sleep(0.5) # انتظار خفيف
        
        player.release()
        return True
    except Exception as e:
        print(f"Play Error: {e}")
        return False

def run_service():
    if platform == 'android':
        # 1. إعداد الخدمة كـ "مشغل موسيقى" (Foreground)
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        
        # ----------------------------------------------------
        # الجزء الجديد: القفل القوي (Partial WakeLock)
        # هذا يمنع المعالج من النوم حتى لو الشاشة مغلقة
        # ----------------------------------------------------
        PowerManager = autoclass('android.os.PowerManager')
        pm = mService.getSystemService(Context.POWER_SERVICE)
        # PARTIAL_WAKE_LOCK = 1
        wakelock = pm.newWakeLock(1, "SmartSRS:BackgroundLock")
        wakelock.acquire() # تفعيل القفل (المعالج لن ينام أبداً)
        # ----------------------------------------------------

        # إظهار الإشعار (مطلوب من أندرويد)
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        
        channel_id = "SmartSRS_Music"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        # IMPORTANCE_LOW = 2 (عشان ما يزعجك بصوت الإشعار كل شوي)
        chan = NotificationChannel(channel_id, "SRS Player", 2)
        nm.createNotificationChannel(chan)
        
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("Smart SRS is Active") \
            .setContentText("Keeping memory awake for reviews...") \
            .setSmallIcon(17301659) \
            .build()
            
        mService.startForeground(1, notification)

    # إعداد المسارات
    app_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(app_dir, "srs_config.txt")

    loaded_file = None
    next_play_time = 0
    current_step = 0

    # حلقة العمل (لا تتوقف أبداً بفضل الـ WakeLock)
    while True:
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    content = f.read().strip()
                
                # أمر التوقف
                if content == "STOP":
                    loaded_file = None
                    os.remove(config_path)
                    # تحرير القفل عند التوقف (لتوفير البطارية)
                    if 'wakelock' in locals() and wakelock.isHeld():
                        wakelock.release()
                
                # تحميل ملف جديد
                elif content and content != loaded_file:
                    loaded_file = content
                    current_step = 0
                    # تأكيد التشغيل
                    play_audio_force(loaded_file)
                    next_play_time = time() + INTERVALS[0]
                    
                    # إعادة تفعيل القفل إذا لم يكن مفعلاً
                    if 'wakelock' in locals() and not wakelock.isHeld():
                        wakelock.acquire()
            except:
                pass

        # التحقق من الموعد
        if loaded_file and next_play_time > 0:
            # نستخدم هامش خطأ بسيط (0.5 ثانية) لضمان الدقة
            if time() >= next_play_time:
                play_audio_force(loaded_file)
                
                current_step += 1
                if current_step < len(INTERVALS):
                    next_play_time = time() + INTERVALS[current_step]
                else:
                    # انتهت الجلسة
                    loaded_file = None
                    next_play_time = 0
                    # حرر القفل بعد الانتهاء
                    if 'wakelock' in locals() and wakelock.isHeld():
                        wakelock.release()

        # راحة قصيرة جداً (للحفاظ على الاستجابة)
        sleep(1)

if __name__ == '__main__':
    run_service()
