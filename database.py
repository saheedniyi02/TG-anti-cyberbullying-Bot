import sqlalchemy as db


MAX_SPAM_MESSAGES=3
#create an engine kn
engine = db.create_engine('sqlite:///database.sqlite')
#create a connection 
conn = engine.connect()

#metadata
metadata = db.MetaData()

GroupMembers = db.Table('GroupMembers', metadata,
                        db.Column('Id', db.Integer(), primary_key=True),
                        db.Column('user_id', db.Integer),
                        db.Column('groupchat_id', db.Integer),
                        db.Column('no_bullying', db.Integer),
                        )
              
metadata.create_all(engine)

MAX_SPAM_MESSAGES=3
def add_to_db(user_id,groupchat_id):
	#first check if the user_id and groupchat_id are in our database 
	search_query = GroupMembers.select().where(db.and_(GroupMembers.columns.user_id == user_id, GroupMembers.columns.groupchat_id == groupchat_id))
	output = conn.execute(search_query)
	result=output.fetchone()
	
	if result:
		#increase no_bullying value by 1
		no_bullying = result.no_bullying
		update_query = GroupMembers.update().where( db.and_(GroupMembers.columns.user_id == result.user_id, GroupMembers.columns.groupchat_id == result.groupchat_id)).values(no_bullying=no_bullying + 1)
		conn.execute(update_query)
	else:
		#add the user 
		insert_query = db.insert(GroupMembers).values(user_id=user_id, groupchat_id=groupchat_id,no_bullying=1)
		conn.execute(insert_query)
	
def has_hit_limit(user_id,groupchat_id):
	""" check if the user has hit the cyberbullying limit for that group chat """
	#search for user
	search_query = GroupMembers.select().where(db.and_(GroupMembers.columns.user_id == user_id, GroupMembers.columns.groupchat_id == groupchat_id))
	output = conn.execute(search_query)
	result=output.fetchone()
	if result:
		if result.no_bullying>=MAX_SPAM_MESSAGES:
			return True
	return False 
	
def reset_user_record(user_id,groupchat_id):
	update_query = GroupMembers.update().where( db.and_(GroupMembers.columns.user_id == user_id, GroupMembers.columns.groupchat_id == groupchat_id)).values(no_bullying=0)
	conn.execute(update_query)
	