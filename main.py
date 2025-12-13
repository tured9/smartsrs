from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.utils import platform
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import os

# بدء الخدمة فوراً
if platform == 'android':
    from jnius import autoclass
    service = autoclass('org.mysrs.smartsrs.ServiceSrsservice')
    mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
    service.start(mActivity, '')
    
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.FOREGROUND_SERVICE
    ])

COLOR_BG = (0.12, 0.14, 0.19, 1)
COLOR_BTN_START = (0.0, 0.7, 0.8, 1)
COLOR_BTN_STOP = (0.9, 0.3, 0.3, 1)

class SRSPlayer(App):
    def build(self):
        Window.clearcolor = COLOR_BG
        self.is_running = False
        
        # تحديد المسار الصحيح لملف الإعدادات
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(app_dir, "srs_config.txt")

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="Smart Review System", size_hint=(1, 0.1), font_size='24sp', bold=True, color=COLOR_BTN_START))
        self.lbl_info = Label(text="Select File & Start", size_hint=(1, 0.1), font_size='16sp')
        layout.add_widget(self.lbl_info)

        chooser_layout = BoxLayout(size_hint=(1, 0.6))
        with chooser_layout.canvas.before:
            Color(0.2, 0.25, 0.3, 1)
            Rectangle(pos=chooser_layout.pos, size=chooser_layout.size)
            
        self.chooser = FileChooserIconView(path="/storage/emulated/0/", filters=['*.mp3', '*.wav', '*.ogg', '*.m4a'])
        layout.add_widget(self.chooser)

        self.btn_action = Button(text="START BACKGROUND SESSION", size_hint=(1, 0.15), background_normal='', background_color=COLOR_BTN_START, font_size='18sp', bold=True)
        self.btn_action.bind(on_press=self.toggle_system)
        layout.add_widget(self.btn_action)

        return layout

    def toggle_system(self, instance):
        if not self.is_running:
            if self.chooser.selection:
                file_path = self.chooser.selection[0]
                
                # كتابة المسار للخدمة
                try:
                    with open(self.config_path, "w") as f:
                        f.write(file_path)
                    
                    self.is_running = True
                    self.btn_action.text = "STOP SESSION"
                    self.btn_action.background_color = COLOR_BTN_STOP
                    self.lbl_info.text = "Running in Background! (Check Notification)"
                except Exception as e:
                    self.lbl_info.text = f"Error: {e}"
            else:
                self.lbl_info.text = "Select a file first!"
        else:
            # إرسال أمر التوقف
            with open(self.config_path, "w") as f:
                f.write("STOP")
            
            self.is_running = False
            self.btn_action.text = "START BACKGROUND SESSION"
            self.btn_action.background_color = COLOR_BTN_START
            self.lbl_info.text = "Session Stopped."

if __name__ == '__main__':
    SRSPlayer().run()
