import logging
import telebot

from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaVideo
)

# ==================================================
# 1. BOT CONFIGURATION
# ==================================================
# Yahan apna Telegram Bot Token directly paste karein:
BOT_TOKEN = "8916953762:AAEg493ZtcCDx8Ux0ZXWcUVaQMnI6hgsbk4"

if not BOT_TOKEN or BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
    raise RuntimeError("Kripya sahi Telegram Bot Token paste karein!")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("demo_bot")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ==================================================
# 5 & 6. PLANS & DIRECT HOSTED URLS CONFIGURATION
# ==================================================
# Plan 1 se 9 tak direct public video URLs ke placeholders hain.
# Plan 10 mein image URL use hoga.
PLANS = [
    {
        "id": 1,
        "name": "Plan 1 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan1",
        "videos": [
            "https://videotourl.com/videos/placeholder_1_1.mp4",
            "https://videotourl.com/videos/placeholder_1_2.mp4",
            "https://videotourl.com/videos/placeholder_1_3.mp4",
            "https://videotourl.com/videos/placeholder_1_4.mp4",
            "https://videotourl.com/videos/placeholder_1_5.mp4",
        ],
    },
    {
        "id": 2,
        "name": "Plan 2 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan2",
        "videos": [
            "https://videotourl.com/videos/placeholder_2_1.mp4",
            "https://videotourl.com/videos/placeholder_2_2.mp4",
            "https://videotourl.com/videos/placeholder_2_3.mp4",
            "https://videotourl.com/videos/placeholder_2_4.mp4",
            "https://videotourl.com/videos/placeholder_2_5.mp4",
        ],
    },
    {
        "id": 3,
        "name": "Plan 3 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan3",
        "videos": [
            "https://videotourl.com/videos/placeholder_3_1.mp4",
            "https://videotourl.com/videos/placeholder_3_2.mp4",
            "https://videotourl.com/videos/placeholder_3_3.mp4",
            "https://videotourl.com/videos/placeholder_3_4.mp4",
            "https://videotourl.com/videos/placeholder_3_5.mp4",
        ],
    },
    {
        "id": 4,
        "name": "Plan 4 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan4",
        "videos": [
            "https://videotourl.com/videos/placeholder_4_1.mp4",
            "https://videotourl.com/videos/placeholder_4_2.mp4",
            "https://videotourl.com/videos/placeholder_4_3.mp4",
            "https://videotourl.com/videos/placeholder_4_4.mp4",
            "https://videotourl.com/videos/placeholder_4_5.mp4",
        ],
    },
    {
        "id": 5,
        "name": "Plan 5 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan5",
        "videos": [
            "https://videotourl.com/videos/placeholder_5_1.mp4",
            "https://videotourl.com/videos/placeholder_5_2.mp4",
            "https://videotourl.com/videos/placeholder_5_3.mp4",
            "https://videotourl.com/videos/placeholder_5_4.mp4",
            "https://videotourl.com/videos/placeholder_5_5.mp4",
        ],
    },
    {
        "id": 6,
        "name": "Plan 6 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan6",
        "videos": [
            "https://videotourl.com/videos/placeholder_6_1.mp4",
            "https://videotourl.com/videos/placeholder_6_2.mp4",
            "https://videotourl.com/videos/placeholder_6_3.mp4",
            "https://videotourl.com/videos/placeholder_6_4.mp4",
            "https://videotourl.com/videos/placeholder_6_5.mp4",
        ],
    },
    {
        "id": 7,
        "name": "Plan 7 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan7",
        "videos": [
            "https://videotourl.com/videos/placeholder_7_1.mp4",
            "https://videotourl.com/videos/placeholder_7_2.mp4",
            "https://videotourl.com/videos/placeholder_7_3.mp4",
            "https://videotourl.com/videos/placeholder_7_4.mp4",
            "https://videotourl.com/videos/placeholder_7_5.mp4",
        ],
    },
    {
        "id": 8,
        "name": "Plan 8 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan8",
        "videos": [
            "https://videotourl.com/videos/placeholder_8_1.mp4",
            "https://videotourl.com/videos/placeholder_8_2.mp4",
            "https://videotourl.com/videos/placeholder_8_3.mp4",
            "https://videotourl.com/videos/placeholder_8_4.mp4",
            "https://videotourl.com/videos/placeholder_8_5.mp4",
        ],
    },
    {
        "id": 9,
        "name": "Plan 9 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan9",
        "videos": [
            "https://videotourl.com/videos/placeholder_9_1.mp4",
            "https://videotourl.com/videos/placeholder_9_2.mp4",
            "https://videotourl.com/videos/placeholder_9_3.mp4",
            "https://videotourl.com/videos/placeholder_9_4.mp4",
            "https://videotourl.com/videos/placeholder_9_5.mp4",
        ],
    },
    {
        "id": 10,
        "name": "Plan 10 Demo",
        "buy_url": "https://yourpaymentgateway.com/pay/plan10",
        "image": "https://videotourl.com/images/placeholder_plan_10.jpg",
    },
]

# User ID -> messages belonging to the currently displayed demo.
active_demos = {}


# ==================================================
# KEYBOARD HELPERS
# ==================================================

def make_button(text, callback_data=None, url=None, style=None):
    kwargs = {"text": text}
    if callback_data is not None:
        kwargs["callback_data"] = callback_data
    if url is not None:
        kwargs["url"] = url

    if style:
        try:
            return InlineKeyboardButton(**kwargs, style=style)
        except (TypeError, ValueError):
            pass

    return InlineKeyboardButton(**kwargs)


