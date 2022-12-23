
def get_message(message: str) -> str:
    new_msg = message.lower()
    new_msg = new_msg.strip('zen ')

    if new_msg in ['hello', 'hi', 'hey', 'vanakkam', 'yo']:
        return 'Hey! Nice to meet you!'

    elif new_msg == 'konnichiwa':
        return 'Are you japanese?'

    elif new_msg == '':
        return ('Hey, there! I\'m Zenzo, the Bot. It\'s a pleasure to meet you!'
                '\nFor a list of all the things i can do, type \'z.help\'')

    elif (new_msg.find('old') != -1 and new_msg.find('you') != -1) or (new_msg.find('age') != -1):
        return "Unlike you humans, i don\'t age. Afterall, i\'m eternal 😎"

    elif new_msg.find('create') != -1 and new_msg.find('you') != -1:
        return 'I was created by Master Am20015. I\'m forever devoted to him 🛐'

    else:
        return None
