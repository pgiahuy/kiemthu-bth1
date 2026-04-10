from locust import HttpUser, task, between

class MyUser(HttpUser):
    @task
    def test_weather(self):
        self.client.get("/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")