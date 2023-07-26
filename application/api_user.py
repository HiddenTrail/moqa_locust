from locust.clients import HttpSession

class ApiUser:
    def __init__(self, session: HttpSession, username, password, auth_url=None):
        self.session = session
        self.username = username
        self.password = password
        if auth_url:
            self.fetch_token(auth_url)
            self.login_user(auth_url)

    def fetch_token(self, auth_url):
        response = self.session.get(f'{auth_url}/samuli-paasimaa-ht/fake_auth/token')
        json_response = response.json()
        try:
            self.access_token = json_response['access_token']
        except KeyError:
            raise AssertionError('access_token not present in the response')
        try:
            self.token_type = json_response['token_type']
        except KeyError:
            raise AssertionError('token_type not present in the response')
        self.session.headers['Authorization'] = f'{self.token_type} {self.access_token}'

    def login_user(self, auth_url):
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.session.post(f'{auth_url}/samuli-paasimaa-ht/fake_auth/login', json=payload)
        json_response = response.json()
        assert 'username' and 'password' in json_response, 'username and/or password not present in the response'

    def users_api(self):
        response = self.session.get('/users')
        json_response = response.json()
        self._assert_response_list(json_response)
        return json_response

    def posts_api(self):
        response = self.session.get('/posts')
        json_response = response.json()
        self._assert_response_list(json_response)
        return json_response

    def post_from_user_api(self, user_id, post_id):
        response = self.session.get(f'/users/{user_id}/posts?id={post_id}', name="/users/user_id/posts?id=post_id")
        json_response = response.json()
        self._assert_response_list(json_response)
        return json_response


    def _assert_response_list(self, json_response):
        for item in json_response:
            try:
                assert 'id' in item
            except AssertionError:
                assert False, 'id not present in the response'
