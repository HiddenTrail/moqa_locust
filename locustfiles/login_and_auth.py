from locust import HttpUser, SequentialTaskSet, task, constant, events
from common.helpers import get_userdata_dict
from application.api_user import ApiUser
import logging


class LogInApi(SequentialTaskSet):
    def on_start(self):
        user_data = get_userdata_dict(file='userdata.json', base_url=self.client.base_url)
        self.auth_url = user_data['auth_url']
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.web_user = ApiUser(self.client, self.username, self.password)

    @task
    def auth(self):
        self.web_user.fetch_token(self.auth_url)

    @task
    def login(self):
        self.web_user.login_user(self.auth_url)


class LogInApiUser(HttpUser):
    wait_time = constant(2)
    abstract = False
    tasks = [LogInApi]


class AbstractLogInApiUser(LogInApiUser):
    abstract = True


@events.request.add_listener
def request_logger(request_type, name, response_time, response_length, response,
                       context, exception, start_time, url, **kwargs):
    logging.debug(f'REQUEST to {request_type} {url}\nResponse:\n{response.text}')
    if exception:
        logging.debug(f"FAILURE: Request to {request_type} {url} failed with exception {exception}")
