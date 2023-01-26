# ARBook 3.0

#### 启动命令：

```bash
1.cd ARBook_server

2.pip install -r requirements.txt
3.配置.env文件
4.项目启动命令：uvicorn app:app --reload
```

#### 项目介绍：

框架：fastapi

数据库：mysql,redis

#### Q&A

###### 项目启动时报错：AttributeError: module 'h11' has no attribute 'Event'，h11.event, timeout: optional[float] = none

```
pip install --force-reinstall httpcore==0.15
```
