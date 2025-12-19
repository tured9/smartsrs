from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder

if 'android' in App.get_running_app().get_application_name().lower():
    from jnius import autoclass, cast
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    AlarmManager = autoclass('android.app.AlarmManager')
    PendingIntent = autoclass('android.app.PendingIntent')
    Intent = autoclass('android.content.Intent')
    PowerManager = autoclass('android.os.PowerManager')
    Service = autoclass('org.kivy.android.PythonService')

class AudioChooser(BoxLayout):
    selected_file = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='اختر ملف صوتي:'))
        filechooser = FileChooserListView(filters=['*.mp3', '*.wav'])
        filechooser.bind(selection=self.select_file)
        self.add_widget(filechooser)
        start_btn = Button(text='بدء المراجعة المتباعدة')
        start_btn.bind(on_press=self.start_spaced_repetition)
        self.add_widget(start_btn)

    def select_file(self, chooser, selection):
        if selection:
            self.selected_file = selection[0]

    def start_spaced_repetition(self, instance):
        if not self.selected_file:
            popup = Popup(title='خطأ', content=Label(text='يرجى اختيار ملف صوتي أولاً'), size_hint=(0.8, 0.4))
            popup.open()
            return

        # الأوقات بالثواني
        intervals = [10, 30, 60, 300, 1500, 1800, 3600]  # 10s, 30s, 1m, 5m, 25m, 30m, 1h
        current_time = int(Clock.get_time() * 1000)  # milliseconds

        activity = PythonActivity.mActivity
        context = cast(Context, activity.getApplicationContext())
        alarm_manager = cast(AlarmManager, context.getSystemService(Context.ALARM_SERVICE))

        for i, interval in enumerate(intervals):
            trigger_time = current_time + (interval * 1000)
            intent = Intent()
            intent.setClassName(context.getPackageName(), 'org.kivy.android.PythonService')
            intent.putExtra('audio_file', self.selected_file)
            pending_intent = PendingIntent.getService(context, i, intent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE)

            # استخدم setExactAndAllowWhileIdle للدقة حتى في Doze mode
            alarm_manager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, trigger_time, pending_intent)

        popup = Popup(title='نجاح', content=Label(text='تم جدولة التشغيل!'), size_hint=(0.8, 0.4))
        popup.open()

class SpacedAudioApp(App):
    def build(self):
        return AudioChooser()

if __name__ == '__main__':
    SpacedAudioApp().run()
