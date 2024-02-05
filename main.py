import cv2,time,base64,json,os,asyncio
from roboflow import Roboflow
from typing import Final, Set
from telegram import Update, Chat, Message
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN: Final = ""
BOT_USERNAME: Final = ""
AUTHORIZED_USERNAMES: Set[str] = {""}

rtsp_url = ""
chat_id = ""

api_key = ""
model_endpoint = ""
version_number = ""

rf = Roboflow(api_key)


project = rf.workspace().project(model_endpoint)
model = project.version(version_number).model

is_watching = False


async def kapiyigozetle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Yetkili kullanıcı kontrolü
    if update.message.from_user.username not in AUTHORIZED_USERNAMES:
        await update.message.reply_text("Bu komutu kullanma izniniz yok.")
        return

    global is_watching, chat_id

    # Gözetlemeyi başlat
    if not is_watching:
        await update.message.reply_text("Gözetlemeye başladım!")
        print("gözlem başladı")
        is_watching = True
        chat_id = update.message.chat_id

        while is_watching and context.update_queue.empty():
            cap = cv2.VideoCapture(rtsp_url)
            ret, frame = cap.read()
            cap.release()

            predict = model.predict(frame).json()
            predictions = predict.get('predictions')
            if predictions:
                if predictions[0].get('class') == "human" and predictions[0].get('confidence') > 0.66:
                    print("insan var")
                    cv2.imwrite("image.jpg", frame)
                    with open("image.jpg", "rb") as image_file:
                        await update.message.reply_photo(image_file)
                        await update.message.reply_text("Biri Geldi!")
            else:
                print("insan yok")

            await asyncio.sleep(15)

    # Gözetlemeyi durdur
    else:
        is_watching = False
        await update.message.reply_text("Gözetleme durduruldu!")


async def stop_watching(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_watching
    is_watching = False
    print("gözlem durdu")
    await update.message.reply_text("Gözetleme durduruldu.")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hoş geldin, kapıya bakıyorum.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yardım için @xanovi ile iletişime geç!")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Yetkili kullanıcı kontrolü
    if update.message.from_user.username not in AUTHORIZED_USERNAMES:
        await update.message.reply_text("Bu botu kullanma izniniz yok.")
        return

    await update.message.reply_text("Bu bir özel komuttur.")


async def handle_first_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Yetkili kullanıcı kontrolü
    if update.message.from_user.username not in AUTHORIZED_USERNAMES:
        await update.message.reply_text("Bu botu kullanma yetkiniz yok. @xanovi ile iletişime geçebilirsiniz!")
        return
    user_message: str = update.message.text.lower()

    # Benimle ilgili bir şey söylenmişse cevap ver
    if "selam" in user_message or "merhaba" in user_message or "naber" in user_message:
        response: str = "Merhaba! Nasıl yardımcı olabilirim?"
    else:
        response: str = "Henüz geliştirilme aşamasında olduğum için şuanda buna cevap veremiyorum @xanovi ile iletişime geçebilirsin!"

    # Cevabı kullanıcıya gönder
    await update.message.reply_text(response)


async def kapiyi_goster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Yetkili kullanıcı kontrolü
    if update.message.from_user.username not in AUTHORIZED_USERNAMES:
        await update.message.reply_text("Bu komutu kullanma izniniz yok.")
        return

    # RTSP URL'sini girin
    rtsp_url = ""

    # Video yakalama nesnesini oluşturun
    cap = cv2.VideoCapture(rtsp_url)

    # İlk kareyi yakalayın
    ret, frame = cap.read()

    # Görüntüyü kaydedin
    cv2.imwrite("image.jpg", frame)

    # Video akışını serbest bırakın
    cap.release()

    # Belleği temizleyin
    cv2.destroyAllWindows()

    with open("image.jpg", "rb") as image_file:
        await update.message.reply_photo(image_file)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Program is starting")
    app = Application.builder().token(TOKEN).build()
    # Komutlar
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler("kapiyabak", kapiyi_goster))
    app.add_handler(CommandHandler("kapiyigozetle", kapiyigozetle))
    app.add_handler(CommandHandler('gozetlemeyidurdur', stop_watching))

    # İlk mesaj kontrolü
    app.add_handler(MessageHandler(filters.TEXT, handle_first_message))
    # Hata
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=5)
