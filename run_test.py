import os
import sys
import pytest
import argparse
from datetime import datetime
from config.config import config


def run_tests():
    # 创建报告目录
    if not os.path.exists(config.REPORT_PATH):
        os.makedirs(config.REPORT_PATH)

    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 配置pytest参数
    pytest_args = [
        "-v",
        "--tb=short",
        f"--html={config.REPORT_PATH}/report_{timestamp}.html",
        "--self-contained-html",
        "--alluredir", f"{config.REPORT_PATH}/allure_{timestamp}"
    ]

    # 添加自定义标记过滤
    parser = argparse.ArgumentParser(description='Run API tests')
    parser.add_argument('--mark', type=str, help='Run tests with specific marker')
    args = parser.parse_args()

    if args.mark:
        pytest_args.extend(["-m", args.mark])

    # 添加测试目录
    pytest_args.append("test_cases/")

    # 运行测试
    exit_code = pytest.main(pytest_args)

    # 生成Allure报告
    if os.path.exists(f"{config.REPORT_PATH}/allure_{timestamp}"):
        os.system(
            f"allure generate {config.REPORT_PATH}/allure_{timestamp} -o {config.REPORT_PATH}/allure_report_{timestamp} --clean")

    sys.exit(exit_code)


if __name__ == "__main__":
    run_tests()