from yandex.Translater import Translater
import core.data.initdata as initdata

#TODO: настройка языка, возможно сделать настройку для каждого из сообщений
def init_yandex_service():
    tr = Translater()
    tr.set_key(initdata.yandex_token())
    tr.set_from_lang('en')
    tr.set_to_lang('ru')
    return tr

#сервис для перевода текста
tr = init_yandex_service()


def translate_text_message(message):
    tr.set_text(message)
    translate_text = tr.translate()
    return translate_text