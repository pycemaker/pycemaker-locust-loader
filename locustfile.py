import math
from locust import HttpUser, TaskSet, task, constant, between
from locust import LoadTestShape
import random


class UserTasks(TaskSet):

    def on_start(self):
        response = self.client.post("/registrar", json={
            "name": "Roberto Campos",
            "email": "robertocampos@email.com",
            "password": "1234",
            "cellphoneNumber": "12999998888"
        })
        response = response.json()
        self.client.delete("/usuario/delete/%s" % response["id"])

    @task
    def usuarios(self):
        self.client.get("/usuarios")


class WebsiteUser(HttpUser):
    host = "http://pcm.centralus.cloudapp.azure.com:8080"
    wait_time = constant(0.5)
    tasks = [UserTasks]


class StepLoadShape(LoadTestShape):

    stages = [
        {"duration": 300, "users": 10, "spawn_rate": 1},
        {"duration": 600, "users": 50, "spawn_rate": 1},
        {"duration": 900, "users": 100, "spawn_rate": 1},
        {"duration": 1200, "users": 200, "spawn_rate": 1},
        {"duration": 1500, "users": 400, "spawn_rate": 1},
        {"duration": 1800, "users": 800, "spawn_rate": 1},
        {"duration": 2100, "users": 1000, "spawn_rate": 1},
        {"duration": 2400, "users": 800, "spawn_rate": 1},
        {"duration": 2700, "users": 400, "spawn_rate": 1},
        {"duration": 3000, "users": 200, "spawn_rate": 1},
        {"duration": 3300, "users": 100, "spawn_rate": 1},
        {"duration": 3600, "users": 10, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        if run_time > 3600:
            self.reset_time()
            return (10, 10)

    # step_time = 60
    # step_load = 6
    # spawn_rate = 10
    # time_limit = 600

    # def tick(self):
    #     run_time = self.get_run_time()

    #     if run_time > self.time_limit:
    #         # self.time_limit = 240
    #         self.reset_time()
    #         return (6, 6)

    #     current_step = math.floor(run_time / self.step_time) + 1
    #     return (current_step * self.step_load, self.spawn_rate)

    # step_time = 30
    # step_load = 10
    # spawn_rate = 10
    # time_limit = 120
    # other_limit = 121

    # def tick(self):
    #     run_time = self.get_run_time()
    #     users = self.get_current_user_count()

    #     if users == 120:
    #         self.time_limit = 119
    #         self.other_limit = 120
    #         return (1, 1)

    #     if run_time > self.other_limit:
    #         current_time_limit = self.other_limit
    #         self.other_limit = current_time_limit + 1
    #         self.time_limit = current_time_limit - 1
    #         print(self.time_limit)
    #         self.reset_time()
    #         return (1, 1)

    #     if run_time > self.time_limit:
    #         current_time_limit = self.time_limit
    #         self.time_limit = current_time_limit + 1
    #         print(self.time_limit)
    #         self.reset_time()
    #         return (1, 1)

    #     current_step = math.floor(run_time / self.step_time) + 1
    #     return (current_step * self.step_load, self.spawn_rate)

    # step_time = 30
    # step_load = 10
    # spawn_rate = 10
    # time_limit = 120

    # def tick(self):
    #     run_time = self.get_run_time()

    #     if run_time > self.time_limit:
    #         current_time_limit = self.time_limit
    #         self.time_limit = current_time_limit + 30
    #         print(self.time_limit)
    #         self.reset_time()
    #         return (1,1)

    #     current_step = math.floor(run_time / self.step_time) + 1
    #     return (current_step * self.step_load, self.spawn_rate)
