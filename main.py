"""
TAO x Tuna - Mobil Surum (Kivy + Crimson Void Konsepti)
Android (.apk) uyumlu mobil uygulama altyapisi.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, PushMatrix, PopMatrix, Rotate
import math
import unicodedata

# ---------- Renk Paleti (Hex -> Kivy RGBA 0-1) ----------
VOID = (0.019, 0.019, 0.019, 1)          # #050505
SURFACE = (0.058, 0.047, 0.047, 1)       # #0f0c0c
ELEVATED = (0.101, 0.050, 0.050, 1)      # #1a0d0d
SILVER = (0.631, 0.631, 0.666, 1)        # #a1a1aa
SILVER_BRIGHT = (1, 1, 1, 1)             # #ffffff
CRIMSON = (0.862, 0.149, 0.149, 1)       # #dc2626
CRIMSON_BRIGHT = (1.0, 0.2, 0.2, 1)      # #ff3333
ERROR_RED = (1.0, 0.101, 0.101, 1)       # #ff1a1a

TARGET_PHRASE = "aufarte malum ex vobis"
SECRET_PASSWORD = "UCYUCELERKABULEDECEK!"


def normalize(text: str) -> str:
    text = text.replace("İ", "i").replace("I", "i").replace("ı", "i")
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = " ".join(text.split())
    return text.strip()


class SigilWidget(FloatLayout):
    """Mobil uyumlu dönen mistik kırmızı Davut Yıldızı (Hexagram) mühür."""
    def __init__(self, size_hint=(None, None), size=(180, 180), **kwargs):
        super().__init__(**kwargs)
        self.size_hint = size_hint
        self.size = size
        self.angle = 0
        
        with self.canvas:
            self.rot_group = PushMatrix()
            self.rot = Rotate(angle=0, origin=(self.center_x, self.center_y))
            # Çizim talimatları burada güncellenecek
            self.draw_sigil()
            self.rot_group_pop = PopMatrix()
            
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        Clock.schedule_interval(self.animate, 1/35.0)

    def update_canvas(self, *args):
        self.rot.origin = self.center
        self.draw_sigil()

    def draw_sigil(self):
        self.canvas.clear()
        with self.canvas:
            Color(*CRIMSON)
            cx, cy = self.center_x, self.center_y
            
            # Halkalar
            Line(circle=(cx, cy, 82), width=2.5)
            Color(*CRIMSON_BRIGHT)
            Line(circle=(cx, cy, 68), width=3)
            Color(*CRIMSON)
            Line(circle=(cx, cy, 52), width=2)
            
            # Üçgenler için rotasyon uygulanan grup
            PushMatrix()
            self.rot = Rotate(angle=self.angle, origin=(cx, cy))
            
            Color(*SILVER_BRIGHT)
            pts1 = self._triangle_points(cx, cy, 58, 0)
            Line(points=pts1 + pts1[:2], width=3)
            
            Color(*CRIMSON_BRIGHT)
            pts2 = self._triangle_points(cx, cy, 58, 60)
            Line(points=pts2 + pts2[:2], width=3)
            
            PopMatrix()
            
            # Merkez çekirdek
            Color(*CRIMSON_BRIGHT)
            Ellipse(pos=(cx-8, cy-8), size=(16, 16))

    def _triangle_points(self, cx, cy, r, rotation_deg):
        pts = []
        for i in range(3):
            deg = rotation_deg + i * 120
            rad = math.radians(deg)
            pts.extend([cx + r * math.cos(rad), cy + r * math.sin(rad)])
        return pts

    def animate(self, dt):
        self.angle = (self.angle + 0.8) % 360
        self.draw_sigil()


class AnimatedSplashWelcomeScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Üst boşluk / Sigil
        sigil_container = FloatLayout(size_hint=(1, 0.6))
        sigil = SigilWidget(size=(160, 160))
        sigil.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        sigil_container.add_widget(sigil)
        layout.add_widget(sigil_container)
        
        # Marka yazısı
        brand_layout = BoxLayout(size_hint=(1, 0.2), spacing=5)
        lbl_tao = Label(text="TAO", font_size='36sp', bold=True, color=SILVER_BRIGHT)
        lbl_x = Label(text=" x ", font_size='36sp', bold=True, color=CRIMSON)
        lbl_tuna = Label(text="Tuna", font_size='36sp', bold=True, color=SILVER_BRIGHT)
        brand_layout.add_widget(lbl_tao)
        brand_layout.add_widget(lbl_x)
        brand_layout.add_widget(lbl_tuna)
        layout.add_widget(brand_layout)
        
        self.lbl_sub = Label(text="H o ş   g e l d i n !", font_size='18sp', color=CRIMSON_BRIGHT, size_hint=(1, 0.2))
        layout.add_widget(self.lbl_sub)
        
        self.add_widget(layout)
        
        # 6 saniye sonra şifre ekranına geçiş
        Clock.schedule_once(self.go_to_password, 6.0)

    def go_to_password(self, dt):
        self.manager.current = 'password'


class PasswordScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        layout.add_widget(Label(text="M Ü H Ü R L Ü   K A P I", font_size='22sp', bold=True, color=SILVER_BRIGHT, size_hint=(1, 0.2)))
        layout.add_widget(Label(text="Meclisin huzuruna geçmek için\nmühürlü parolayı fısılda, Paşam.", font_size='14sp', color=SILVER, size_hint=(1, 0.15), halign='center'))
        
        # Giriş alanı
        self.pwd_input = TextInput(
            text="", password=True, multiline=False,
            font_size='16sp', size_hint=(1, None), height=50,
            halign='center', background_color=(0.1, 0.05, 0.05, 1),
            foreground_color=SILVER_BRIGHT
        )
        layout.add_widget(self.pwd_input)
        
        self.hint_lbl = Label(text="", font_size='13sp', color=ERROR_RED, size_hint=(1, 0.1))
        layout.add_widget(self.hint_lbl)
        
        btn_open = Button(text="KAPIYI AÇ", font_size='16sp', bold=True, background_color=(0.86, 0.14, 0.14, 1), size_hint=(1, None), height=50)
        btn_open.bind(on_press=self.verify)
        layout.add_widget(btn_open)
        
        btn_exit = Button(text="✕ Çıkış Yap", font_size='14sp', color=SILVER, background_color=(0.05, 0.05, 0.05, 1), size_hint=(1, None), height=40)
        btn_exit.bind(on_press=lambda x: App.get_running_app().stop())
        layout.add_widget(btn_exit)
        
        self.add_widget(layout)

    def verify(self, instance):
        if self.pwd_input.text.strip() == SECRET_PASSWORD:
            self.manager.current = 'menu'
        else:
            self.hint_lbl.text = "Mühür reddedildi... Yanlış parola."


class MenuScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        sigil = SigilWidget(size=(140, 140))
        sigil.size_hint = (1, 0.4)
        layout.add_widget(sigil)
        
        layout.add_widget(Label(text="G İ Z L İ   M E C L İ S", font_size='16sp', color=CRIMSON_BRIGHT, size_hint=(1, 0.1)))
        
        btn_start = Button(text="BAŞLA", font_size='16sp', bold=True, background_color=(0.86, 0.14, 0.14, 1), size_hint=(1, None), height=50)
        btn_start.bind(on_press=lambda x: setattr(self.manager, 'current', 'spell'))
        layout.add_widget(btn_start)
        
        btn_credits = Button(text="CREDITS", font_size='16sp', bold=True, background_color=(0.86, 0.14, 0.14, 1), size_hint=(1, None), height=50)
        btn_credits.bind(on_press=lambda x: setattr(self.manager, 'current', 'credits'))
        layout.add_widget(btn_credits)
        
        btn_lock = Button(text="🔒 Sistemi Kilitle", font_size='14sp', color=SILVER, background_color=(0.05, 0.05, 0.05, 1), size_hint=(1, None), height=40)
        btn_lock.bind(on_press=lambda x: setattr(self.manager, 'current', 'password'))
        layout.add_widget(btn_lock)
        
        self.add_widget(layout)


class CreditsScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=40, spacing=15)
        
        layout.add_widget(Label(text="CREDITS", font_size='22sp', bold=True, color=SILVER_BRIGHT, size_hint=(1, 0.2)))
        layout.add_widget(Label(text="By TAOxTuna\nSadece TAO Eque's için.\nMimari & Tasarım: TAOxTuna", font_size='14sp', color=SILVER, halign='center', size_hint=(1, 0.5)))
        
        btn_back = Button(text="← Menüye Dön", font_size='14sp', color=SILVER, background_color=(0.05, 0.05, 0.05, 1), size_hint=(1, None), height=45)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(btn_back)
        
        self.add_widget(layout)


class SpellScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        layout.add_widget(Label(text="BÜYÜ ÇEMBERİ", font_size='22sp', bold=True, color=SILVER_BRIGHT, size_hint=(1, 0.2)))
        
        self.spell_input = TextInput(
            text="", multiline=False, font_size='15sp',
            size_hint=(1, None), height=50, halign='center',
            background_color=(0.1, 0.05, 0.05, 1), foreground_color=SILVER_BRIGHT
        )
        layout.add_widget(self.spell_input)
        
        self.hint_lbl = Label(text="", font_size='13sp', color=ERROR_RED, size_hint=(1, 0.1))
        layout.add_widget(self.hint_lbl)
        
        btn_cast = Button(text="FISILDA", font_size='16sp', bold=True, background_color=(0.86, 0.14, 0.14, 1), size_hint=(1, None), height=50)
        btn_cast.bind(on_press=self.check_spell)
        layout.add_widget(btn_cast)
        
        btn_back = Button(text="← Menüye Dön", font_size='14sp', color=SILVER, background_color=(0.05, 0.05, 0.05, 1), size_hint=(1, None), height=40)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def check_spell(self, instance):
        val = normalize(self.spell_input.text)
        if val == TARGET_PHRASE:
            self.manager.current = 'reveal'
        else:
            self.hint_lbl.text = "Sözler yanlış... tekrar dene."


class RevealScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        layout.add_widget(Label(text="3 Yüceler, büyünü kabul eylesin, Paşam!", font_size='20sp', bold=True, color=SILVER_BRIGHT, halign='center', size_hint=(1, 0.6)))
        
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'menu'), 3.5)
        self.add_widget(layout)


class TAOxTunaMobileApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AnimatedSplashWelcomeScreen(name='splash'))
        sm.add_widget(PasswordScreen(name='password'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(CreditsScreen(name='credits'))
        sm.add_widget(SpellScreen(name='spell'))
        sm.add_widget(RevealScreen(name='reveal'))
        return sm


if __name__ == '__main__':
    TAOxTunaMobileApp().run()