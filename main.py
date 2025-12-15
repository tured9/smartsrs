from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from plyer import filechooser  # إضافة plyer لمنتقي الملفات الأصلي
import os
# بدء الخدمة فوراً عند فتح التطبيق
if platform == 'android':
    from jnius import autoclass
    service = autoclass('org.mysrs.smartsrs.ServiceSrsservice')
    mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
    service.start(mActivity, '')
   
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.FOREGROUND_SERVICE,
        Permission.WAKE_LOCK,
        Permission.POST_NOTIFICATIONS
    ])
COLOR_BG = (0.12, 0.14, 0.19, 1)
COLOR_BTN_START = (0.0, 0.7, 0.8, 1)
COLOR_BTN_STOP = (0.9, 0.3, 0.3, 1)
class SRSPlayer(App):
    def build(self):
        Window.clearcolor = COLOR_BG
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(app_dir, "srs_config.txt")
        self.is_running = False
        self.selected_file = None  # متغير لتخزين مسار الملف المختار
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
       
        # العنوان
        layout.add_widget(Label(text="Smart Review System", size_hint=(1, 0.1), font_size='22sp', bold=True, color=COLOR_BTN_START))
       
        # زر إصلاح البطارية (ضروري)
        btn_fix = Button(text="🔋 ALLOW BACKGROUND RUN", size_hint=(1, 0.1), background_color=(1, 0.5, 0, 1))
        btn_fix.bind(on_press=self.open_settings)
        layout.add_widget(btn_fix)
        self.lbl_info = Label(text="Press Choose File & Start", size_hint=(1, 0.1), font_size='16sp')
        layout.add_widget(self.lbl_info)
       
        # زر اختيار الملف (بدلاً من FileChooserIconView)
        btn_choose = Button(text="Choose Audio File", size_hint=(1, 0.15), background_color=(0.3, 0.6, 0.9, 1), font_size='18sp')
        btn_choose.bind(on_press=self.choose_file)
        layout.add_widget(btn_choose)
       
        # عرض الملف المختار
        self.lbl_selected = Label(text="No file selected", size_hint=(1, 0.2), font_size='14sp', color=(1,1,1,1))
        layout.add_widget(self.lbl_selected)
       
        # زر البدء
        self.btn_action = Button(text="START SESSION", size_hint=(1, 0.15), background_normal='', background_color=COLOR_BTN_START, font_size='20sp', bold=True)
        self.btn_action.bind(on_press=self.toggle_system)
        layout.add_widget(self.btn_action)
        return layout
    
    def choose_file(self, instance):
        # فتح منتقي الملفات الأصلي مع فلاتر للملفات الصوتية
        filechooser.open_file(on_selection=self.handle_selection, filters=['*.mp3', '*.wav', '*.m4a'])
    
    def handle_selection(self, selection):
        # التعامل مع الاختيار (قائمة بمسارات الملفات)
        if selection:
            self.selected_file = selection[0]
            self.lbl_selected.text = f"Selected: {os.path.basename(self.selected_file)}"
            self.lbl_info.text = "File selected! Press Start."
        else:
            self.lbl_info.text = "No file selected."
    
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
            except:
                self.lbl_info.text = "Error opening settings"
    
    def toggle_system(self, instance):
        if not self.is_running:
            if self.selected_file:
                with open(self.config_path, "w") as f:
                    f.write(self.selected_file)
                self.is_running = True
                self.btn_action.text = "STOP SESSION"
                self.btn_action.background_color = COLOR_BTN_STOP
                self.lbl_info.text = "Session Started in Background!"
            else:
                self.lbl_info.text = "Choose a file first!"
        else:
            with open(self.config_path, "w") as f:
                f.write("STOP")
            self.is_running = False
            self.btn_action.text = "START SESSION"
            self.btn_action.background_color = COLOR_BTN_START
            self.lbl_info.text = "Stopped."
if __name__ == '__main__':
    SRSPlayer().run()
