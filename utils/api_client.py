import requests
import json
import logging
from typing import Dict, Any, Optional
from config.config import config

'''
#配置logging基本设置#参数：作用#
%(levelno)s：打印日志级别的数值
%(levelname)s：打印日志级别的名称
%(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s：打印当前执行程序名
%(funcName)s：打印日志的当前函数
%(lineno)d：打印日志的当前行号
%(asctime)s：打印日志的时间
%(thread)d：打印线程ID
%(threadName)s：打印线程名称
%(process)d：打印进程ID
%(message)s：打印日志信息
'''
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = config.BASE_API_URL
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.TOKEN}',
            'X-API-Key': config.API_KEY
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # 设置默认参数
        kwargs.setdefault('timeout', config.TIMEOUT)
        kwargs.setdefault('verify', config.VERIFY_SSL)

        # 合并headers
        headers = kwargs.pop('headers', {})
        merged_headers = {**self.headers, **headers}

        logger.info(f"Making {method.upper()} request to {url}")
        if kwargs.get('json'):
            logger.debug(f"Request payload: {kwargs['json']}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=merged_headers,
                **kwargs
            )

            logger.info(f"Response status: {response.status_code}")
            if response.content:
                logger.debug(f"Response content: {response.text[:500]}...")  # 限制日志长度

            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request('GET', endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request('POST', endpoint, json=json, **kwargs)

    def put(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request('PUT', endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request('DELETE', endpoint, **kwargs)

    def patch(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request('PATCH', endpoint, json=json, **kwargs)


# 全局客户端实例
api_client = APIClient()