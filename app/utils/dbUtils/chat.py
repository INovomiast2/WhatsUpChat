# Chat.py - A toolset for creating chats in database and manage them

import argparse
import os
import sys
from chatUtils import core

# Argument Parser
arguments = argparse.ArgumentParser("Chat.py", "Manage chat functions.", "Made with <3 by: INovomiast2", add_help=True)
chatCore = core()

# Arguments
arguments.add_argument("--add-contact", action="store_true")
arguments.add_argument("--remove-chat", nargs=1, type=str, metavar=('chat_id'))
arguments.add_argument("--search-chat", "-s", action="store_true")
arguments.add_argument("--filter", nargs=1, metavar=('filter_type'), choices=['user', 'id', 'less_than', 'words', 'more_than'], type=str)
arguments.add_argument("--list", "-l", action="store_true")
arguments.add_argument("--add-user", action="store_true")
arguments.add_argument("--remove-user", action="store_true")
arguments.add_argument("--send-message", action="store_true")
arguments.add_argument("-v", "--version", action="version", version='%(prog)s 2.0')

args = arguments.parse_args()

add_contact = args.add_contact
remove_chat = args.remove_chat
search = args.search_chat
fltr = args.filter
list_chats = args.list
add_user = args.add_user

if add_contact:
    chatCore.execute_add_contact()
elif remove_chat:
    pass
elif search:
    pass
elif fltr:
    pass
elif list_chats:
    pass
elif add_user:
    chatCore.execute_register_user()
elif args.remove_user:
    pass
elif args.send_message:
    chatCore.execute_create_message()
else:
    arguments.print_help()