"""
Smart SRS - Final Version with AlarmManager
Complete English Interface
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.utils import platform
from kivy.core.window import Window
import os

if platform == 'android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    
    # Request all necessary permissions
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.FOREGROUND_SERVICE,
        Permission.WAKE_LOCK,
        Permission.POST_NOTIFICATIONS,
        Permission.SCHEDULE_EXACT_ALARM,
        Permission.USE_EXACT_ALARM
    ])
    
    # Disable battery optimization
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        Intent = autoclass('android.content.Intent')
        Settings = autoclass('android.provider.Settings')
        Uri = autoclass('android.net.Uri')
        PowerManager = autoclass('android.os.PowerManager')
        Context = autoclass('android.content.Context')
        
        pm = activity.getSystemService(Context.POWER_SERVICE)
        
        if hasattr(pm, 'isIgnoringBatteryOptimizations'):
            if not pm.isIgnoringBatteryOptimizations(activity.getPackageName()):
                intent = Intent()
                intent.setAction(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
                intent.setData(Uri.parse("package:" + activity.getPackageName()))
                try:
                    activity.startActivity(intent)
                    print("✅ Battery optimization request opened")
                except:
                    print("⚠️ Could not open battery settings")
    except Exception as e:
        print(f"Battery check error: {e}")
    
    # Start service
    try:
        service = autoclass('org.mysrs.smartsrs.ServiceSrsservice')
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        service.start(mActivity, '')
        print("✅ Service started successfully")
    except Exception as e:
        print(f"❌ Service start error: {e}")

# Colors
COLOR_BG = (0.08, 0.10, 0.14, 1)
COLOR_PRIMARY = (0.2, 0.7, 0.9, 1)
COLOR_DANGER = (0.95, 0.25, 0.25, 1)
COLOR_SUCCESS = (0.2, 0.85, 0.4, 1)
COLOR_WARNING = (1.0, 0.7, 0.0, 1)
COLOR_TEXT = (0.95, 0.95, 0.95, 1)


class SRSPlayer(App):
    def build(self):
        Window.clearcolor = COLOR_BG
        
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(app_dir, "srs_config.txt")
        self.is_running = False
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=25, spacing=18)
        
        # Main title
        title = Label(
            text="🎯 Smart Review System",
            size_hint=(1, 0.09),
            font_size='28sp',
            bold=True,
            color=COLOR_PRIMARY
        )
        layout.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text="Spaced Repetition Made Easy",
            size_hint=(1, 0.05),
            font_size='15sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(subtitle)
        
        # Status label
        self.status_label = Label(
            text="📁 Select an audio file to begin",
            size_hint=(1, 0.08),
            font_size='17sp',
            color=COLOR_TEXT,
            bold=True
        )
        layout.add_widget(self.status_label)
        
        # Review schedule info
        intervals_box = BoxLayout(orientation='vertical', size_hint=(1, 0.12), spacing=5)
        
        intervals_title = Label(
            text="⏱️ Review Schedule:",
            size_hint=(1, 0.4),
            font_size='15sp',
            color=COLOR_WARNING,
            bold=True
        )
        intervals_box.add_widget(intervals_title)
        
        intervals_text = Label(
            text="10 sec → 1 min → 5 min → 30 min → 1 hour",
            size_hint=(1, 0.6),
            font_size='13sp',
            color=(0.8, 0.8, 0.8, 1)
        )
        intervals_box.add_widget(intervals_text)
        
        layout.add_widget(intervals_box)
        
        # File chooser
        chooser_container = BoxLayout(size_hint=(1, 0.5), padding=5)
        
        self.file_chooser = FileChooserIconView(
            path="/storage/emulated/0/",
            filters=['*.mp3', '*.wav', '*.ogg', '*.m4a', '*.aac', '*.flac'],
            size_hint=(1, 1)
        )
        chooser_container.add_widget(self.file_chooser)
        
        layout.add_widget(chooser_container)
        
        # Start/Stop button
        self.action_button = Button(
            text="▶️ START REVIEW",
            size_hint=(1, 0.13),
            background_normal='',
            background_color=COLOR_SUCCESS,
            font_size='24sp',
            bold=True
        )
        self.action_button.bind(on_press=self.toggle_session)
        layout.add_widget(self.action_button)
        
        # Important tip
        tip_label = Label(
            text="💡 Make sure to disable battery optimization",
            size_hint=(1, 0.06),
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            italic=True
        )
        layout.add_widget(tip_label)
        
        return layout
    
    def toggle_session(self, instance):
        """Start or stop review session"""
        if not self.is_running:
            # Start session
            if self.file_chooser.selection:
                file_path = self.file_chooser.selection[0]
                file_name = os.path.basename(file_path)
                
                try:
                    # Write file path
                    with open(self.config_path, "w", encoding='utf-8') as f:
                        f.write(file_path)
                    
                    self.is_running = True
                    self.action_button.text = "⏸️ STOP REVIEW"
                    self.action_button.background_color = COLOR_DANGER
                    
                    # Show file name (truncated)
                    short_name = file_name[:30] + "..." if len(file_name) > 30 else file_name
                    self.status_label.text = f"🎵 Reviewing: {short_name}"
                    self.status_label.color = COLOR_SUCCESS
                    
                    print(f"✅ Session started: {file_path}")
                    
                except Exception as e:
                    print(f"❌ Error starting session: {e}")
                    self.status_label.text = "❌ Error starting session"
                    self.status_label.color = COLOR_DANGER
            else:
                self.status_label.text = "⚠️ Please select a file first"
                self.status_label.color = COLOR_WARNING
        else:
            # Stop session
            try:
                with open(self.config_path, "w", encoding='utf-8') as f:
                    f.write("STOP")
                
                self.is_running = False
                self.action_button.text = "▶️ START REVIEW"
                self.action_button.background_color = COLOR_SUCCESS
                self.status_label.text = "⏹️ Session stopped"
                self.status_label.color = (0.7, 0.7, 0.7, 1)
                
                print("⏹️ Session stopped")
                
            except Exception as e:
                print(f"❌ Error stopping session: {e}")


if __name__ == '__main__':
    SRSPlayer().run()
