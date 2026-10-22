import logging
from telebot import TeleBot, types

# ==========================================
# 1. BOT CONFIGURATION
# ==========================================
# Paste your Telegram Bot Token directly below:
BOT_TOKEN = "8916953762:AAEg493ZtcCDx8Ux0ZXWcUVaQMnI6hgsbk4"

bot = TeleBot(BOT_TOKEN, parse_mode="HTML")

# Configure logging for debugging and error tracking
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ==========================================
# 5 & 6. CONTENT & PURCHASE URL CONFIGURATION
# ==========================================
# Leave or replace these placeholders with your actual direct public video URLs.
# Each plan from Plan 1 to Plan 9 has its own list of video URLs.
PLAN_VIDEOS = {
    "𝙈𝙊𝙈 𝘼𝙉𝘿 𝙎𝙊𝙉 😍🔥": [
        "https://videotourl.com/videos/1791609652325-1646ca32-e73f-4a5a-9874-a0f4e401c6bb.mp4",
        "https://videotourl.com/videos/1791610410648-c50ab2d2-b1b2-4998-8f5f-43a5f719b603.mp4",
        "https://videotourl.com/videos/1791609530271-d1845e11-78bd-4465-a0e3-3e0dd57fb424.mp4",
        "https://videotourl.com/videos/placeholder_1_4.mp4",
        "https://videotourl.com/videos/placeholder_1_5.mp4",
    ],
    "plan_2": [
        "https://videotourl.com/videos/placeholder_2_1.mp4",
        "https://videotourl.com/videos/placeholder_2_2.mp4",
        "https://videotourl.com/videos/placeholder_2_3.mp4",
        "https://videotourl.com/videos/placeholder_2_4.mp4",
        "https://videotourl.com/videos/placeholder_2_5.mp4",
    ],
    "plan_3": [
        "https://videotourl.com/videos/placeholder_3_1.mp4",
        "https://videotourl.com/videos/placeholder_3_2.mp4",
        "https://videotourl.com/videos/placeholder_3_3.mp4",
        "https://videotourl.com/videos/placeholder_3_4.mp4",
        "https://videotourl.com/videos/placeholder_3_5.mp4",
    ],
    "plan_4": [
        "https://videotourl.com/videos/placeholder_4_1.mp4",
        "https://videotourl.com/videos/placeholder_4_2.mp4",
        "https://videotourl.com/videos/placeholder_4_3.mp4",
        "https://videotourl.com/videos/placeholder_4_4.mp4",
        "https://videotourl.com/videos/placeholder_4_5.mp4",
    ],
    "plan_5": [
        "https://videotourl.com/videos/placeholder_5_1.mp4",
        "https://videotourl.com/videos/placeholder_5_2.mp4",
        "https://videotourl.com/videos/placeholder_5_3.mp4",
        "https://videotourl.com/videos/placeholder_5_4.mp4",
        "https://videotourl.com/videos/placeholder_5_5.mp4",
    ],
    "plan_6": [
        "https://videotourl.com/videos/placeholder_6_1.mp4",
        "https://videotourl.com/videos/placeholder_6_2.mp4",
        "https://videotourl.com/videos/placeholder_6_3.mp4",
        "https://videotourl.com/videos/placeholder_6_4.mp4",
        "https://videotourl.com/videos/placeholder_6_5.mp4",
    ],
    "plan_7": [
        "https://videotourl.com/videos/placeholder_7_1.mp4",
        "https://videotourl.com/videos/placeholder_7_2.mp4",
        "https://videotourl.com/videos/placeholder_7_3.mp4",
        "https://videotourl.com/videos/placeholder_7_4.mp4",
        "https://videotourl.com/videos/placeholder_7_5.mp4",
    ],
    "plan_8": [
        "https://videotourl.com/videos/placeholder_8_1.mp4",
        "https://videotourl.com/videos/placeholder_8_2.mp4",
        "https://videotourl.com/videos/placeholder_8_3.mp4",
        "https://videotourl.com/videos/placeholder_8_4.mp4",
        "https://videotourl.com/videos/placeholder_8_5.mp4",
    ],
    "plan_9": [
        "https://videotourl.com/videos/placeholder_9_1.mp4",
        "https://videotourl.com/videos/placeholder_9_2.mp4",
        "https://videotourl.com/videos/placeholder_9_3.mp4",
        "https://videotourl.com/videos/placeholder_9_4.mp4",
        "https://videotourl.com/videos/placeholder_9_5.mp4",
    ],
}

