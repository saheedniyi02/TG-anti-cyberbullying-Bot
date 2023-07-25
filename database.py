import sqlalchemy as db

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
                        db.Column('no_spam', db.Integer),
                        )
              
metadata.create_all(engine)

#Add  a single item
query = db.insert(GroupMembers).values(user_id=4427, groupchat_id=125,no_spam=1)
Result = conn.execute(query)

#Add to a single row
query = db.insert(GroupMembers).values(user_id=2, groupchat_id=12,no_spam=1)
Result = conn.execute(query)

#get all items in our db
output = conn.execute(GroupMembers.select()).fetchall()
print(output)

#seaech for specific items 
query = GroupMembers.select().where(GroupMembers.columns.user_id==4427)
output = conn.execute(query)
print(output.fetchone())

query = GroupMembers.select().where(db.and_(GroupMembers.columns.user_id == 2, GroupMembers.columns.groupchat_id == 12))
output = conn.execute(query)
print("hi")
result=output.fetchone()
print(result)

# Update item
# Get previous value
print(f"{result}: RESULT")
no_spam = result.no_spam
print(no_spam)

query = GroupMembers.update().where(
    db.and_(GroupMembers.columns.user_id == result.user_id, GroupMembers.columns.groupchat_id == result.groupchat_id)
).values(no_spam=no_spam + 1)

# Execute the update statement
conn.execute(query)

# Delete
query = GroupMembers.delete().where(
    db.and_(GroupMembers.columns.user_id == 4427, GroupMembers.columns.groupchat_id == 125)
)

# Execute the delete statement
conn.execute(query)

#get all items in our db
output = conn.execute(GroupMembers.select()).fetchall()
print(output)

