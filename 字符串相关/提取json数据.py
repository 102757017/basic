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




print("========= glom 模块用法演示 (真正最终兼容版) =========\n")

# --- 1-6 部分代码无需修改，它们已经可以正常工作 ---

print("--- 1. 基础用法：访问嵌套数据 ---")
username = glom(api_response, 'data.user.name')
print(f"使用data.user.name获取用户名: {username}\n")


print("--- 2. 访问列表元素 ---")
first_product_name = glom(api_response, 'data.products.0.name')
print(f"使用data.products.0.name获取第一个商品的名字: {first_product_name}\n")


print("--- 3. 处理缺失数据和设置默认值 ---")
spec_age_safe = T['data']['user'].get('age')
user_age = glom(api_response, spec_age_safe)
print(f"使用兼容性 spec '{spec_age_safe}' 获取不存在的用户年龄: {user_age}")

spec_age_default_safe = T['data']['user'].get('age', 18)
user_age_with_default = glom(api_response, spec_age_default_safe)
print(f"使用兼容性 spec '{spec_age_default_safe}' 获取年龄: {user_age_with_default}\n")


print("--- 4. 数据转换：在规范中调用函数 ---")
spec_lower_status = ('status', str.lower)
status_lower = glom(api_response, spec_lower_status)
print(f"使用 ('status', <built-in method lower of str object at ...>) 获取状态并转为小写: {status_lower}\n")


print("--- 5. 列表操作 ---")
spec_all_names = ('data.products', ['name'])
product_names = glom(api_response, spec_all_names)
print(f"使用 {spec_all_names} 获取所有商品的名字: {product_names}")


#Coalesce 的主要作用是：提供一种优雅的方式来处理可能缺失的数据路径，允许你指定多个备选路径，glom 会按顺序尝试这些路径，返回第一个成功获取的值。
spec_all_prices = ('data.products', [Coalesce('price', default=0.0)])
product_prices = glom(api_response, spec_all_prices)
print(f"使用 {spec_all_prices} 获取所有价格 (缺失的用0.0代替): {product_prices}\n")



print("--- 6. 数据重组：创建全新的数据结构 ---")
summary_spec = {
    'user_email': 'data.user.profile.email',
    'active_user': 'data.user.profile.is_active',
    'product_count': ('data.products', len),
    'total_value': ('data.products', [Coalesce('price', default=0)], Sum())
}
summary = glom(api_response, summary_spec)
print("使用字典作为 spec 来重组数据，生成的摘要信息:")
pprint.pprint(summary)
print("")

# --- 7. 处理对象属性---
print("--- 7. 处理对象属性 ---")
User = namedtuple('User', ['name', 'city'])
user_obj = User(name='Bob', city='New York')
# 对于对象属性访问，必须显式使用 T.attribute 的形式
spec_obj_name = T.name
obj_name = glom(user_obj, spec_obj_name)
print(f"从对象 {user_obj} 中使用 spec '{spec_obj_name}' 获取名字: {obj_name}\n")