# 4. Plan 10 Image URL Placeholder
PLAN_10_IMAGE = "https://videotourl.com/images/placeholder_plan_10.jpg"

# 6. Configurable Purchase URLs for each plan
PLAN_PURCHASE_URLS = {
    "plan_1": "https://yourpaymentgateway.com/pay/plan1",
    "plan_2": "https://yourpaymentgateway.com/pay/plan2",
    "plan_3": "https://yourpaymentgateway.com/pay/plan3",
    "plan_4": "https://yourpaymentgateway.com/pay/plan4",
    "plan_5": "https://yourpaymentgateway.com/pay/plan5",
    "plan_6": "https://yourpaymentgateway.com/pay/plan6",
    "plan_7": "https://yourpaymentgateway.com/pay/plan7",
    "plan_8": "https://yourpaymentgateway.com/pay/plan8",
    "plan_9": "https://yourpaymentgateway.com/pay/plan9",
    "plan_10": "https://yourpaymentgateway.com/pay/plan10",
}

# ==========================================
# 8. USER STATE TRACKING
# ==========================================
# Stores list of message IDs sent during a demo session per user: {user_id: [msg_id_1, msg_id_2, ...]}
user_active_demo_messages = {}


def track_message(user_id, message_or_messages):
  """Helper to track message IDs sent to a user for cleanup."""
  if user_id not in user_active_demo_messages:
    user_active_demo_messages[user_id] = []

  if isinstance(message_or_messages, list):
    for msg in message_or_messages:
      user_active_demo_messages[user_id].append(msg.message_id)
  else:
    user_active_demo_messages[user_id].append(message_or_messages.message_id)


def clear_user_demo(chat_id, user_id):
  """Deletes tracked demo messages safely with error handling."""
  if user_id in user_active_demo_messages:
    for msg_id in user_active_demo_messages[user_id]:
      try:
        bot.delete_message(chat_id, msg_id)
      except Exception as e:
        logger.warning(
            f"Could not delete message {msg_id} for user {user_id}: {e}"
        )
    user_active_demo_messages[user_id] = []


# ==========================================
# 2. START MENU HANDLER
# ==========================================
@bot.message_handler(commands=["start"])
def send_start_menu(message):
  chat_id = message.chat.id
  user_id = message.from_user.id

  # Clear any lingering old state if applicable
  clear_user_demo(chat_id, user_id)

  # 2. Display one caption with 10 danger-style (red) buttons
  caption = "Select your plan to see the demo."

  markup = types.InlineKeyboardMarkup(row_id=2)
  for i in range(1, 11):
    # Telegram inline buttons don't have native color styling via Bot API,
    # but Danger style is conventionally represented or handled via UI clients if supported,
    # or we map callback data properly.
    button_text = f"Plan {i} Demo"
    callback_data = f"select_plan_{i}"
    markup.add(
        types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )

  bot.send_message(chat_id, caption, reply_markup=markup)


