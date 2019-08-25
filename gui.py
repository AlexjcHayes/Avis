from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty

Window.clearcolor = (0.5, 0.5, 0.5, 1)
Window.size = (300, 100)


class User(Screen):
    test1 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.test1.focus and keycode == 40:  # 40 - Enter key pressed
            self.abc()

    def abc(self):
        print('Test')


class Avis(App):

    def build(self):
        return self.root


if __name__ == '__main__':
    Avis().run()