def get_plan(plan_id):
    return next((plan for plan in PLANS if plan["id"] == plan_id), None)


def valid_url(url):
    return (
        isinstance(url, str)
        and url.strip()
        and not url.startswith("PASTE_")
    )


# ==================================================
# DELETE CURRENT DEMO
# ==================================================

def delete_demo(user_id):
    demo = active_demos.pop(user_id, None)
    if not demo:
        return

    chat_id = demo["chat_id"]
    for message_id in reversed(demo["message_ids"]):
        try:
            bot.delete_message(chat_id, message_id)
        except Exception:
            log.info("Could not delete message %s", message_id)


# ==================================================
# START / PLAN MENU
# ==================================================

def send_plan_menu(chat_id):
    kb = InlineKeyboardMarkup(row_width=2)

    for plan in PLANS:
        kb.add(
            make_button(
                plan["name"],
                callback_data=f"plan:{plan['id']}",
                style="danger"
            )
        )

    bot.send_message(
        chat_id,
        "Select your plan to see the demo.",
        reply_markup=kb
    )


@bot.message_handler(commands=["start"])
def start(message):
    delete_demo(message.from_user.id)
    send_plan_menu(message.chat.id)


# ==================================================
# SHOW DEMO (VIDEOS OR IMAGE FOR PLAN 10)
# ==================================================

@bot.callback_query_handler(func=lambda call: call.data.startswith("plan:"))
def show_demo(call):
    bot.answer_callback_query(call.id)

    try:
        plan_id = int(call.data.split(":")[1])
    except (ValueError, IndexError):
        return

    plan = get_plan(plan_id)
    if not plan:
        bot.answer_callback_query(call.id, "Plan nahi mila.", show_alert=True)
        return

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    delete_demo(user_id)
    message_ids = []

    # Plan 10 Image Logic
    if plan_id == 10:
        image_url = plan.get("image", "")
        if "placeholder" in image_url:
            log.warning("Plan 10 image URL placeholder replace nahi kiya gaya.")

        kb = InlineKeyboardMarkup(row_width=2)
        kb.row(
            make_button("Buy Now", callback_data=f"buy:{plan_id}", style="success"),
            make_button("Change Plan", callback_data="change_plan", style="primary")
        )

        try:
            sent_img = bot.send_photo(
                chat_id=chat_id,
                photo=image_url if valid_url(image_url) else "https://picsum.photos/600/400",
                caption="Plan 10 Demo Image\n\nTap the buttons below:",
                reply_markup=kb
            )
            message_ids.append(sent_img.message_id)
        except Exception as e:
            log.exception("Could not send Plan 10 image")
            bot.send_message(chat_id, f"<b>Error:</b> Image load karne mein samasya aayi.\n<pre>{e}</pre>")
            return

        active_demos[user_id] = {"chat_id": chat_id, "message_ids": message_ids}
        return

    # Plans 1 to 9 Video Logic (Direct hosted URLs with spoiler)
    videos = [v.strip() for v in plan.get("videos", []) if valid_url(v)]

    if not videos:
        bot.send_message(chat_id, "Is plan ke demo video URLs abhi add nahi kiye gaye.")
        return

    media = []
    for idx, video_url in enumerate(videos[:10]):
        try:
            media.append(
                InputMediaVideo(
                    media=video_url,
                    has_spoiler=True,
                    caption="Demo Video" if idx == 0 else None
                )
            )
        except Exception as e:
            log.error(f"Error creating InputMediaVideo for {video_url}: {e}")

    try:
        sent_media = bot.send_media_group(chat_id, media)
        for msg in sent_media:
            message_ids.append(msg.message_id)
    except Exception as e:
        log.exception("Could not send demo media group")
        bot.send_message(chat_id, f"<b>Telegram API Error:</b> Videos send nahi ho paaye.\n<pre>{e}</pre>")
        send_plan_menu(chat_id)
        return

    kb = InlineKeyboardMarkup(row_width=2)
    kb.row(
        make_button("Buy Now", callback_data=f"buy:{plan_id}", style="success"),
        make_button("Change Plan", callback_data="change_plan", style="primary")
    )

    try:
        instruction = bot.send_message(
            chat_id,
            "Tap the video to watch the demo.",
            reply_markup=kb
        )
        message_ids.append(instruction.message_id)
    except Exception as e:
        log.exception("Could not send instruction message")
        delete_demo(user_id)
        return

    active_demos[user_id] = {
        "chat_id": chat_id,
        "message_ids": message_ids
    }


# ==================================================
# BUY NOW
# ==================================================

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy:"))
def buy_now(call):
    try:
        plan_id = int(call.data.split(":")[1])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Invalid plan.")
        return

    plan = get_plan(plan_id)
    if not plan:
        bot.answer_callback_query(call.id, "Plan nahi mila.", show_alert=True)
        return

    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    delete_demo(user_id)

    kb = InlineKeyboardMarkup()
    kb.add(make_button("Proceed to Payment", url=plan["buy_url"], style="success"))
    kb.add(make_button("Change Plan", callback_data="change_plan", style="primary"))

    bot.send_message(
        chat_id,
        f"Aapne {plan['name']} चुना है। Payment complete karne ke liye niche diye gaye button par click karein:",
        reply_markup=kb
    )


# ==================================================
# CHANGE PLAN
# ==================================================

@bot.callback_query_handler(func=lambda call: call.data == "change_plan")
def change_plan(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    delete_demo(user_id)
    send_plan_menu(chat_id)


# ==================================================
# RUN BOT
# ==================================================

if __name__ == "__main__":
    log.info("Demo bot starting...")
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
