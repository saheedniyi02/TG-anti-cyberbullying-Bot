import logging
import pickle
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import filters, MessageHandler,CommandHandler, ContextTypes,Application
from model import clean_text
from database import add_to_db, has_hit_limit, reset_user_record,MAX_SPAM_MESSAGES
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


#maximum number of spam_messages
MAX_SPAM_MESSAGES=3
NO_BANNED_DAYS=1
model_path="assets/model.pickle" 
vectorizer_path="assets/vectorizer.pickle"
	
def is_spam(text):
	vectorizer = pickle.load(open(vectorizer_path,'rb'))
	model = pickle.load(open(model_path,'rb'))
	text=clean_text(text)
	prediction=model.predict(vectorizer.transform([text]))[0]
	if prediction==1:
		return True
	return False
	
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""Give a simple explanation of what the bot does"""
	await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"This is a cyber bullying bot, I Will help you remove users who engage in cyber-bullying on your group chats\nHow to use?\n\nAdd me as an admin to your group chat and give me permission to remove users, send and delete messages.  \nUsers are given {MAX_SPAM_MESSAGES} opportunities, if a user has sent up to {MAX_SPAM_MESSAGES} messages he will be removed and banned for {NO_BANNED_DAYS} days!"
    )
	

async def remove_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
   chat_id=update.effective_chat.id
   message=update.message
   sender_id=message.from_user.id
   if is_spam(message.text):
   	add_to_db(sender_id,chat_id)
   	
   	#if user has hit limit
   	if has_hit_limit(sender_id,chat_id):
   		#current date
   		current_date=datetime.now()
   		ban_duration=timedelta(days=NO_BANNED_DAYS)
   		unban_date=current_date+ban_duration
   		
   		#reset record
   		reset_user_record(sender_id,chat_id)
   		
   		#remove user 
   		await context.bot.send_message(chat_id=update.effective_chat.id, text=f"The message you've sent is a spam, and you've exceeded the spam limit, you'll be banned from the group chat for {NO_BANNED_DAYS} days!!",reply_to_message_id=message.message_id)
   		
   		await context.bot.ban_chat_member(chat_id=chat_id,user_id=sender_id, revoke_messages=True, until_date=unban_date)
   	
   	else:
   		#send a message that the person has sent a spam message 
   		await context.bot.send_message(chat_id=update.effective_chat.id, text="The message you've sent is a spam, be careful or you'll be removed from the group chat soon!",reply_to_message_id=message.message_id)



if __name__ == "__main__":
    application = Application.builder().token("TOKEN").build()
    
    start_handler = CommandHandler("start", start, filters=~filters.ChatType.GROUPS)
    spam_handler = MessageHandler(filters.TEXT & filters.ChatType.GROUPS , remove_spam)
    application.add_handler(start_handler)
    application.add_handler(spam_handler)
    application.run_polling()