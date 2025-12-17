"""
Smart SRS Service - النسخة النهائية القوية جداً
مع جميع التحسينات الاحترافية للعمل في الخلفية بشكل موثوق 100%
"""

from time import sleep, time
from jnius import autoclass, cast
from kivy.utils import platform
import os
import sys

# فترات المراجعة المتباعدة (بالثواني)
# يمكنك تغييرها حسب رغبتك
INTERVALS = [10, 60, 300, 1800, 3600]  # 10 ثانية، دقيقة، 5 دقائق، 30 دقيقة، ساعة

# للاختبار السريع استخدم هذه:
# INTERVALS = [5, 10, 15, 20, 30]


def play_audio_ultimate(file_path):
    """
    تشغيل صوتي احترافي مع معالجة أخطاء قوية
    يعمل مثل تطبيقات الموسيقى تماماً
    """
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        AudioManager = autoclass('android.media.AudioManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        
        am = cast(AudioManager, mService.getSystemService(Context.AUDIO_SERVICE))
        
        # 1. إنشاء Audio Attributes (مثل تطبيقات الموسيقى)
        try:
            Builder = autoclass('android.media.AudioAttributes$Builder')
            attributes = Builder() \
                .setUsage(1) \
                .setContentType(2) \
                .build()
        except:
            attributes = None
        
        # 2. طلب Audio Focus (مهم جداً!)
        focus_result = -1
        try:
            # محاولة استخدام API الحديث (Android 8+)
            FocusBuilder = autoclass('android.media.AudioFocusRequest$Builder')
            focus_request = FocusBuilder(2) \
                .setAudioAttributes(attributes if attributes else AudioAttributes.Builder().build()) \
                .setAcceptsDelayedFocusGain(True) \
                .build()
            focus_result = am.requestAudioFocus(focus_request)
            print(f"✅ Audio Focus (Modern): {focus_result}")
        except:
            # استخدام API القديم (Android 7 وأقل)
            try:
                focus_result = am.requestAudioFocus(None, 3, 2)
                print(f"✅ Audio Focus (Legacy): {focus_result}")
            except Exception as e:
                print(f"⚠️ Audio Focus failed: {e}")
        
        # 3. إنشاء وتشغيل MediaPlayer
        player = MediaPlayer()
        
        if attributes:
            try:
                player.setAudioAttributes(attributes)
            except:
                pass
        
        player.setDataSource(file_path)
        player.prepare()
        player.start()
        
        print(f"🎵 Playing: {os.path.basename(file_path)}")
        
        # 4. الانتظار حتى ينتهي التشغيل
        duration = player.getDuration() / 1000.0
        end_time = time() + duration + 1.5
        
        while time() < end_time:
            if not player.isPlaying():
                break
            sleep(0.5)
        
        # 5. التنظيف
        try:
            player.stop()
        except:
            pass
        
        player.release()
        
        # إرجاع Audio Focus
        try:
            am.abandonAudioFocus(focus_request if 'focus_request' in locals() else None)
        except:
            pass
        
        print("✅ Playback completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Play error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_service():
    """
    الخدمة الرئيسية - محسّنة للعمل بشكل موثوق 100%
    مع جميع التحسينات الاحترافية
    """
    if platform != 'android':
        print("Not Android - service not started")
        return
    
    try:
        # استيراد الكلاسات
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        PendingIntent = autoclass('android.app.PendingIntent')
        Intent = autoclass('android.content.Intent')
        
        print("="*50)
        print("🚀 Smart SRS Service Starting...")
        print("="*50)
        
        # ═══════════════════════════════════════════════
        # 1. WakeLock المحسّن - يمنع النوم تماماً
        # ═══════════════════════════════════════════════
        pm = mService.getSystemService(Context.POWER_SERVICE)
        wakelock = pm.newWakeLock(
            PowerManager.PARTIAL_WAKE_LOCK,
            "SmartSRS::UltimateReviewLock"
        )
        wakelock.setReferenceCounted(False)  # مهم جداً!
        
        print("✅ WakeLock created")
        
        # ═══════════════════════════════════════════════
        # 2. Notification Channel قوي جداً
        # ═══════════════════════════════════════════════
        channel_id = "SmartSRS_Ultimate"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        
        # IMPORTANCE_HIGH = 4 (أعلى أولوية)
        chan = NotificationChannel(channel_id, "Smart Review System", 4)
        chan.setDescription("Spaced repetition review - Always running")
        chan.setShowBadge(True)
        chan.setLockscreenVisibility(1)  # VISIBILITY_PUBLIC
        
        try:
            AudioAttributes = autoclass('android.media.AudioAttributes')
            Builder = autoclass('android.media.AudioAttributes$Builder')
            sound_attr = Builder() \
                .setUsage(5) \
                .setContentType(4) \
                .build()
            chan.setSound(None, sound_attr)
        except:
            chan.setSound(None, None)
        
        nm.createNotificationChannel(chan)
        
        print("✅ Notification channel created")
        
        # ═══════════════════════════════════════════════
        # 3. PendingIntent للنقر على الإشعار
        # ═══════════════════════════════════════════════
        launch_intent = mService.getPackageManager() \
            .getLaunchIntentForPackage(mService.getPackageName())
        
        if launch_intent:
            pending_intent = PendingIntent.getActivity(
                mService,
                0,
                launch_intent,
                PendingIntent.FLAG_IMMUTABLE
            )
        else:
            pending_intent = None
        
        # ═══════════════════════════════════════════════
        # 4. Notification قوي جداً
        # ═══════════════════════════════════════════════
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("🎯 Smart Review Active") \
            .setContentText("Background review running...") \
            .setSmallIcon(17301659) \
            .setOngoing(True) \
            .setPriority(2) \
            .setCategory("service") \
            .setVisibility(1)
        
        if pending_intent:
            notification.setContentIntent(pending_intent)
        
        notification = notification.build()
        
        # ═══════════════════════════════════════════════
        # 5. بدء Foreground Service
        # ═══════════════════════════════════════════════
        try:
            mService.startForeground(1, notification)
            print("✅ Foreground service started")
        except Exception as e:
            print(f"⚠️ startForeground error: {e}")
        
        # ═══════════════════════════════════════════════
        # 6. المتغيرات الرئيسية
        # ═══════════════════════════════════════════════
        app_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(app_dir, "srs_config.txt")
        
        loaded_file = None
        next_play_time = 0
        current_step = 0
        review_count = 0
        total_reviews = 0
        
        print(f"📁 Config path: {config_path}")
        print("🔄 Service loop starting...")
        print("="*50)
        
        # ═══════════════════════════════════════════════
        # 7. الحلقة الرئيسية - المحرك الأساسي
        # ═══════════════════════════════════════════════
        while True:
            try:
                # قراءة ملف الإعدادات
                if os.path.exists(config_path):
                    try:
                        with open(config_path, "r", encoding='utf-8') as f:
                            content = f.read().strip()
                        
                        # أمر الإيقاف
                        if content == "STOP":
                            print("\n" + "="*50)
                            print("⏹️ STOP command received")
                            
                            loaded_file = None
                            next_play_time = 0
                            current_step = 0
                            
                            # تحرير WakeLock
                            if wakelock.isHeld():
                                wakelock.release()
                                print("🔓 WakeLock released")
                            
                            # حذف ملف الإعدادات
                            try:
                                os.remove(config_path)
                            except:
                                pass
                            
                            # إشعار الإيقاف
                            stop_notification = NotificationBuilder(mService, channel_id) \
                                .setContentTitle("⏹️ Review Stopped") \
                                .setContentText(f"Session completed: {total_reviews} reviews done") \
                                .setSmallIcon(17301659) \
                                .setOngoing(False) \
                                .build()
                            
                            nm.notify(1, stop_notification)
                            
                            print(f"📊 Total reviews: {total_reviews}")
                            print("="*50 + "\n")
                            
                            review_count = 0
                        
                        # ملف جديد
                        elif content and content != loaded_file:
                            print("\n" + "="*50)
                            print(f"📥 New file loaded: {os.path.basename(content)}")
                            
                            loaded_file = content
                            current_step = 0
                            review_count = 0
                            
                            # الحصول على WakeLock
                            if not wakelock.isHeld():
                                wakelock.acquire()
                                print("🔒 WakeLock acquired")
                            
                            # تشغيل فوري (المراجعة الأولى)
                            print("🎵 Review #1 (immediate)...")
                            success = play_audio_ultimate(loaded_file)
                            
                            if success:
                                review_count = 1
                                total_reviews += 1
                                
                                if current_step < len(INTERVALS):
                                    next_play_time = time() + INTERVALS[current_step]
                                    next_minutes = INTERVALS[current_step] // 60
                                    next_seconds = INTERVALS[current_step] % 60
                                    
                                    print(f"✅ Review #1 done")
                                    print(f"⏰ Next review in: {next_minutes}m {next_seconds}s")
                                    
                                    # تحديث الإشعار
                                    update_notification = NotificationBuilder(mService, channel_id) \
                                        .setContentTitle(f"🎯 Review #{review_count} Done") \
                                        .setContentText(f"Next in {next_minutes}m {next_seconds}s") \
                                        .setSmallIcon(17301659) \
                                        .setOngoing(True) \
                                        .setPriority(2)
                                    
                                    if pending_intent:
                                        update_notification.setContentIntent(pending_intent)
                                    
                                    nm.notify(1, update_notification.build())
                            else:
                                print("❌ First review failed")
                            
                            print("="*50 + "\n")
                    
                    except Exception as e:
                        print(f"⚠️ Config read error: {e}")
                
                # التحقق من موعد التشغيل التالي
                if loaded_file and next_play_time > 0:
                    current_time = time()
                    
                    if current_time >= next_play_time:
                        # التأكد من WakeLock
                        if not wakelock.isHeld():
                            wakelock.acquire()
                            print("🔒 WakeLock re-acquired")
                        
                        review_number = review_count + 1
                        print(f"\n🎵 Review #{review_number}...")
                        
                        success = play_audio_ultimate(loaded_file)
                        
                        if success:
                            review_count += 1
                            total_reviews += 1
                            current_step += 1
                            
                            if current_step < len(INTERVALS):
                                # لا يزال هناك مراجعات
                                next_play_time = time() + INTERVALS[current_step]
                                next_minutes = INTERVALS[current_step] // 60
                                next_seconds = INTERVALS[current_step] % 60
                                
                                print(f"✅ Review #{review_count} done")
                                print(f"⏰ Next review in: {next_minutes}m {next_seconds}s\n")
                                
                                # تحديث الإشعار
                                update_notification = NotificationBuilder(mService, channel_id) \
                                    .setContentTitle(f"🎯 Review #{review_count} Done") \
                                    .setContentText(f"Next in {next_minutes}m {next_seconds}s") \
                                    .setSmallIcon(17301659) \
                                    .setOngoing(True) \
                                    .setPriority(2)
                                
                                if pending_intent:
                                    update_notification.setContentIntent(pending_intent)
                                
                                nm.notify(1, update_notification.build())
                            else:
                                # انتهت جميع المراجعات
                                print("\n" + "="*50)
                                print(f"🎉 All {review_count} reviews completed!")
                                print("="*50 + "\n")
                                
                                loaded_file = None
                                next_play_time = 0
                                current_step = 0
                                
                                # تحرير WakeLock
                                if wakelock.isHeld():
                                    wakelock.release()
                                    print("🔓 WakeLock released")
                                
                                # إشعار الإكمال
                                complete_notification = NotificationBuilder(mService, channel_id) \
                                    .setContentTitle("✅ Session Complete!") \
                                    .setContentText(f"{review_count} reviews done successfully") \
                                    .setSmallIcon(17301659) \
                                    .setOngoing(False) \
                                    .build()
                                
                                nm.notify(1, complete_notification)
                                
                                review_count = 0
                        else:
                            print(f"❌ Review #{review_number} failed - will retry next cycle\n")
                
                # نوم قصير (1 ثانية)
                sleep(1)
            
            except Exception as e:
                print(f"⚠️ Loop error: {e}")
                import traceback
                traceback.print_exc()
                sleep(3)
    
    except Exception as e:
        print(f"💥 FATAL SERVICE ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_service()
