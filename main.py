from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

import time
import os

# --- الألوان الحديثة (Modern Palette) ---
COLOR_BG = (0.12, 0.14, 0.19, 1)      # خلفية داكنة احترافية
COLOR_BTN_START = (0.0, 0.7, 0.8, 1)  # تركواز للتشغيل
COLOR_BTN_STOP = (0.9, 0.3, 0.3, 1)   # أحمر هادئ للإيقاف
COLOR_TEXT = (0.9, 0.9, 0.9, 1)       # أبيض مائل للرمادي
COLOR_ACCENT = (0.2, 0.25, 0.3, 1)    # لون خلفية المستعرض

# فترات التكرار
INTERVALS = [10, 60, 300, 1800, 3600]

class SRSPlayer(App):
    def build(self):
        # تعيين لون خلفية التطبيق بالكامل
        Window.clearcolor = COLOR_BG
        
        self.sound = None
        self.queue_index = 0
        self.next_time = 0
        self.is_running = False

        # التخطيط الرئيسي مع هوامش (Padding)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # --- العنوان ---
        self.lbl_title = Label(
            text="Smart Review System", 
            size_hint=(1, 0.1), 
            font_size='24sp', 
            bold=True,
            color=COLOR_BTN_START
        )
        layout.add_widget(self.lbl_title)

        # --- حالة التطبيق ---
        self.lbl_info = Label(
            text="Select an audio file to begin...", 
            size_hint=(1, 0.1), 
            font_size='16sp', 
            color=COLOR_TEXT
        )
        layout.add_widget(self.lbl_info)

        # --- مستعرض الملفات (داخل خلفية مميزة) ---
        # نقوم بإنشاء حاوية للمستعرض لتمييز لونه
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

        # --- الزر الرئيسي (تصميم مسطح Flat Design) ---
        self.btn_action = Button(
            text="START SESSION", 
            size_hint=(1, 0.15), 
            background_normal='', # إلغاء الخلفية الرمادية الافتراضية
            background_color=COLOR_BTN_START, 
            font_size='20sp', 
            bold=True,
            color=(1,1,1,1)
        )
        self.btn_action.bind(on_press=self.toggle_system)
        layout.add_widget(self.btn_action)

        Clock.schedule_interval(self.background_loop, 1)
        return layout

    def toggle_system(self, instance):
        if not self.is_running:
            self.start_process()
        else:
            self.stop_process()

    def start_process(self):
        if self.chooser.selection:
            try:
                file_path = self.chooser.selection[0]
                self.sound = SoundLoader.load(file_path)
                if self.sound:
                    self.is_running = True
                    self.queue_index = 0
                    
                    # تغيير شكل الزر عند التشغيل
                    self.btn_action.text = "STOP SESSION"
                    self.btn_action.background_color = COLOR_BTN_STOP
                    
                    self.schedule_next_play()
                else:
                    self.lbl_info.text = "Error: Invalid Audio File!"
                    self.lbl_info.color = (1, 0, 0, 1)
            except Exception as e:
                self.lbl_info.text = "Error loading file"
        else:
            self.lbl_info.text = "Please select a file first!"
            self.lbl_info.color = (1, 1, 0, 1)

    def stop_process(self):
        self.is_running = False
        self.next_time = 0
        if self.sound and self.sound.state == 'play':
            self.sound.stop()
        
        # إعادة الزر لحالته الطبيعية
        self.btn_action.text = "START SESSION"
        self.btn_action.background_color = COLOR_BTN_START
        self.lbl_info.text = "Session Stopped."
        self.lbl_info.color = COLOR_TEXT

    def schedule_next_play(self):
        if self.queue_index < len(INTERVALS):
            wait = INTERVALS[self.queue_index]
            self.next_time = time.time() + wait
            self.lbl_info.text = f"Next replay in: {wait} seconds"
            self.lbl_info.color = COLOR_BTN_START
            self.queue_index += 1
        else:
            self.lbl_info.text = "All reviews finished for today."
            self.stop_process()

    def background_loop(self, dt):
        if self.is_running and self.next_time > 0:
            rem = int(self.next_time - time.time())
            if rem > 0:
                self.lbl_info.text = f"Review #{self.queue_index} in: {rem}s"
            
            if time.time() >= self.next_time:
                if self.sound:
                    self.sound.play()
                    self.lbl_info.text = "🔊 Listening now..."
                    self.lbl_info.color = (0, 1, 0, 1)
                    
                    self.next_time = time.time() + 999999
                    dur = self.sound.length if self.sound.length > 0 else 5
                    Clock.schedule_once(lambda dt: self.schedule_next_play(), dur + 2)

if __name__ == '__main__':
    SRSPlayer().run()
