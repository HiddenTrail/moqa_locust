from locust import LoadTestShape


class CustomLoadTestShape(LoadTestShape):
    stages = [
        {"duration": 10, "users": 1, "spawn_rate": 1},
        {"duration": 30, "users": 5, "spawn_rate": 2},
        {"duration": 60, "users": 10, "spawn_rate": 3}
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None
