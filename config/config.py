import os

class Config:
    # API基础配置- 使用环境变量或默认值
    BASE_URL = os.getenv('API_BASE_URL', 'https://ixngeneral.ixa.digital-xian.com')
    API_VERSION = os.getenv('API_VERSION', 'v1')

    # 认证配置
    API_KEY = os.getenv('API_KEY', 'your-api-key-here')
    TOKEN = os.getenv('API_TOKEN', '')

    # 测试配置
    TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))     # 转换为整数类型
    VERIFY_SSL = os.getenv('VERIFY_SSL', 'True').lower() == 'true'      # 转换为布尔值

    # 报告配置（计算属性 - 动态生成完整的API基础URL）
    REPORT_FORMAT = os.getenv('REPORT_FORMAT', 'html')
    REPORT_PATH = os.getenv('REPORT_PATH', 'reports')

    @property
    def BASE_API_URL(self):
        return f"{self.BASE_URL}/{self.API_VERSION}"

# 创建全局配置实例
config = Config()