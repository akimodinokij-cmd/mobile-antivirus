import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class AntivirusApp(App):

  def build(self):
    self.title = 'Мобильный Антивирус'
    layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

    self.header_label = Label(
        text='Мобильный сканер безопасности',
        font_size=20,
        size_hint_y=None,
        height=40,
        halign='center',
    )
    layout.add_widget(self.header_label)

    self.scan_btn = Button(
        text='Сканировать папку Загрузки',
        size_hint_y=None,
        height=60,
        background_color=(0.1, 0.5, 0.8, 1),
    )
    self.scan_btn.bind(on_press=self.start_scan)
    layout.add_widget(self.scan_btn)

    self.result_label = Label(
        text=(
            'Нажмите кнопку выше, чтобы начать проверку папки /sdcard/Download.'
        ),
        size_hint_y=None,
        halign='left',
        valign='top',
    )
    self.result_label.bind(
        width=lambda *x: setattr(
            self.result_label, 'text_size', (self.result_label.width, None)
        ),
        texture_size=lambda *x: setattr(
            self.result_label, 'height', self.result_label.texture_size[1]
        ),
    )

    scroll = ScrollView(size_hint=(1, 1))
    scroll.add_widget(self.result_label)
    layout.add_widget(scroll)

    return layout

  def start_scan(self, instance):
    target_dir = '/sdcard/Download'
    suspicious_ext = ['.vbs', '.bat', '.exe', '.scr', '.pif']
    found_files = []

    self.result_label.text = 'Идет сканирование файлов...\nПодождите.'

    try:
      if os.path.exists(target_dir):
        for root, dirs, files in os.walk(target_dir):
          for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in suspicious_ext:
              full_path = os.path.join(root, file)
              found_files.append(full_path)

        if found_files:
          result_text = (
              f'Внимание! Найдено подозрительных файлов: {len(found_files)}\n\n'
          )
          for path in found_files:
            result_text += f'- {path}\n'
          self.result_label.text = result_text
        else:
          self.result_label.text = (
              'Сканирование завершено!\nУгроз не обнаружено (папка чиста).'
          )
      else:
        self.result_label.text = 'Ошибка: папка Download не найдена.'
    except Exception as e:
      self.result_label.text = (
          f'Ошибка доступа:\n{str(e)}\n\nРазрешите приложению доступ к файлам.'
      )


if __name__ == '__main__':
  AntivirusApp().run()
