<h1 align="center">ICPCOL</h1>
<p align="center">
    工信部域名备案查询工具，用于渗透过程中收集目标备案域名，可用于确认资产归属或收集企业备案资产
</p>
<p align="center">
    <img src="https://badgen.net/badge/language/python"> 
    <img src="https://badgen.net/github/stars/Ryan0x01/ICPCol">
    <img src="https://badgen.net/github/forks/Ryan0x01/ICPCol">
	<img src="https://badgen.net/github/issues/Ryan0x01/ICPCol">
    <a href="https://angesec.com"><img src="https://img.shields.io/badge/blog-@%20%E6%9A%97%E6%A0%BC%E5%AE%89%E5%85%A8-blue.svg?style=social"></a>
</p>



<br>

## 介绍

> **责任说明：请勿将程序用于恶意数据窃取，使用程序所造成的影响作者概不负责！**

获取网站备案是信息收集中不可或缺的一环，目前最权威的备案查询网站是工信部备案查询系统，由于在工信部网站查询每次查询都需要手动输入验证码，查询效率低下，因此编写了 ICPCol 用于自动化备案查询

ICPCol 支持进行单一目标备案查询和批量查询，查询目标可以是**IP地址、域名、备案号、公司名**，在信息收集过程中可以利用脚本对收集的企业控股公司名进行批量备案查询

如果程序运行出现问题或有其他程序优化方案，欢迎在`Issue`中指出

如果本项目有帮助到你，可以点个`Star`支持作者

<br>


## 环境要求

在使用之前需要使用 pip 安装依赖库文件

```python
pip install -r requirements.txt
```

直接运行 python 脚本或使用 `-h` 参数可以查看参数列表

```
C:\>python ICPCol.py
usage: python ICPCol.py [-t TARGET] [-f FILE] [-o [FILENAME]] [-s [SIMPLE_FILE]] [-p PROXY] [-tp] [-h]

   __     ______     ______   ______     ______     __
  /\ \   /\  ___\   /\  == \ /\  ___\   /\  __ \   /\ \
  \ \ \  \ \ \____  \ \  _-/ \ \ \____  \ \ \/\ \  \ \ \____
   \ \_\  \ \_____\  \ \_\    \ \_____\  \ \_____\  \ \_____\
    \/_/   \/_____/   \/_/     \/_____/   \/_____/   \/_____/

                        Version：v2.0.0      Author：OssianSong

input:
  -t TARGET           输入公司名/备案号/域名/IP地址 询对应备案信息
  -f FILE             从指定txt文件中读取数据进行批量查询

output:
  -o [FILENAME]       指定文件名将数据保存到Excel中,参数为空时使用默认文件名
  -s [SIMPLE_FILE]    生成FOFA查询语法并保存到txt中,参数为空时使用默认文件名

options:
  -p PROXY            使用代理查询,指定使用的代理地址,格式：[Protocol://IP:Port]
  -tp, --third-party  使用非官方备案网站进行查询,不保证结果精确性
  -h, --help          查看程序使用帮助
```

<br>

## 快速使用

### 单一查询

通过 `-t` 参数指定查询目标，查询目标可以输入**域名**、**IP**、**公司名**和**备案号**

```
python ICPCol.py -t baidu.com
```

### 批量查询

通过 `-f` 参数指定 txt 文件，可以对文件内目标进行批量查询。需要注意的是，如果查询数据较大，IP会被工信部网站封禁

```
python ICPCol.py -f targets.txt
```

脚本运行结果如下，输入域名查询可以确认资产归属于哪个公司，输入公司名查询可以收集该公司所有备案资产

```
D:\02-Program\05-Project\Python\ICPCol>python ICPCol.py -t baidu.com
[√] 获取 cookie 成功
[√] 获取 token 成功
[√] 计算验证码滑块缺口位置成功
[√] 自动破解滑块验证码成功
查询对象：baidu.com 共有 1 个已备案域名
正在查询第1页...
+--------------------------+-------------------+-----------+----------+--------+----------+------------+
|        域名主办方        |     网站备案号    |    域名   | 域名类型 | 审批项 | 限制接入 |  备案日期  |
+--------------------------+-------------------+-----------+----------+--------+----------+------------+
| 北京百度网讯科技有限公司 | 京ICP证030173号-1 | baidu.com |   企业   |   无   |    否    | 2023-01-10 |
+--------------------------+-------------------+-----------+----------+--------+----------+------------+
```

### 结果处理

在程序运行未指定 `-o` 参数时，会直接以表格的格式输出查询结果

指定 `-o` 参数可以将查询结果保存到Excel中，如果未在参数后指定文件名，则使用当前时间戳作为文件名保存

```
python ICPCol.py -f targets.txt -o XX集团有限公司
```

通过 `-s` 参数可以根据查询结果自动生成 FOFA 查询语句，并将查询语句保存到 txt 文件中，生成的域名查询语法为 `domian="baidu.com"`，生成的IP地址查询语法为 `ip="127.0.0.1"`

```
python ICPCol.py -t 北京百度网讯科技有限公司 -s baidu.txt
```

### 使用代理

在进行批量查询时，如果查询目标过多超200以上，可能会导致IP被封禁，通过参数`-p`可以指定使用代理IP进行查询，避免被封禁，代理地址使用 **http** 协议时可以通过 `<ip>:<port>` 的格式指定代理

```
python ICPCol.py -f targets.txt -p 127.0.0.1:10809
```

或者使用完整代理地址格式 `<protocol>://<ip>:<port>`

```
python ICPCol.py -f targets.txt -p http://127.0.0.1:10809
```

如果使用 **socks5** 协议则指定代理地址如下

```
python ICPCol.py -f targets.txt -p socks5://127.0.0.1:10808
```

在进行批量查询时，如果IP地址被封禁会暂停程序运行不中断，**在手动更换IP地址或代理节点后**输入 `c` 可以进行后续目标备案信息查询

### 第三方查询

通过 `--third-party` 可以指定使用第三方备案网站进行查询，查询结果准确性降低，但不会被封IP

```
python ICPCol.py -t baidu.com --third-party
```
