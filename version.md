# v1.0
- 数据库orm模块建立完成

# v2.0
- 数据库可支持使用`config.txt`进行配置
- 新增了数据库初始化的演示文件`sample.py`
- 新增了`logger`模块
- 链接了`spider`爬虫模块
- 在`database.utils`中增加了一些常用的函数并添加了生成随机数据的函数

# v3.0
- 修复了季节生成不完全的bug
- 修复了日志文件夹不存在的bug
- 修复了日志debug重复输出的bug

# v4.0
- 新增了`database.api`模块，用于操作数据库，获取DataFrame
- 修改了数据库结构
  - 在Supplier表中增加了`region`字段
  
# v5.0
- 新增了`fake-data-config.txt`文件，用于配置生成假数据的参数

# v6.0
- 更新数据库生成逻辑，让年龄和性别有关联，并且符合正态分布