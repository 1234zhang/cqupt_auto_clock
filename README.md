克隆了之后使用下面的方法创建python 虚拟环境：
```
# 首先安装virtualvenv
pip3 install virtualenv
# 创建venv文件
virtualenv venv
# 进入venv虚拟环境
source venv/bin/activate
```

进入虚拟环境之后，使用下面的方式安装相关依赖
```
pip3 install -r requirements.txt
```

完成上面之后，整体运行环境就安装完成。

之后在/src/contant.py文件中安装文件格式将相关信息填写完成。
其中[server酱推送](http://sc.ftqq.com/3.version) 进行微信的推送。