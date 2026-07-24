import pprint
from collections import namedtuple
# 导入 T (Target) 以构建更灵活的 spec
from glom import glom, Coalesce, Sum, T

# --- 准备工作: 定义贯穿整个演示的示例数据 ---
api_response = {
    'transaction_id': 'txn_12345abc',
    'status': 'SUCCESS',
    'data': {
        'user': {
            'id': 101,
            'name': 'Alice',
            'profile': {
                'email': 'alice@example.com',
                'is_active': True
            }
        },
        'products': [
            {'id': 'p001', 'name': 'Laptop', 'price': 1200},
            {'id': 'p002', 'name': 'Mouse', 'price': 25},
            {'id': 'p003', 'name': 'Keyboard'},
        ],
        'metadata': None
    }
}





username = glom(api_response, 'data.user.name')
