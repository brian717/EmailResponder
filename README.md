# EmailResponder
Auto-responder for gmail. Polls for new messages with a given string in the subject and replies with a given message.

Usage: python emailResponder.py responder_config.json

The config file is in json and should be self-explanatory (field values are named in a way that should explain what they are). 

This polls a given gmail account every 10 seconds for new emails with a subject containing the search string specified in the config file. 

It responds from the given fromEmail with the given message.
It ignores responses to threads, as well as subsequent emails frmo a user who it already responded to. 
(This is done to avoid the same person getting the same exact message on subsequent emails, which would be suspicious)
