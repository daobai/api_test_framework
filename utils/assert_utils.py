import json
from typing import Dict, Any, List


class AssertUtils:
    @staticmethod
    def assert_status_code(response, expected_code: int):
        """验证状态码"""
        actual_code = response.status_code
        assert actual_code == expected_code, (
            f"Expected status code {expected_code}, but got {actual_code}. "
            f"Response: {response.text}"
        )

    @staticmethod
    def assert_response_time(response, max_time: float):
        """验证响应时间"""
        response_time = response.elapsed.total_seconds()
        assert response_time <= max_time, (
            f"Response time {response_time}s exceeded maximum allowed time {max_time}s"
        )

    @staticmethod
    def assert_json_contains(response, expected_data: Dict[str, Any]):
        """验证JSON响应包含特定字段和值"""
        response_json = response.json()
        for key, expected_value in expected_data.items():
            assert key in response_json, f"Key '{key}' not found in response"
            actual_value = response_json[key]
            assert actual_value == expected_value, (
                f"Value mismatch for key '{key}': expected {expected_value}, got {actual_value}"
            )

    @staticmethod
    def assert_json_schema(response, schema: Dict[str, Any]):
        """验证JSON响应符合指定模式（简单实现）"""
        # 这里可以集成jsonschema库进行更复杂的验证
        response_json = response.json()

        def _validate(data, schema):
            if isinstance(schema, dict):
                for key, value_type in schema.items():
                    assert key in data, f"Missing key: {key}"
                    _validate(data[key], value_type)
            elif isinstance(schema, list) and schema:
                for item in data:
                    _validate(item, schema[0])
            else:
                assert isinstance(data, schema), f"Expected type {schema}, got {type(data)}"

        _validate(response_json, schema)

    @staticmethod
    def assert_response_contains(response, expected_text: str):
        """验证响应包含特定文本"""
        assert expected_text in response.text, (
            f"Expected text '{expected_text}' not found in response"
        )


# 创建便捷的断言实例
assert_utils = AssertUtils()