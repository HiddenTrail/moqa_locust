from locust import HttpUser, TaskSet, task, constant, events
from common.helpers import get_userdata_dict
from application.api_user import ApiUser
from application.users_post import get_random_user_id
from application.users_post import get_random_post_id_for_user
import gevent
import logging


class UsersPostScenario(TaskSet):
    def on_start(self):
        user_data = get_userdata_dict(file='userdata.json', base_url=self.client.base_url)
        self.auth_url = user_data['auth_url']
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.web_user = ApiUser(self.client, self.username, self.password, self.auth_url)

    @task
    def users_post(self):
        gevent.sleep(2)
        user_list = self.web_user.users_api()
        user_id = get_random_user_id(user_list)
        gevent.sleep(1)
        posts_list = self.web_user.posts_api()
        post_id = get_random_post_id_for_user(user_id, posts_list)
        gevent.sleep(1)
        self.web_user.post_from_user_api(user_id, post_id)


class UsersPostScenarioUser(HttpUser):
    wait_time = constant(2)
    abstract = False
    tasks = [UsersPostScenario]


class AbstractUsersPostScenarioUser(UsersPostScenarioUser):
    abstract = True


@events.request.add_listener
def request_logger(request_type, name, response_time, response_length, response,
                       context, exception, start_time, url, **kwargs):
    logging.debug(f'REQUEST to {request_type} {url}\nResponse:\n{response.text}')
    if exception:
        logging.debug(f"FAILURE: Request to {request_type} {url} failed with exception {exception}")
