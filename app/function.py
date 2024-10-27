# Обработчик для голосовых сообщений
# @dp.message(types.ContentType.VOICE)
# async def voice_message(message: Message):
#     if message.voice:
#         voice = await message.voice.get_file()
#         file_path = f"{DOWNLOAD_FOLDER}/{voice.file_id}.ogg"
#         await bot.download_file(voice.file_path, file_path)