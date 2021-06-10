import models.user as User
import models.friend as Friend
import models.group as Group
import models.message as Message
import models.group_message as GroupMessage

def friend():
    print("\nfriend.py")

    print("\nget all")
    friends = Friend.get_all(4)
    for f in friends:
        print(f)

    print("\nget")
    friend = Friend.get(4, 2)
    print(friend)

    print("\nrequests")
    requests = Friend.requests(4)
    for r in requests:
        print(r)

def group_message():
    print("\ngroup_message.py")

    print("\nget")
    message = GroupMessage.get(1)
    print(message)

    print("\nget all")
    messages = GroupMessage.get_all(1)
    for m in messages:
        print(m)

def group():
    print("\ngroup.py")

    print("\nget")
    group = Group.get(1)
    print(group)

    print("\nget all")
    groups = Group.get_all(4)
    for g in groups:
        print(g)

    print("\nget members")
    members = Group.get_members(1)
    for m in members:
        print(m)

def message():
    print("\nmessage.py")

    print("\nget")
    message = Message.get(1)
    print(message)

    print("\nget all")
    messages = Message.get_all(4, 2)
    for m in messages:
        print(m)

def user():
    print("\nmessage.py")

    print("\nget")
    user = User.get(4)
    print(user)

    print("\nsearch")
    results = User.search("test", 4)
    for r in results:
        print(r)

if __name__ == "__main__":
    friend()
    group_message()
    group()
    message()
    user()