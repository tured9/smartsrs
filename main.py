"""
Smart SRS - Fixed Version
Stable startup with proper error handling
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.utils import platform
from kivy.core.window import Window
import os
import traceback

# Android-specific imports
PythonActivity = None
if platform == 'android':
    try:
        from android.permissions import request_permissions, Permission
        from jnius import autoclass, cast
        
        # Request basic permissions first
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])
        
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except Exception as e:
        print(f"Android setup error: {e}")

# Colors
COLOR_BG = (0.08, 0.10, 0.14, 1)
COLOR_PRIMARY = (0.2, 0.7, 0.9, 1)
COLOR_DANGER = (0.95, 0.25, 0.25, 1)
COLOR_SUCCESS = (0.2, 0.85, 0.4, 1)
COLOR_WARNING = (1.0, 0.7, 0.0, 1)
COLOR_TEXT = (0.95, 0.95, 0.95, 1)


class SRSPlayer(App):
    def build(self):
        try:
            Window.clearcolor = COLOR_BG
            
            # Setup paths
            if platform == 'android':
                from android.storage import app_storage_path
                app_dir = app_storage_path()
            else:
                app_dir = os.path.dirname(os.path.abspath(__file__))
            
            self.config_path = os.path.join(app_dir, "srs_config.txt")
            self.is_running = False
            
            print(f"App directory: {app_dir}")
            print(f"Config path: {self.config_path}")
            
            # Main layout
            layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
            
            # Title
            title = Label(
                text="🎯 Smart Review System",
                size_hint=(1, 0.1),
                font_size='26sp',
                bold=True,
                color=COLOR_PRIMARY
            )
            layout.add_widget(title)
            
            # Status
            self.status_label = Label(
                text="📁 Select an audio file to begin",
                size_hint=(1, 0.08),
                font_size='16sp',
                color=COLOR_TEXT
            )
            layout.add_widget(self.status_label)
            
            # Review schedule
            schedule_label = Label(
                text="⏱️ Schedule: 10s → 1m → 5m → 30m → 1h",
                size_hint=(1, 0.06),
                font_size='14sp',
                color=COLOR_WARNING
            )
            layout.add_widget(schedule_label)
            
            # File chooser
            if platform == 'android':
                default_path = "/storage/emulated/0/"
            else:
                default_path = os.path.expanduser("~")
            
            self.file_chooser = FileChooserIconView(
                path=default_path,
                filters=['*.mp3', '*.wav', '*.ogg', '*.m4a'],
                size_hint=(1, 0.6)
            )
            layout.add_widget(self.file_chooser)
            
            # Action button
            self.action_button = Button(
                text="▶️ START REVIEW",
                size_hint=(1, 0.12),
                background_normal='',
                background_color=COLOR_SUCCESS,
                font_size='22sp',
                bold=True
            )
            self.action_button.bind(on_press=self.toggle_session)
            layout.add_widget(self.action_button)
            
            # Start service after UI is ready
            if platform == 'android':
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: self.start_service(), 2)
            
            print("✅ UI built successfully")
            return layout
            
        except Exception as e:
            print(f"❌ Build error: {e}")
            traceback.print_exc()
            
            # Fallback minimal UI
            layout = BoxLayout(orientation='vertical', padding=20)
            error_label = Label(
                text=f"❌ Error starting app:\n{str(e)}",
                color=(1, 0, 0, 1)
            )
            layout.add_widget(error_label)
            return layout
    
    def start_service(self):
        """Start service after UI is ready"""
        try:
            if platform != 'android':
                return
            
            # Request additional permissions
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.FOREGROUND_SERVICE,
                Permission.WAKE_LOCK,
                Permission.POST_NOTIFICATIONS,
            ])
            
            # Start service
            service = autoclass('org.mysrs.smartsrs.ServiceSrsservice')
            mActivity = PythonActivity.mActivity
            service.start(mActivity, '')
            
            print("✅ Service started")
            self.status_label.text = "✅ Service ready"
            
        except Exception as e:
            print(f"⚠️ Service start error: {e}")
            self.status_label.text = "⚠️ Service not available"
    
    def toggle_session(self, instance):
        """Start or stop review session"""
        try:
            if not self.is_running:
                # Start
                if self.file_chooser.selection:
                    file_path = self.file_chooser.selection[0]
                    file_name = os.path.basename(file_path)
                    
                    # Write config
                    with open(self.config_path, "w", encoding='utf-8') as f:
                        f.write(file_path)
                    
                    self.is_running = True
                    self.action_button.text = "⏸️ STOP"
                    self.action_button.background_color = COLOR_DANGER
                    
                    short_name = file_name[:25] + "..." if len(file_name) > 25 else file_name
                    self.status_label.text = f"🎵 {short_name}"
                    self.status_label.color = COLOR_SUCCESS
                    
                    print(f"✅ Started: {file_path}")
                else:
                    self.status_label.text = "⚠️ Select a file first"
                    self.status_label.color = COLOR_WARNING
            else:
                # Stop
                with open(self.config_path, "w", encoding='utf-8') as f:
                    f.write("STOP")
                
                self.is_running = False
                self.action_button.text = "▶️ START"
                self.action_button.background_color = COLOR_SUCCESS
                self.status_label.text = "⏹️ Stopped"
                self.status_label.color = (0.7, 0.7, 0.7, 1)
                
                print("⏹️ Stopped")
                
        except Exception as e:
            print(f"❌ Toggle error: {e}")
            self.status_label.text = f"❌ Error: {str(e)}"
            self.status_label.color = COLOR_DANGER


if __name__ == '__main__':
    try:
        SRSPlayer().run()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        traceback.print_exc()
