from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from time import sleep
import random
import traceback
import time
import sys

api_id = 123456
api_hash = ''
phone_details =''
client = TelegramClient('session_name', api_id, api_hash)
try:
  client.start()
  me = client.get_me()
  last_date = None
  chunk_size = 200
  groups=[]
  result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
  groups.extend(result.chats)
  #chooseing group to scrape member
  print("Choose a group to scrape members from:")
  for i in range(0,len(groups)):
    print(str(i) + ' - ' + groups[i].title)
  g_index = input("Enter a Number: ")
  if int(g_index) < 0 or int(g_index) > len(groups)-1:
    print("Wrong input please enter valid group number")
  else:
    target_group=groups[int(g_index)]
    #fetching members 
    print('Fetching Members...')
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=False)
    #printing members name from group
    print("Users with their usernames, names and ids ")
    for user in all_participants:
      if user.username:
          username= user.username
      else:
          username= "None"
      print("User Name: " ,username)
      print("User Id: ",user.id)
      if user.first_name:
          first_name= user.first_name
      else:
          first_name= ""
      if user.last_name:
          last_name= user.last_name
      else:
        last_name= ""
      name= (first_name + ' ' + last_name).strip()
      print("Name: ",name)
      print(" ")

    print(len(all_participants))
    #adding members to other private group 
    print("Choose group in which you want to add members")
    for i in range(0,len(groups)):
      print(str(i) + ' - ' + groups[i].title)
    group_index = input("Enter a Number: ")
    if int(group_index) < 0 or int(group_index) > len(groups)-1:
      print("Wrong input please enter valid group number")
    else:
      add_member_group=groups[int(group_index)]
      print(add_member_group)
      n = 0
      for user in all_participants:
        n += 1
        if n % 50 == 0:
          sleep(900)
        try:
          print ("Adding {}".format(user.id))
          print()
          user_to_add = InputPeerUser(user.id, user.access_hash)
          #for channels
          #target_group_entity = InputPeerChannel(add_member_group.id,add_member_group.access_hash)
          #client(InviteToChannelRequest(target_group_entity,[user_to_add]))

          #for group
          client(AddChatUserRequest(add_member_group.id,user_to_add,fwd_limit=10))
          print("Waiting for 30-35 Seconds...")
          time.sleep(random.randrange(30, 35))
        except PeerFloodError:
          print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
          print("The user's privacy settings do not allow you to do this. Skipping.")
        except:
          #traceback.print_exc()
          #print("Unexpected Error")
          pass
except Exception as e:
  print(e)
  print("Error in connecting")
finally:
  client.disconnect()