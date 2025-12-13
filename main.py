from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.utils import platform
import time
import os

INTERVALS = [10, 60, 300, 1800, 3600]

class SRSPlayer(App):
    def build(self):
        self.sound = None
        self.queue_index = 0
        self.next_time = 0
        self.is_running = False
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        self.lbl_info = Label(text="اختر ملفاً صوتياً للبدء", size_hint=(1, 0.15), font_size='18sp', halign='center')
        self.lbl_info.bind(size=self.lbl_info.setter('text_size')) 
        layout.add_widget(self.lbl_info)
        start_path = "/storage/emulated/0/" if platform == 'android' else os.getcwd()
        self.chooser = FileChooserIconView(path=start_path, filters=['*.mp3', '*.wav', '*.ogg', '*.m4a'])
        layout.add_widget(self.chooser)
        self.btn_action = Button(text="بدء الجدولة الذكية", size_hint=(1, 0.2), background_color=(0.1, 0.7, 0.1, 1), font_size='22sp', bold=True)
        self.btn_action.bind(on_press=self.toggle_system)
        layout.add_widget(self.btn_action)
        Clock.schedule_interval(self.background_loop, 1)
        return layout

    def toggle_system(self, instance):
        if not self.is_running: self.start_process()
        else: self.stop_process()

    def start_process(self):
        if self.chooser.selection:
            try:
                file_path = self.chooser.selection[0]
                self.sound = SoundLoader.load(file_path)
                if self.sound:
                    self.is_running = True; self.queue_index = 0
                    self.btn_action.text = "إيقاف وإنهاء الجلسة"; self.btn_action.background_color = (0.9, 0.1, 0.1, 1)
                    self.schedule_next_play()
                else: self.lbl_info.text = "فشل تشغيل الملف"
            except Exception as e: self.lbl_info.text = str(e)
        else: self.lbl_info.text = "اختر ملفاً أولاً!"

    def stop_process(self):
        self.is_running = False; self.next_time = 0
        if self.sound and self.sound.state == 'play': self.sound.stop()
        self.btn_action.text = "بدء الجدولة الذكية"; self.btn_action.background_color = (0.1, 0.7, 0.1, 1)
        self.lbl_info.text = "تم الإيقاف."

    def schedule_next_play(self):
        if self.queue_index < len(INTERVALS):
            wait = INTERVALS[self.queue_index]
            self.next_time = time.time() + wait
            self.lbl_info.text = f"التشغيل القادم بعد: {wait} ثانية"
            self.queue_index += 1
        else: self.lbl_info.text = "انتهت الجلسة."; self.stop_process()

    def background_loop(self, dt):
        if self.is_running and self.next_time > 0:
            rem = int(self.next_time - time.time())
            if rem > 0: self.lbl_info.text = f"المراجعة ({self.queue_index}): بعد {rem} ثانية"
            if time.time() >= self.next_time:
                if self.sound:
                    self.sound.play(); self.lbl_info.text = "جاري الاستماع..."
                    self.next_time = time.time() + 999999
                    dur = self.sound.length if self.sound.length > 0 else 5
                    Clock.schedule_once(lambda dt: self.schedule_next_play(), dur + 2)

if __name__ == '__main__': SRSPlayer().run()
