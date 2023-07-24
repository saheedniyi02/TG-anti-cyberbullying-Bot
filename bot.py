import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import  filters, MessageHandler,ContextTypes,Application

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

#name: no of spam messages 
db=[]

#maximum number of spam_messages
MAX_SPAM_MESSAGES=3
NO_BANNED_DAYS=1

def add_to_db(user_id,chat_id):
	for i,user_record in enumerate(db):
		if (user_record["user_id"]==user_id) and (user_record["chat_id"]==chat_id):
			user_record["no_spam_messages"]+=1
			db[i]=user_record
			return
	db.append({"user_id":user_id,"chat_id":chat_id,"no_spam_messages":1})
	return 
	
def has_hit_limit(user_id,chat_id):
	for user_record in db:
		if (user_record["user_id"]==user_id) and (user_record["chat_id"]==chat_id):
			if user_record["no_spam_messages"]==MAX_SPAM_MESSAGES:
				return True
			return False
			
def reset_user_record(user_id,chat_id):
	for i,user_record in enumerate(db):
		if (user_record["user_id"]==user_id) and (user_record["chat_id"]==chat_id):
			user_record["no_spam_messages"]=0
			db[i]=user_record
			return
	
	
def is_spam(text):
	if "crazy" in text:
		return True
	return False

async def remove_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
   print(db)
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
   		await context.bot.send_message(chat_id=update.effective_chat.id, text=f"The message you've sent is a spam, and you've exceeding the spam limit, you'll be banned from the group chat for {NO_BANNED_DAYS} days!!",reply_to_message_id=message.message_id)
   		
   		await context.bot.ban_chat_member(chat_id=chat_id,user_id=sender_id, revoke_messages=False, until_date=unban_date)
   		reset_user_record(sender_id,chat_id)
   		
   		
   	
   	else:
   		#send a message that the person has sent a spam message 
   		await context.bot.send_message(chat_id=update.effective_chat.id, text="The message you've sent is a spam, be careful or you'll be removed from the group chat soon!",reply_to_message_id=message.message_id)



if __name__ == "__main__":
    application = Application.builder().token("TOKEN").build()
    spam_handler = MessageHandler(filters.TEXT & filters.ChatType.GROUPS , remove_spam)
    application.add_handler(spam_handler)
    application.run_polling()