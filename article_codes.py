#import the necessary packages
from telegram import Update
from telegram.ext import  filters, CommandHandler, MessageHandler,ContextTypes,Application

TOKEN=""

#logging
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


#stsrt command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""Give a simple explanation of what the bot does"""
	await context.bot.send_message( chat_id=update.effective_chat.id, text=f"This is a cyber bullying bot, I Will help you remove users who engage in cyber-bullying on your group chats")


def is_cyberbullying(text):
	if "fool" in text:
		return True
	return False
	
#a list of dictionaries in format {"user_id": 1, "chat_id"1:,"no_bullying":0}
db=[]

#maximum number of bullying_messages
MAX_BULLYING_MESSAGES=3
NO_BANNED_DAYS=3


def add_to_db(user_id,chat_id):
	#search for the user record in the group chat 
	for i,user_record in enumerate(db):
		if (user_record["user_id"]==user_id) and (user_record["chat_id"]==chat_id):
			#if user exists, increase the number of bullying message the user has sent by 1
			user_record["no_bullying"]+=1
			db[i]=user_record
			return
	#if user doesn't exist, create a new user to the database 
	db.append({"user_id":user_id,"chat_id":chat_id,"no_bullying":1})
	return 
	
def has_hit_limit(user_id,chat_id):
	for user_record in db:
		if (user_record["user_id"]==user_id) and (user_record["chat_id"]==chat_id):
			if user_record["no_bullying"]==MAX_BULLYING_MESSAGES:
				return True
			return False
			
def reset_user_record(user_id,chat_id):
	for i,user_record in enumerate(db):
		if (user_record["user_id"]==user_id) and (user_record["chat_id"]==chat_id):
			user_record["no_bullying"]=0
			db[i]=user_record
			return

			
from datetime import datetime, timedelta
			
#cyberbullying handler
async def remove_cyberbullying(update: Update, context: ContextTypes.DEFAULT_TYPE):
   chat_id=update.effective_chat.id
   message=update.message
   sender_id=message.from_user.id
   if is_cyberbullying(message.text):
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
   		await context.bot.send_message(chat_id=update.effective_chat.id, text=f"The message you've sent is a abusive, and you've exceeding the cyberbullying limit, you'll be banned from the group chat for {NO_BANNED_DAYS} days!!",reply_to_message_id=message.message_id)
   		
   		await context.bot.ban_chat_member(chat_id=chat_id,user_id=sender_id, revoke_messages=False, until_date=unban_date)
   			
   	else:
   		#send a message that the person has sent an abusive message 
   		await context.bot.send_message(chat_id=update.effective_chat.id, text="The message you've sent is a abusive, be careful or you'll be removed from the group chat soon!",reply_to_message_id=message.message_id)

		

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    start_handler = CommandHandler("start", start, filters=~filters.ChatType.GROUPS)
    cyberbullying_handler = MessageHandler(filters.TEXT & filters.ChatType.GROUPS , remove_cyberbullying) #filters.TEXT & filters.ChatType.GROUPS tells us we want only text messages from group chats 
    application.add_handler(start_handler)
    application.add_handler(cyberbullying_handler)
    application.run_polling()