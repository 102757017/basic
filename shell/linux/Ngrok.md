

安装

```
!pip install pyngrok
!ngrok diagnose
from kaggle_secrets import UserSecretsClient
from pyngrok import ngrok
user_secrets = UserSecretsClient()
token=user_secrets.get_secret("ngrok_token")

# 设置 authtoken（只需一次）
ngrok.set_auth_token(token)
```





创建隧道

```
from pyngrok import ngrok

# 启动 TCP 隧道，立即返回，不阻塞
tunnel = ngrok.connect(14500, "tcp")
print("公网地址:", tunnel.public_url)
```


