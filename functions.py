# get user's name
import slack

def get_user_name(client, user_id):
    response = client.users_info(user=user_id)
    return response['user']['name'].capitalize()
