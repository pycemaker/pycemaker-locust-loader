import math
from locust import HttpUser, TaskSet, task, constant, between
from locust import LoadTestShape
import random


class UserTasks(TaskSet):

    @task
    def registrar(self):
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
    host = "http://pycemaker.herokuapp.com"
    wait_time = constant(0.5)
    tasks = [UserTasks]


class StepLoadShape(LoadTestShape):
    """
    A step load shape
    Keyword arguments:
        step_time -- Time between steps
        step_load -- User increase amount at each step
        spawn_rate -- Users to stop/start per second at every step
        time_limit -- Time limit in seconds
    """

    step_time = 60
    step_load = 6
    spawn_rate = 10
    time_limit = 600

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            # self.time_limit = 240
            self.reset_time()
            return (6, 6)

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)

    # """
    # A step load shape
    # Keyword arguments:
    #     step_time -- Time between steps
    #     step_load -- User increase amount at each step
    #     spawn_rate -- Users to stop/start per second at every step
    #     time_limit -- Time limit in seconds
    # """

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


# class StepLoadShape(LoadTestShape):
#     """
#     A step load shape
#     Keyword arguments:
#         step_time -- Time between steps
#         step_load -- User increase amount at each step
#         spawn_rate -- Users to stop/start per second at every step
#         time_limit -- Time limit in seconds
#     """

#     step_time = 30
#     step_load = 10
#     spawn_rate = 10
#     time_limit = 120

#     def tick(self):
#         run_time = self.get_run_time()

#         if run_time > self.time_limit:
#             current_time_limit = self.time_limit
#             self.time_limit = current_time_limit + 30
#             print(self.time_limit)
#             self.reset_time()
#             return (1,1)

#         current_step = math.floor(run_time / self.step_time) + 1
#         return (current_step * self.step_load, self.spawn_rate)
