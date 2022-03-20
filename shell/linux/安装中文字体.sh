#安装字体管理器
!apt install -y fontconfig mkfontscale
#下载simsun.ttc
!wget -c https://files.cnblogs.com/files/xiaochina/simsun.zip
# 解压simsun.zip
!unzip simsun.zip
#将simsun.ttc复制到指定目录
!cp simsun.ttc  /usr/share/fonts/
#字体扩展
!mkfontscale
#新增字体目录      
!mkfontdir   
#刷新缓存        
!fc-cache -fv 
#查看字体   
!fc-list :lang=zh