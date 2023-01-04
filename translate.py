# Imports the Google Cloud Translation library
from google.cloud import translate


# Initialize Translation client
def translate_text(text="YOUR_TEXT_TO_TRANSLATE", project_id="YOUR_PROJECT_ID"):
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from Russian to Chinese
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "ru",
            "target_language_code": "zh-CN,zh,zh-TW"
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text))


#с аудио

    if lang[0] == "ru": # если язык русский
        transed = translator.translate(message.text, lang_tgt="zh-CN") # переводим
        voice = gtts.gTTS(transed) # делаем гс
        voice.save(transed + ".mp3") # сохраняем гс
        bot.reply_to(message, transed) #отправляем переведённый текст
        bot.send_audio(message.chat.id, audio=open(transed + ".mp", "rb")) # отправляем озвучку
        os.remove(transed + ".mp3") # удаляем файл гс (озвучки)
    else:
        bot.reply_to(message, "Я вас не понял") # если нас чего-то не устраивает (например сообщение всё из символов)

    elif lang[0] == "zh-CN": # если язык китайский (далее код аналогичен вышеприведённому)
        transed = translator.translate(message.text,lang_tgt="ru") # только тут меняем lang_tgt="ru" на ру (переводит с английского на русский)
        voice = gtts.gTTS(transed)
        voice.save(transed + ".mp3")
        bot.reply_to(message, transed)
        bot.send_audio(message.chat.id, audio=open(transed +".mp3", "rb"))
        os.remove(transed + ".mp3")
    else:
        bot.reply_to(message, "Я вас не понял") # если нас чего-то не устраивает (например сообщение всё из символов)


