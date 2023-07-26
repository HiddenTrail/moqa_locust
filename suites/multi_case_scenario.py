from locust import events
from locust_plugins.listeners import RescheduleTaskOnFail
from locustfiles.login_and_auth import AbstractLogInApiUser
from locustfiles.users_and_posts import AbstractUsersAndPostsApiUser
from locustfiles.users_post_scenario import AbstractUsersPostScenarioUser
from common.load_test_shape import CustomLoadTestShape


class LoginAndAuthTests(AbstractLogInApiUser):
    weight = 30


class UsersAndPostsTest(AbstractUsersAndPostsApiUser):
    weight = 40


class UsersPostScenarioTest(AbstractUsersPostScenarioUser):
    weight = 30


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    RescheduleTaskOnFail(environment)
