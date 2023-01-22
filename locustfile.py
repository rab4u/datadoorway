import json
from random import randint

from locust import HttpUser, task


class HelloWorldUser(HttpUser):

    data = {
        "age": 99,
        "name": "ravi",
        "email": "rab4@engineer.com",
        "created_on": "2018-11-13T20:20:39+00:00",
        "mobile_number": "123456789"
    }

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0Ijo" \
            "xNTE2MjM5MDIyLCJleHAiOjE5MTkyNjQ0MjYsInNjb3BlcyI6ImRkOmFkbWluIHB1Ymxpc2g6d3JpdGUgbWV0cmljczpy" \
            "ZWFkIn0.mDKbgFAPQJ-TfZv55ZVp-Bg4f6_6u9mLQRE2hhLn3Z0"

    @task
    def publish_android(self):
        random_number = randint(1, 99)
        self.data['age'] = random_number
        resp = self.client.post(
            url="http://localhost:8000/publish",
            params={
                "payload_category": "android",
                "publishers": ["file", "kafka"],
                "schema_id": "users/mobile/android"
            },
            data=json.dumps(self.data),
            auth=None,
            headers={"authorization": "Bearer " + self.token},
            name="http://localhost:8000",
        )

    @task
    def publish_ios(self):
        random_number = randint(1, 99)
        self.data['age'] = random_number
        resp = self.client.post(
            url="http://localhost:8000/publish",
            params={
                "payload_category": "ios",
                "publishers": ["file"],
                "schema_id": "users/mobile/ios"
            },
            data=json.dumps(self.data),
            auth=None,
            headers={"authorization": "Bearer " + self.token},
            name="http://localhost:8000",
        )

    # @task
    # def hello_world(self):
    #     resp = self.client.get(
    #         url="http://localhost:8000/publish",
    #         data=json.dumps(self.data),
    #         auth=None,
    #         headers={"authorization": "Bearer " + self.token},
    #         name="http://localhost:8000",
    #     )
