"""
main.py - التطبيق الرئيسي المحسن
يعمل مثل تطبيقات الموسيقى المحترفة
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.utils import platform
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import os

# بدء الخدمة
if platform == 'android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    
    # طلب الأذونات
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.FOREGROUND_SERVICE,
        Permission.WAKE_LOCK,
        Permission.MODIFY_AUDIO_SETTINGS,
        Permission.POST_NOTIFICATIONS
    ])
    
    # بدء الخدمة
    try:
        service = autoclass('org.mysrs.smartsrs.ServiceSrsservice')
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        service.start(mActivity, '')
        print("Service started successfully!")
    except Exception as e:
        print(f"Service start error: {e}")

# الألوان
COLOR_BG = (0.12, 0.14, 0.19, 1)
COLOR_PRIMARY = (0.0, 0.7, 0.8, 1)
COLOR_DANGER = (0.9, 0.3, 0.3, 1)
COLOR_WARNING = (0.95, 0.65, 0.15, 1)
COLOR_SUCCESS = (0.2, 0.8, 0.4, 1)


class SRSPlayer(App):
    def build(self):
        Window.clearcolor = COLOR_BG
        
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(app_dir, "srs_config.txt")
        self.is_running = False
        
        # التخطيط الرئيسي
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # العنوان
        title = Label(
            text="🎯 Smart Review System",
            size_hint=(1, 0.1),
            font_size='26sp',
            bold=True,
            color=COLOR_PRIMARY
        )
        layout.add_widget(title)
        
        # زر إصلاح البطارية
        btn_battery = Button(
            text="⚙️ Battery Optimization (Required)",
            size_hint=(1, 0.08),
            background_normal='',
            background_color=COLOR_WARNING,
            font_size='15sp',
            bold=True
        )
        btn_battery.bind(on_press=self.fix_battery_optimization)
        layout.add_widget(btn_battery)
        
        # معلومات الحالة
        self.lbl_status = Label(
            text="📁 Select an audio file to start",
            size_hint=(1, 0.08),
            font_size='16sp',
            color=(1, 1, 1, 0.9)
        )
        layout.add_widget(self.lbl_status)
        
        # معلومات الفترات
        intervals_text = "⏱️ Intervals: 10s, 1m, 5m, 30m, 1h"
        lbl_intervals = Label(
            text=intervals_text,
            size_hint=(1, 0.06),
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(lbl_intervals)
        
        # مستعرض الملفات
        chooser_box = BoxLayout(size_hint=(1, 0.5))
        with chooser_box.canvas.before:
            Color(0.2, 0.25, 0.3, 1)
            Rectangle(pos=chooser_box.pos, size=chooser_box.size)
        
        self.chooser = FileChooserIconView(
            path="/storage/emulated/0/",
            filters=['*.mp3', '*.wav', '*.ogg', '*.m4a', '*.aac']
        )
        chooser_box.add_widget(self.chooser)
        layout.add_widget(chooser_box)
        
        # زر البدء/الإيقاف
        self.btn_action = Button(
            text="▶️ START SESSION",
            size_hint=(1, 0.12),
            background_normal='',
            background_color=COLOR_SUCCESS,
            font_size='22sp',
            bold=True
        )
        self.btn_action.bind(on_press=self.toggle_system)
        layout.add_widget(self.btn_action)
        
        # نصائح
        tips = Label(
            text="💡 Tip: Keep app unlocked in battery settings",
            size_hint=(1, 0.06),
            font_size='13sp',
            color=(0.6, 0.6, 0.6, 1),
            italic=True
        )
        layout.add_widget(tips)
        
        return layout
    
    def fix_battery_optimization(self, instance):
        """فتح إعدادات تحسين البطارية"""
        if platform == 'android':
            try:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                Intent = autoclass('android.content.Intent')
                Settings = autoclass('android.provider.Settings')
                Uri = autoclass('android.net.Uri')
                
                # فتح إعدادات تحسين البطارية
                intent = Intent()
                intent.setAction(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
                intent.setData(Uri.parse("package:" + activity.getPackageName()))
                activity.startActivity(intent)
                
                self.lbl_status.text = "✅ Battery settings opened"
                self.lbl_status.color = COLOR_SUCCESS
                
            except Exception as e:
                print(f"Battery optimization error: {e}")
                self.lbl_status.text = "⚠️ Go to Settings → Apps → Battery manually"
                self.lbl_status.color = COLOR_WARNING
    
    def toggle_system(self, instance):
        """بدء أو إيقاف نظام المراجعة"""
        if not self.is_running:
            # بدء المراجعة
            if self.chooser.selection:
                file_path = self.chooser.selection[0]
                file_name = os.path.basename(file_path)
                
                # كتابة الملف
                try:
                    with open(self.config_path, "w") as f:
                        f.write(file_path)
                    
                    self.is_running = True
                    self.btn_action.text = "⏸️ STOP SESSION"
                    self.btn_action.background_color = COLOR_DANGER
                    self.lbl_status.text = f"🎵 Reviewing: {file_name[:25]}..."
                    self.lbl_status.color = COLOR_SUCCESS
                    
                    print(f"Session started: {file_path}")
                    
                except Exception as e:
                    print(f"Error writing config: {e}")
                    self.lbl_status.text = "❌ Error starting session"
                    self.lbl_status.color = COLOR_DANGER
            else:
                self.lbl_status.text = "⚠️ Please select a file first"
                self.lbl_status.color = COLOR_WARNING
        else:
            # إيقاف المراجعة
            try:
                with open(self.config_path, "w") as f:
                    f.write("STOP")
                
                self.is_running = False
                self.btn_action.text = "▶️ START SESSION"
                self.btn_action.background_color = COLOR_SUCCESS
                self.lbl_status.text = "⏹️ Session stopped"
                self.lbl_status.color = (0.7, 0.7, 0.7, 1)
                
                print("Session stopped")
                
            except Exception as e:
                print(f"Error stopping session: {e}")


if __name__ == '__main__':
    SRSPlayer().run()
