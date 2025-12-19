"""
Smart SRS - Ultimate Crash-Proof Version
Full English Interface
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
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    
    try:
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.FOREGROUND_SERVICE,
            Permission.WAKE_LOCK,
            Permission.POST_NOTIFICATIONS,
            Permission.SCHEDULE_EXACT_ALARM,
            Permission.USE_EXACT_ALARM
        ])
    except Exception as e:
        print(f"Permission error: {e}")

# Colors
COLOR_BG = (0.12, 0.14, 0.19, 1)
COLOR_BTN_START = (0.0, 0.7, 0.8, 1)
COLOR_BTN_STOP = (0.9, 0.3, 0.3, 1)
COLOR_TEXT = (0.9, 0.9, 0.9, 1)
COLOR_ACCENT = (0.2, 0.25, 0.3, 1)

class SRSPlayer(App):
    def build(self):
        Window.clearcolor = COLOR_BG
        
        self.is_running = False
        
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(app_dir, "srs_config.txt")

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.lbl_title = Label(text="Smart Review System", size_hint=(1, 0.1), font_size='24sp', bold=True, color=COLOR_BTN_START)
        layout.add_widget(self.lbl_title)

        self.lbl_info = Label(text="Select an audio file to begin...", size_hint=(1, 0.1), font_size='16sp', color=COLOR_TEXT)
        layout.add_widget(self.lbl_info)

        chooser_layout = BoxLayout(size_hint=(1, 0.6))
        with chooser_layout.canvas.before:
            Color(*COLOR_ACCENT)
            Rectangle(pos=chooser_layout.pos, size=chooser_layout.size)
        
        start_path = "/storage/emulated/0/" if platform == 'android' else os.getcwd()
        self.chooser = FileChooserIconView(
            path=start_path, 
            filters=['*.mp3', '*.wav', '*.ogg', '*.m4a']
        )
        layout.add_widget(self.chooser)

        self.btn_action = Button(
            text="START SESSION", 
            size_hint=(1, 0.15), 
            background_normal='', 
            background_color=COLOR_BTN_START, 
            font_size='20sp', 
            bold=True,
            color=(1,1,1,1)
        )
        self.btn_action.bind(on_press=self.toggle_session)
        layout.add_widget(self.btn_action)

        return layout

    def toggle_session(self, instance):
        try:
            if not self.is_running:
                if self.chooser.selection:
                    file_path = self.chooser.selection[0]
                    with open(self.config_path, "w") as f:
                        f.write(file_path)
                    self.is_running = True
                    self.btn_action.text = "STOP SESSION"
                    self.btn_action.background_color = COLOR_BTN_STOP
                    self.lbl_info.text = "Session started!"
                else:
                    self.lbl_info.text = "Please select a file first!"
            else:
                with open(self.config_path, "w") as f:
                    f.write("STOP")
                self.is_running = False
                self.btn_action.text = "START SESSION"
                self.btn_action.background_color = COLOR_BTN_START
                self.lbl_info.text = "Session stopped."
        except Exception as e:
            self.lbl_info.text = "Error: Try again"
            print(f"Toggle error: {e}")

if __name__ == '__main__':
    SRSPlayer().run()
