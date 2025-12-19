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
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.FOREGROUND_SERVICE,
        Permission.WAKE_LOCK,
        Permission.POST_NOTIFICATIONS,
        Permission.SCHEDULE_EXACT_ALARM,
        Permission.USE_EXACT_ALARM
    ])
    
    try:
        service = autoclass('org.mysrs.smartsrs.ServiceSrsservice')
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        service.start(mActivity, '')
    except: pass

class SRSPlayer(App):
    def build(self):
        Window.clearcolor = (0.08, 0.1, 0.14, 1)
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(app_dir, "srs_config.txt")
        self.is_running = False

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="Smart SRS Ultimate", size_hint=(1, 0.1), font_size='24sp', bold=True, color=(0, 0.8, 1, 1)))
        
        btn_fix = Button(text="⚡ ALLOW BACKGROUND RUN (Click Me)", size_hint=(1, 0.1), background_color=(1, 0.5, 0, 1))
        btn_fix.bind(on_press=self.open_settings)
        layout.add_widget(btn_fix)

        self.lbl_info = Label(text="Select File...", size_hint=(1, 0.05))
        layout.add_widget(self.lbl_info)

        self.chooser = FileChooserIconView(path="/storage/emulated/0/", filters=['*.mp3', '*.wav', '*.m4a'])
        layout.add_widget(self.chooser)

        self.btn_action = Button(text="START SESSION", size_hint=(1, 0.15), background_color=(0, 0.8, 0, 1), font_size='20sp', bold=True)
        self.btn_action.bind(on_press=self.toggle)
        layout.add_widget(self.btn_action)

        return layout

    def open_settings(self, instance):
        if platform == 'android':
            try:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                Intent = autoclass('android.content.Intent')
                Settings = autoclass('android.provider.Settings')
                Uri = autoclass('android.net.Uri')
                intent = Intent()
                intent.setAction(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
                intent.setData(Uri.parse("package:" + activity.getPackageName()))
                activity.startActivity(intent)
            except: pass

    def toggle(self, instance):
        if not self.is_running:
            if self.chooser.selection:
                with open(self.config_path, "w") as f:
                    f.write(self.chooser.selection[0])
                self.is_running = True
                self.btn_action.text = "STOP"
                self.btn_action.background_color = (1, 0, 0, 1)
            else:
                self.lbl_info.text = "Select file!"
        else:
            with open(self.config_path, "w") as f:
                f.write("STOP")
            self.is_running = False
            self.btn_action.text = "START"
            self.btn_action.background_color = (0, 0.8, 0, 1)

if __name__ == '__main__':
    SRSPlayer().run()