# ==========================================
# 3, 4, 9. PLAN SELECTION & MEDIA HANDLERS
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data.startswith("select_plan_"))
def handle_plan_selection(call):
  chat_id = call.message.chat.id
  user_id = call.from_user.id
  plan_num = call.data.split("_")[-1]
  plan_key = f"plan_{plan_num}"

  # Acknowledge callback query to stop loading animation
  bot.answer_callback_query(call.id)

  # Clear existing message to refresh view
  try:
    bot.delete_message(chat_id, call.message.message_id)
  except Exception as e:
    logger.warning(f"Could main start menu message be deleted: {e}")

  # Reset user state tracking list
  user_active_demo_messages[user_id] = []

  # Action for Plan 10 (Image only)
  if plan_num == "10":
    if "placeholder" in PLAN_10_IMAGE:
      logger.warning("Plan 10 image URL is still set to a placeholder.")
    
    try:
      markup = types.InlineKeyboardMarkup()
      markup.add(
          types.InlineKeyboardButton(
              "Buy Now", callback_data=f"buy_{plan_key}"
          ),
          types.InlineKeyboardButton(
              "Change Plan", callback_data="change_plan"
          ),
      )

      sent_msg = bot.send_photo(
          chat_id=chat_id,
          photo=PLAN_10_IMAGE,
          caption="Plan 10 Demo Image\n\nTap the buttons below:",
          reply_markup=markup,
      )
      track_message(user_id, sent_msg)
    except Exception as e:
      logger.error(f"Failed to send image for Plan 10: {e}")
      bot.send_message(
          chat_id,
          f"<b>Error:</b> Plan 10 image load nahi ho payi.\n<pre>{e}</pre>",
      )
    return

  # Actions for Plans 1 to 9 (Videos with spoilers)
  urls = PLAN_VIDEOS.get(plan_key, [])
  
  # Validate URLs
  for url in urls:
    if "placeholder" in url:
      logger.warning(f"URL placeholder found unreplaced in {plan_key}: {url}")

  media_group = []
  for idx, url in enumerate(urls):
    # Apply Telegram's spoiler feature to every video using caption or input media parameter
    is_first = (idx == 0)
    media_group.append(
        types.InputMediaVideo(
            media=url,
            has_spoiler=True,
            caption="Demo Video" if is_first else None,
        )
    )

  try:
    # Send media group
    sent_media = bot.send_media_group(chat_id=chat_id, media=media_group)
    track_message(user_id, sent_media)

    # Instruction message and buttons below the media group
    instruction_text = "Tap the video to watch the demo."
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Buy Now", callback_data=f"buy_{plan_key}"),
        types.InlineKeyboardButton("Change Plan", callback_data="change_plan"),
    )

    sent_instruction = bot.send_message(
        chat_id=chat_id, text=instruction_text, reply_markup=markup
    )
    track_message(user_id, sent_instruction)

  except Exception as e:
    logger.error(f"Telegram API Error while sending videos for {plan_key}: {e}")
    bot.send_message(
        chat_id,
        f"<b>Telegram API Error:</b> Videos send karne mein samasya aayi.\n<pre>{e}</pre>",
    )
    # Fallback to main menu if it fails
    send_start_menu(call.message)


# ==========================================
# 6 & 7. BUY NOW & CHANGE PLAN HANDLERS
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_buy_now(call):
  chat_id = call.message.chat.id
  user_id = call.from_user.id
  plan_key = call.data.replace("buy_", "")
  purchase_url = PLAN_PURCHASE_URLS.get(plan_key, "https://t.me/")

  bot.answer_callback_query(call.id)

  # 8. Delete currently displayed demo media and its instruction/button messages
  clear_user_demo(chat_id, user_id)

  # Display purchase message with URL button
  markup = types.InlineKeyboardMarkup()
  markup.add(types.InlineKeyboardButton("Proceed to Payment", url=purchase_url))
  markup.add(
      types.InlineKeyboardButton("Back to Menu", callback_data="change_plan")
  )

  bot.send_message(
      chat_id,
      "Aapke dwara chune gaye plan ko kharidne ke liye niche diye gaye button par click karein:",
      reply_markup=markup,
  )


@bot.callback_query_handler(func=lambda call: call.data == "change_plan")
def handle_change_plan(call):
  chat_id = call.message.chat.id
  user_id = call.from_user.id

  bot.answer_callback_query(call.id)

  # 8. Delete currently displayed demo media and its instruction/button messages
  clear_user_demo(chat_id, user_id)
  
  # Also remove the current trigger message if it exists
  try:
    bot.delete_message(chat_id, call.message.message_id)
  except Exception:
    pass

  # Show original menu containing all 10 plan buttons
  caption = "Select your plan to see the demo."
  markup = types.InlineKeyboardMarkup(row_width=2)
  for i in range(1, 11):
    markup.add(
        types.InlineKeyboardButton(
            text=f"Plan {i} Demo", callback_data=f"select_plan_{i}"
        )
    )

  bot.send_message(chat_id, caption, reply_markup=markup)


# ==========================================
# MAIN ENTRY POINT
# ==========================================
if __name__ == "__main__":
    logger.info("Bot is starting up...")
    bot.remove_webhook()  # Telegram ke purane webhook ko remove karne ke liye
    bot.infinity_polling(skip_pending=True)
