import pytest
import allure
from utils.api_client import api_client
from utils.assert_utils import assert_utils
from data.test_data import TestData


@allure.feature("用户管理API")
class TestUserAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.endpoint = TestData.ENDPOINTS["users"]
        self.created_user_ids = []

    def teardown_method(self):
        # 清理测试数据
        for user_id in self.created_user_ids:
            api_client.delete(TestData.ENDPOINTS["user_detail"].format(id=user_id))

    @allure.story("创建用户")
    @allure.title("测试创建有效用户")
    def test_create_valid_user(self):
        with allure.step("发送创建用户请求"):
            response = api_client.post(self.endpoint, json=TestData.VALID_USER)

        with allure.step("验证响应状态码"):
            assert_utils.assert_status_code(response, 201)

        with allure.step("验证响应数据"):
            response_data = response.json()
            assert "id" in response_data
            self.created_user_ids.append(response_data["id"])

            expected_data = {
                "username": TestData.VALID_USER["username"],
                "email": TestData.VALID_USER["email"]
            }
            assert_utils.assert_json_contains(response, expected_data)

    @allure.story("创建用户")
    @allure.title("测试创建无效用户")
    def test_create_invalid_user(self):
        with allure.step("发送创建无效用户请求"):
            response = api_client.post(self.endpoint, json=TestData.INVALID_USER)

        with allure.step("验证响应状态码为400"):
            assert_utils.assert_status_code(response, 400)

    @allure.story("获取用户")
    @allure.title("测试获取用户列表")
    def test_get_users(self):
        with allure.step("先创建一个测试用户"):
            create_response = api_client.post(self.endpoint, json=TestData.VALID_USER)
            user_id = create_response.json()["id"]
            self.created_user_ids.append(user_id)

        with allure.step("获取用户列表"):
            response = api_client.get(self.endpoint)

        with allure.step("验证响应状态码"):
            assert_utils.assert_status_code(response, 200)

        with allure.step("验证响应包含创建的用户"):
            users = response.json()
            assert any(user["id"] == user_id for user in users), "Created user not found in list"

    @allure.story("用户详情")
    @allure.title("测试获取用户详情")
    def test_get_user_detail(self):
        with allure.step("先创建一个测试用户"):
            create_response = api_client.post(self.endpoint, json=TestData.VALID_USER)
            user_id = create_response.json()["id"]
            self.created_user_ids.append(user_id)

        with allure.step("获取用户详情"):
            endpoint = TestData.ENDPOINTS["user_detail"].format(id=user_id)
            response = api_client.get(endpoint)

        with allure.step("验证响应状态码"):
            assert_utils.assert_status_code(response, 200)

        with allure.step("验证响应数据"):
            expected_data = {
                "id": user_id,
                "username": TestData.VALID_USER["username"],
                "email": TestData.VALID_USER["email"]
            }
            assert_utils.assert_json_contains(response, expected_data)