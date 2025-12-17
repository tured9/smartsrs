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
        Permission.WAKE_LOCK
    ])
    
    try:
        service = autoclass('org.mysrs.smartsrs.ServiceSrsservice')
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        service.start(mActivity, '')
    except:
        pass

class SRSPlayer(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        
        self.config_path = os.path.join(os.path.dirname(__file__), "srs_config.txt")
        self.is_running = False
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text="Smart Review System", size_hint=(1, 0.1), 
                     font_size='26sp', bold=True)
        layout.add_widget(title)
        
        self.status = Label(text="اختر ملف صوتي", size_hint=(1, 0.08), 
                           font_size='16sp')
        layout.add_widget(self.status)
        
        info = Label(text="الفترات: 10 ثانية، دقيقة، 5 دقائق، 30 دقيقة، ساعة", 
                    size_hint=(1, 0.06), font_size='13sp')
        layout.add_widget(info)
        
        self.chooser = FileChooserIconView(
            path="/storage/emulated/0/",
            filters=['*.mp3', '*.wav', '*.ogg', '*.m4a'],
            size_hint=(1, 0.6)
        )
        layout.add_widget(self.chooser)
        
        self.btn = Button(text="ابدأ المراجعة", size_hint=(1, 0.12), 
                         font_size='20sp', bold=True,
                         background_color=(0, 0.7, 0.8, 1),
                         background_normal='')
        self.btn.bind(on_press=self.toggle)
        layout.add_widget(self.btn)
        
        return layout
    
    def toggle(self, instance):
        if not self.is_running:
            if self.chooser.selection:
                with open(self.config_path, "w") as f:
                    f.write(self.chooser.selection[0])
                
                self.is_running = True
                self.btn.text = "أوقف المراجعة"
                self.btn.background_color = (0.9, 0.3, 0.3, 1)
                self.status.text = "جاري المراجعة..."
            else:
                self.status.text = "اختر ملف أولاً!"
        else:
            with open(self.config_path, "w") as f:
                f.write("STOP")
            
            self.is_running = False
            self.btn.text = "ابدأ المراجعة"
            self.btn.background_color = (0, 0.7, 0.8, 1)
            self.status.text = "تم الإيقاف"

if __name__ == '__main__':
    SRSPlayer().run()
