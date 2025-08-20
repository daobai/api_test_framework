class TestData:
    # 用户相关测试数据
    VALID_USER = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test@123456"
    }

    INVALID_USER = {
        "username": "ab",  # 太短
        "email": "invalid-email",
        "password": "weak"
    }

    # 产品相关测试数据
    VALID_PRODUCT = {
        "name": "Test Product",
        "price": 99.99,
        "description": "This is a test product",
        "category": "electronics"
    }

    # API端点
    ENDPOINTS = {
        "users": "/users",
        "user_detail": "/users/{id}",
        "products": "/products",
        "product_detail": "/products/{id}"
    }