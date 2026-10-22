
import logging
import telebot

from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaVideo,
)

# ==================================================
# BOT TOKEN — YAHAN APNA TOKEN DALO
# ==================================================

TOKEN = "8916953762:AAHIY62LgS0lxFF1ubdwCAQuqMrlkriF2po"

if TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE" or not TOKEN.strip():
    raise RuntimeError("main.py mein apna bot token daalo.")

bot = telebot.TeleBot(TOKEN.strip())

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("demo_bot")


# ==================================================
# PLANS
# Plan 1-9: Hosted video URLs
# Plan 10: Hosted image URL only
# ==================================================

PLANS = [
    {
        "id": 1,
        "name": "𝙈𝙊𝙈 𝘼𝙉𝘿 𝙎𝙊𝙉 😍🔥",
        "buy_url": "https://example.com/buy1",
        "videos": [
            "https://videotourl.com/videos/1791609652325-1646ca32-e73f-4a5a-9874-a0f4e401c6bb.mp4",
            "https://videotourl.com/videos/1791610410648-c50ab2d2-b1b2-4998-8f5f-43a5f719b603.mp4",
            "https://videotourl.com/videos/1791609530271-d1845e11-78bd-4465-a0e3-3e0dd57fb424.mp4",
            "https://videotourl.com/videos/1791609530271-d1845e11-78bd-4465-a0e3-3e0dd57fb424.mp4",
            "https://your-host.com/plan1-video5.mp4",
        ],
    },
    {
        "id": 2,
        "name": "Plan 2 Demo",
        "buy_url": "https://example.com/buy2",
        "videos": [
            "https://your-host.com/plan2-video1.mp4",
            "https://your-host.com/plan2-video2.mp4",
            "https://your-host.com/plan2-video3.mp4",
            "https://your-host.com/plan2-video4.mp4",
            "https://your-host.com/plan2-video5.mp4",
        ],
    },
    {
        "id": 3,
        "name": "Plan 3 Demo",
        "buy_url": "https://example.com/buy3",
        "videos": [
            "https://your-host.com/plan3-video1.mp4",
            "https://your-host.com/plan3-video2.mp4",
            "https://your-host.com/plan3-video3.mp4",
            "https://your-host.com/plan3-video4.mp4",
            "https://your-host.com/plan3-video5.mp4",
        ],
    },
    {
        "id": 4,
        "name": "Plan 4 Demo",
        "buy_url": "https://example.com/buy4",
        "videos": [
            "https://your-host.com/plan4-video1.mp4",
            "https://your-host.com/plan4-video2.mp4",
            "https://your-host.com/plan4-video3.mp4",
            "https://your-host.com/plan4-video4.mp4",
            "https://your-host.com/plan4-video5.mp4",
        ],
    },
    {
        "id": 5,
        "name": "Plan 5 Demo",
        "buy_url": "https://example.com/buy5",
        "videos": [
            "https://your-host.com/plan5-video1.mp4",
            "https://your-host.com/plan5-video2.mp4",
            "https://your-host.com/plan5-video3.mp4",
            "https://your-host.com/plan5-video4.mp4",
            "https://your-host.com/plan5-video5.mp4",
        ],
    },
    {
        "id": 6,
        "name": "Plan 6 Demo",
        "buy_url": "https://example.com/buy6",
        "videos": [
            "https://your-host.com/plan6-video1.mp4",
            "https://your-host.com/plan6-video2.mp4",
            "https://your-host.com/plan6-video3.mp4",
            "https://your-host.com/plan6-video4.mp4",
            "https://your-host.com/plan6-video5.mp4",
        ],
    },
    {
        "id": 7,
        "name": "Plan 7 Demo",
        "buy_url": "https://example.com/buy7",
        "videos": [
            "https://your-host.com/plan7-video1.mp4",
            "https://your-host.com/plan7-video2.mp4",
            "https://your-host.com/plan7-video3.mp4",
            "https://your-host.com/plan7-video4.mp4",
            "https://your-host.com/plan7-video5.mp4",
        ],
    },
    {
        "id": 8,
        "name": "Plan 8 Demo",
        "buy_url": "https://example.com/buy8",
        "videos": [
            "https://your-host.com/plan8-video1.mp4",
            "https://your-host.com/plan8-video2.mp4",
            "https://your-host.com/plan8-video3.mp4",
            "https://your-host.com/plan8-video4.mp4",
            "https://your-host.com/plan8-video5.mp4",
        ],
    },
    {
        "id": 9,
        "name": "Plan 9 Demo",
        "buy_url": "https://example.com/buy9",
        "videos": [
            "https://your-host.com/plan9-video1.mp4",
            "https://your-host.com/plan9-video2.mp4",
            "https://your-host.com/plan9-video3.mp4",
            "https://your-host.com/plan9-video4.mp4",
            "https://your-host.com/plan9-video5.mp4",
        ],
    },
    {
        "id": 10,
        "name": "Plan 10 Demo",
        "buy_url": "https://example.com/buy10",
        "image": "https://your-host.com/plan10-image.jpg",
    },
]


# User ID -> active demo messages
active_demos = {}


# ==================================================
# BUTTON HELPER
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
    return next(
        (plan for plan in PLANS if plan["id"] == plan_id),
        None
    )


