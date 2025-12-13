from time import sleep, time
from jnius import autoclass
from kivy.core.audio import SoundLoader
from kivy.utils import platform
import os

# فترات التكرار (ثواني)
INTERVALS = [10, 60, 300, 1800, 3600]

def get_service():
    """تجهيز الخدمة لتعمل في الخلفية وتظهر إشعاراً"""
    if platform == 'android':
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        
        # تفعيل إشعار دائم لمنع النظام من قتل الخدمة
        Context = autoclass('android.content.Context')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        
        channel_id = "SmartSRS_Channel"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        
        # إنشاء قناة الإشعارات
        chan = NotificationChannel(channel_id, "SmartSRS Background", NotificationManager.IMPORTANCE_LOW)
        nm.createNotificationChannel(chan)
        
        # إنشاء الإشعار
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("Smart SRS") \
            .setContentText("Running in background...") \
            .setSmallIcon(17301659) \
            .build() # 17301659 is icon 'music'
            
        # تشغيل الخدمة في المقدمة
        mService.startForeground(1, notification)

def run_service():
    get_service()
    
    current_step = 0
    next_play_time = 0
    loaded_file = None
    sound = None
    
    # ملف التواصل بين الواجهة والخدمة
    config_file = "srs_config.txt"

    while True:
        # قراءة الملف لمعرفة هل هناك أمر جديد
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    content = f.read().strip()
                
                # إذا وجدنا "STOP"، نوقف كل شيء
                if content == "STOP":
                    if sound: sound.stop()
                    loaded_file = None
                    current_step = 0
                    os.remove(config_file) # مسح الأمر
                
                # إذا وجدنا مسار ملف جديد
                elif content and content != loaded_file:
                    loaded_file = content
                    current_step = 0
                    # جدولة أول تشغيل
                    next_play_time = time() + INTERVALS[0]
                    
            except:
                pass

        # منطق التشغيل
        if loaded_file and next_play_time > 0:
            if time() >= next_play_time:
                # تشغيل الصوت
                try:
                    sound = SoundLoader.load(loaded_file)
                    if sound:
                        sound.play()
                        # انتظار انتهاء الصوت
                        sleep(sound.length + 1)
                        
                        # الجدولة القادمة
                        current_step += 1
                        if current_step < len(INTERVALS):
                            next_play_time = time() + INTERVALS[current_step]
                        else:
                            # انتهت الجلسة
                            loaded_file = None
                            next_play_time = 0
                except:
                    pass
        
        # راحة للمعالج (مهم جداً)
        sleep(1)

if __name__ == '__main__':
    run_service()
