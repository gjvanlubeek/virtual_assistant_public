def create_list(list_of_dictionaries):
    list = []
    for dictionaries in list_of_dictionaries:
        content = f'email: {dictionaries["email"]}, sender: {dictionaries["sender"]}, subject: {dictionaries["subject"]}, date: {dictionaries["date"]}, content: {dictionaries["content"]}'
        list.append(content)
    
    return list