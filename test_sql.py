import sqlalchemy as db

engine = db.create_engine("sqlite:///test_database.sqlite")
# create a connection
conn = engine.connect()

# metadata
metadata = db.MetaData()

GroupMembers = db.Table(
    "GroupMembers",
    metadata,
    db.Column("Id", db.Integer(), primary_key=True),
    db.Column("user_id", db.Integer),
    db.Column("groupchat_id", db.Integer),
    db.Column("no_bullying", db.Integer),
)
metadata.create_all(engine)

query = db.insert(GroupMembers).values(user_id=4427, groupchat_id=125, no_bullying=1)
Result = conn.execute(query)

query = db.insert(GroupMembers).values(user_id=2, groupchat_id=12, no_bullying=1)
Result = conn.execute(query)

# read all items in the table
output = conn.execute(GroupMembers.select()).fetchall()
print(output)

# seaech for specific items
query = GroupMembers.select().where(GroupMembers.columns.user_id == 4427)
output = conn.execute(query)
print(output.fetchone())

# search for items with multiple conditions
query = GroupMembers.select().where(
    db.and_(GroupMembers.columns.user_id == 2, GroupMembers.columns.groupchat_id == 12)
)
output = conn.execute(query)
result = output.fetchone()
print(result)

# Get previous value of no_bullying
no_bullying = result.no_bullying

query = (
    GroupMembers.update()
    .where(
        db.and_(
            GroupMembers.columns.user_id == result.user_id,
            GroupMembers.columns.groupchat_id == result.groupchat_id,
        )
    )
    .values(no_bullying=no_bullying + 1)
)
conn.execute(query)

query = GroupMembers.delete().where(
    db.and_(
        GroupMembers.columns.user_id == 4427, GroupMembers.columns.groupchat_id == 125
    )
)
# Execute the delete statement
conn.execute(query)