def is_placeholder(url):
    return (
        not isinstance(url, str)
        or not url.strip()
        or "your-host.com" in url
        or "example.com" in url
    )


def valid_url(url):
    return (
        isinstance(url, str)
        and url.startswith(("https://", "http://"))
        and not is_placeholder(url)
    )


# ==================================================
# DELETE CURRENT DEMO
# ==================================================

def delete_demo(user_id):
    demo = active_demos.pop(user_id, None)

    if not demo:
        return

    for message_id in reversed(demo["message_ids"]):
        try:
            bot.delete_message(
                demo["chat_id"],
                message_id
            )
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
        "Jis plan ka demo dekhna chahte ho, "
        "us plan ko select karo 👇",
        reply_markup=kb
    )


@bot.message_handler(commands=["start"])
def start(message):
    delete_demo(message.from_user.id)
    send_plan_menu(message.chat.id)


# ==================================================
# DEMO BUTTONS
# ==================================================

def demo_keyboard(plan_id):
    kb = InlineKeyboardMarkup(row_width=2)

    kb.row(
        make_button(
            "🛒 Buy Now",
            callback_data=f"buy:{plan_id}",
            style="success"
        ),
        make_button(
            "🔄 Change Plan",
            callback_data="change_plan",
            style="primary"
        )
    )

    return kb


# ==================================================
# PLAN DEMO
# ==================================================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("plan:")
)
def show_demo(call):
    bot.answer_callback_query(call.id)

    try:
        plan_id = int(call.data.split(":")[1])
    except (ValueError, IndexError):
        return

    plan = get_plan(plan_id)

    if not plan:
        return

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    delete_demo(user_id)

    message_ids = []

    # --------------------------------------------------
    # PLAN 10: IMAGE ONLY
    # --------------------------------------------------

    if plan_id == 10:
        image_url = plan.get("image", "")

        if not valid_url(image_url):
            bot.send_message(
                chat_id,
                "Plan 10 ki image URL abhi set nahi hai."
            )
            return

        try:
            sent = bot.send_photo(
                chat_id,
                photo=image_url,
                caption=(
                    "🖼️ Plan 10 Demo\n\n"
                    "Image dekh lo. Neeche apna option select karo."
                ),
                reply_markup=demo_keyboard(plan_id)
            )

            message_ids.append(sent.message_id)

        except Exception:
            log.exception("Plan 10 image send failed")
            bot.send_message(
                chat_id,
                "Image send nahi hui. Direct image URL check karo."
            )
            return

    # --------------------------------------------------
    # PLANS 1-9: VIDEO MEDIA GROUP
    # --------------------------------------------------

    else:
        videos = [
            url for url in plan.get("videos", [])
            if valid_url(url)
        ][:10]

        if not videos:
            bot.send_message(
                chat_id,
                f"{plan['name']} ke video URLs abhi set nahi hain."
            )
            return

        media = [
            InputMediaVideo(
                media=url,
                has_spoiler=True
            )
            for url in videos
        ]

        try:
            sent_messages = bot.send_media_group(
                chat_id,
                media
            )

            message_ids.extend(
                msg.message_id for msg in sent_messages
            )

            instruction = bot.send_message(
                chat_id,
                "🎬 Video dekhne ke liye video par tap karo.\n\n"
                "Demo pasand aaye toh Buy Now dabao, "
                "ya doosra plan dekhne ke liye Change Plan dabao.",
                reply_markup=demo_keyboard(plan_id)
            )

            message_ids.append(instruction.message_id)

        except Exception:
            log.exception("Video media group failed")

            for message_id in reversed(message_ids):
                try:
                    bot.delete_message(chat_id, message_id)
                except Exception:
                    pass

            bot.send_message(
                chat_id,
                "Videos send nahi hui. Direct video URLs check karo."
            )
            return

    active_demos[user_id] = {
        "chat_id": chat_id,
        "message_ids": message_ids
    }


# ==================================================
# BUY NOW
# ==================================================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("buy:")
)
def buy_now(call):
    try:
        plan_id = int(call.data.split(":")[1])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Invalid plan")
        return

    plan = get_plan(plan_id)

    if not plan:
        bot.answer_callback_query(
            call.id,
            "Plan nahi mila.",
            show_alert=True
        )
        return

    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Demo aur uske buttons delete karo.
    delete_demo(user_id)

    buy_url = plan.get("buy_url", "")

    if not valid_url(buy_url):
        bot.send_message(
            chat_id,
            "Is plan ka purchase URL abhi set nahi hai."
        )
        return

    kb = InlineKeyboardMarkup()

    kb.add(
        make_button(
            "💳 Continue to Buy",
            url=buy_url,
            style="success"
        )
    )

    bot.send_message(
        chat_id,
        f"{plan['name']} select kiya hai.\n"
        "Purchase karne ke liye neeche click karo.",
        reply_markup=kb
    )


# ==================================================
# CHANGE PLAN
# ==================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "change_plan"
)
def change_plan(call):
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Purana demo delete karo.
    delete_demo(user_id)

    send_plan_menu(chat_id)


# ==================================================
# START BOT
# ==================================================

if __name__ == "__main__":
    log.info("Demo bot starting")

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )
