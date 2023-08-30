from django import dispatch

# Triggered if a message gets answered.
message_answered = dispatch.Signal()

# Triggered if a new message is received.
new_message = dispatch.Signal()
