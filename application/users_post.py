import random
import logging


def get_random_user_id(user_list):
    user = random.choice(user_list)
    logging.debug(f'Random user: {user}')
    return user['id']

def get_random_post_id_for_user(user_id, posts_list):
    users_posts_list = []
    for post in posts_list:
        if post['userId'] == user_id:
            users_posts_list.append(post)
    post = random.choice(users_posts_list)
    logging.debug(f'Random post: {post}')
    return post['id']
