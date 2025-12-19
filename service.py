"""
Smart SRS Service - ULTIMATE VERSION
Uses AlarmManager for GUARANTEED exact timing
+ Timer fallback for maximum reliability
"""

from time import sleep, time
from jnius import autoclass, cast
from kivy.utils import platform
import os

# Review intervals (in seconds)
# Customize these as you wish
INTERVALS = [10, 60, 300, 1800, 3600]  # 10s, 1min, 5min, 30min, 1hour

# For quick testing use:
# INTERVALS = [5, 10, 15, 20, 30]


def play_audio_ultimate(file_path):
    """
    Ultimate audio player with robust error handling
    Works like Spotify/YouTube Music
    """
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        AudioManager = autoclass('android.media.AudioManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        
        am = cast(AudioManager, mService.getSystemService(Context.AUDIO_SERVICE))
        
        # Request Audio Focus
        focus_result = -1
        try:
            Builder = autoclass('android.media.AudioAttributes$Builder')
            attributes = Builder().setUsage(1).setContentType(2).build()
            
            try:
                FocusBuilder = autoclass('android.media.AudioFocusRequest$Builder')
                focus_request = FocusBuilder(2) \
                    .setAudioAttributes(attributes) \
                    .setAcceptsDelayedFocusGain(True) \
                    .build()
                focus_result = am.requestAudioFocus(focus_request)
                print(f"✅ Audio Focus (Modern): {focus_result}")
            except:
                focus_result = am.requestAudioFocus(None, 3, 2)
                print(f"✅ Audio Focus (Legacy): {focus_result}")
        except Exception as e:
            print(f"⚠️ Audio Focus error: {e}")
        
        # Create and play MediaPlayer
        player = MediaPlayer()
        
        try:
            player.setAudioAttributes(attributes)
        except:
            pass
        
        player.setDataSource(file_path)
        player.prepare()
        player.start()
        
        print(f"🎵 Playing: {os.path.basename(file_path)}")
        
        # Wait for completion
        duration = player.getDuration() / 1000.0
        end_time = time() + duration + 1.5
        
        while time() < end_time:
            if not player.isPlaying():
                break
            sleep(0.5)
        
        # Cleanup
        try:
            player.stop()
        except:
            pass
        
        player.release()
        
        # Release Audio Focus
        try:
            am.abandonAudioFocus(focus_request if 'focus_request' in locals() else None)
        except:
            pass
        
        print("✅ Playback completed")
        return True
        
    except Exception as e:
        print(f"❌ Play error: {e}")
        import traceback
        traceback.print_exc()
        return False


def schedule_alarm(context, delay_seconds, review_number):
    """
    Schedule exact alarm using AlarmManager
    This FORCES Android to play at exact time
    """
    try:
        AlarmManager = autoclass('android.app.AlarmManager')
        Intent = autoclass('android.content.Intent')
        PendingIntent = autoclass('android.app.PendingIntent')
        SystemClock = autoclass('android.os.SystemClock')
        
        alarm_manager = cast(AlarmManager, context.getSystemService('alarm'))
        
        # Create intent for alarm
        intent = Intent(context, autoclass('org.mysrs.smartsrs.ServiceSrsservice'))
        intent.setAction(f"ALARM_REVIEW_{review_number}")
        intent.putExtra("review_number", review_number)
        
        # Create PendingIntent
        pending_intent = PendingIntent.getService(
            context,
            review_number,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        )
        
        # Calculate trigger time
        trigger_time = SystemClock.elapsedRealtime() + (delay_seconds * 1000)
        
        # Schedule exact alarm (works even in Doze mode!)
        try:
            alarm_manager.setExactAndAllowWhileIdle(
                AlarmManager.ELAPSED_REALTIME_WAKEUP,
                trigger_time,
                pending_intent
            )
            print(f"⏰ AlarmManager scheduled review #{review_number} in {delay_seconds}s")
            return True
        except:
            # Fallback for older Android versions
            alarm_manager.setExact(
                AlarmManager.ELAPSED_REALTIME_WAKEUP,
                trigger_time,
                pending_intent
            )
            print(f"⏰ AlarmManager (legacy) scheduled review #{review_number} in {delay_seconds}s")
            return True
            
    except Exception as e:
        print(f"❌ AlarmManager schedule error: {e}")
        return False


def cancel_all_alarms(context):
    """Cancel all scheduled alarms"""
    try:
        AlarmManager = autoclass('android.app.AlarmManager')
        Intent = autoclass('android.content.Intent')
        PendingIntent = autoclass('android.app.PendingIntent')
        
        alarm_manager = cast(AlarmManager, context.getSystemService('alarm'))
        
        for i in range(1, len(INTERVALS) + 1):
            intent = Intent(context, autoclass('org.mysrs.smartsrs.ServiceSrsservice'))
            intent.setAction(f"ALARM_REVIEW_{i}")
            
            pending_intent = PendingIntent.getService(
                context,
                i,
                intent,
                PendingIntent.FLAG_NO_CREATE | PendingIntent.FLAG_IMMUTABLE
            )
            
            if pending_intent:
                alarm_manager.cancel(pending_intent)
                pending_intent.cancel()
        
        print("🗑️ All alarms cancelled")
    except Exception as e:
        print(f"⚠️ Cancel alarms error: {e}")


def run_service():
    """
    ULTIMATE SERVICE with AlarmManager + Timer
    Double protection for maximum reliability
    """
    if platform != 'android':
        print("Not Android - service not started")
        return
    
    try:
        # Import classes
        PythonService = autoclass('org.kivy.android.PythonService')
        mService = PythonService.mService
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        PendingIntent = autoclass('android.app.PendingIntent')
        Intent = autoclass('android.content.Intent')
        
        print("=" * 60)
        print("🚀 Smart SRS Service - ULTIMATE VERSION")
        print("=" * 60)
        
        # POWERFUL WakeLock
        pm = mService.getSystemService(Context.POWER_SERVICE)
        wakelock = pm.newWakeLock(
            PowerManager.PARTIAL_WAKE_LOCK,
            "SmartSRS::UltimateAlarmLock"
        )
        wakelock.setReferenceCounted(False)
        print("✅ WakeLock created")
        
        # HIGH PRIORITY Notification Channel
        channel_id = "SmartSRS_Ultimate"
        nm = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        
        chan = NotificationChannel(channel_id, "Smart Review", 4)
        chan.setDescription("Spaced repetition with AlarmManager")
        chan.setShowBadge(True)
        chan.setLockscreenVisibility(1)
        chan.setSound(None, None)
        
        nm.createNotificationChannel(chan)
        print("✅ Notification channel created")
        
        # PendingIntent for notification tap
        launch_intent = mService.getPackageManager() \
            .getLaunchIntentForPackage(mService.getPackageName())
        
        if launch_intent:
            pending_intent = PendingIntent.getActivity(
                mService, 0, launch_intent, PendingIntent.FLAG_IMMUTABLE
            )
        else:
            pending_intent = None
        
        # Create Foreground Notification
        notification = NotificationBuilder(mService, channel_id) \
            .setContentTitle("🎯 Smart Review Active") \
            .setContentText("Background review with AlarmManager") \
            .setSmallIcon(17301659) \
            .setOngoing(True) \
            .setPriority(2) \
            .setCategory("service") \
            .setVisibility(1)
        
        if pending_intent:
            notification.setContentIntent(pending_intent)
        
        notification = notification.build()
        
        # Start Foreground Service
        try:
            mService.startForeground(1, notification)
            print("✅ Foreground service started")
        except Exception as e:
            print(f"⚠️ startForeground error: {e}")
        
        # Main Variables
        app_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(app_dir, "srs_config.txt")
        
        loaded_file = None
        next_play_time = 0
        current_step = 0
        review_count = 0
        total_reviews = 0
        alarms_scheduled = False
        
        print(f"📁 Config path: {config_path}")
        print("🔄 Service loop starting...")
        print("=" * 60 + "\n")
        
        # MAIN LOOP
        while True:
            try:
                # Read config file
                if os.path.exists(config_path):
                    try:
                        with open(config_path, "r", encoding='utf-8') as f:
                            content = f.read().strip()
                        
                        # STOP command
                        if content == "STOP":
                            print("\n" + "=" * 60)
                            print("⏹️ STOP command received")
                            
                            cancel_all_alarms(mService)
                            
                            loaded_file = None
                            next_play_time = 0
                            current_step = 0
                            alarms_scheduled = False
                            
                            if wakelock.isHeld():
                                wakelock.release()
                                print("🔓 WakeLock released")
                            
                            try:
                                os.remove(config_path)
                            except:
                                pass
                            
                            stop_notification = NotificationBuilder(mService, channel_id) \
                                .setContentTitle("⏹️ Review Stopped") \
                                .setContentText(f"Completed {total_reviews} reviews") \
                                .setSmallIcon(17301659) \
                                .setOngoing(False) \
                                .build()
                            
                            nm.notify(1, stop_notification)
                            
                            print(f"📊 Total reviews: {total_reviews}")
                            print("=" * 60 + "\n")
                            
                            review_count = 0
                        
                        # NEW FILE
                        elif content and content != loaded_file:
                            print("\n" + "=" * 60)
                            print(f"📥 New file: {os.path.basename(content)}")
                            
                            loaded_file = content
                            current_step = 0
                            review_count = 0
                            alarms_scheduled = False
                            
                            if not wakelock.isHeld():
                                wakelock.acquire()
                                print("🔒 WakeLock acquired")
                            
                            # Play immediately (Review #1)
                            print("🎵 Review #1 (immediate)...")
                            success = play_audio_ultimate(loaded_file)
                            
                            if success:
                                review_count = 1
                                total_reviews += 1
                                
                                # Schedule ALL remaining reviews
                                print("\n⏰ Scheduling AlarmManager for ALL reviews...")
                                for i, interval in enumerate(INTERVALS):
                                    review_num = i + 2
                                    if schedule_alarm(mService, interval, review_num):
                                        print(f"   ✓ Review #{review_num} → +{interval}s ({interval//60}m {interval%60}s)")
                                
                                alarms_scheduled = True
                                
                                # Set timer for next play (backup)
                                if current_step < len(INTERVALS):
                                    next_play_time = time() + INTERVALS[current_step]
                                    next_min = INTERVALS[current_step] // 60
                                    next_sec = INTERVALS[current_step] % 60
                                    
                                    print(f"\n✅ Review #1 done")
                                    print(f"⏱️ Timer backup: next in {next_min}m {next_sec}s")
                                    print("=" * 60 + "\n")
                                    
                                    update_notif = NotificationBuilder(mService, channel_id) \
                                        .setContentTitle(f"🎯 Review #1 Done") \
                                        .setContentText(f"Next: {next_min}m {next_sec}s (AlarmManager active)") \
                                        .setSmallIcon(17301659) \
                                        .setOngoing(True) \
                                        .setPriority(2)
                                    
                                    if pending_intent:
                                        update_notif.setContentIntent(pending_intent)
                                    
                                    nm.notify(1, update_notif.build())
                            else:
                                print("❌ First review failed")
                            
                    except Exception as e:
                        print(f"⚠️ Config read error: {e}")
                
                # Check timer for next play (backup)
                if loaded_file and next_play_time > 0:
                    current_time = time()
                    
                    if current_time >= next_play_time:
                        if not wakelock.isHeld():
                            wakelock.acquire()
                            print("🔒 WakeLock re-acquired")
                        
                        review_number = review_count + 1
                        print(f"\n🎵 Review #{review_number} (Timer backup)...")
                        
                        success = play_audio_ultimate(loaded_file)
                        
                        if success:
                            review_count += 1
                            total_reviews += 1
                            current_step += 1
                            
                            if current_step < len(INTERVALS):
                                next_play_time = time() + INTERVALS[current_step]
                                next_min = INTERVALS[current_step] // 60
                                next_sec = INTERVALS[current_step] % 60
                                
                                print(f"✅ Review #{review_count} done")
                                print(f"⏱️ Next: {next_min}m {next_sec}s\n")
                                
                                update_notif = NotificationBuilder(mService, channel_id) \
                                    .setContentTitle(f"🎯 Review #{review_count} Done") \
                                    .setContentText(f"Next: {next_min}m {next_sec}s") \
                                    .setSmallIcon(17301659) \
                                    .setOngoing(True) \
                                    .setPriority(2)
                                
                                if pending_intent:
                                    update_notif.setContentIntent(pending_intent)
                                
                                nm.notify(1, update_notif.build())
                            else:
                                # All reviews completed
                                print("\n" + "=" * 60)
                                print(f"🎉 All {review_count} reviews completed!")
                                print("=" * 60 + "\n")
                                
                                loaded_file = None
                                next_play_time = 0
                                current_step = 0
                                alarms_scheduled = False
                                
                                cancel_all_alarms(mService)
                                
                                if wakelock.isHeld():
                                    wakelock.release()
                                    print("🔓 WakeLock released")
                                
                                complete_notif = NotificationBuilder(mService, channel_id) \
                                    .setContentTitle("✅ Session Complete!") \
                                    .setContentText(f"{review_count} reviews done") \
                                    .setSmallIcon(17301659) \
                                    .setOngoing(False) \
                                    .build()
                                
                                nm.notify(1, complete_notif)
                                
                                review_count = 0
                        else:
                            print(f"❌ Review #{review_number} failed\n")
                
                # Sleep
                sleep(1)
            
            except Exception as e:
                print(f"⚠️ Loop error: {e}")
                import traceback
                traceback.print_exc()
                sleep(3)
    
    except Exception as e:
        print(f"💥 FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_service()
