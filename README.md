<h1 align="center">ICPCOL</h1>
<p align="center">
    工信部域名备案查询工具，可以对单一或批量主体备案信息查询，并支持结果导出
</p>
<p align="center">
    <img src="https://badgen.net/badge/language/python"> 
    <img src="https://badgen.net/github/stars/OssianSong/ICPCol">
    <img src="https://badgen.net/github/forks/OssianSong/ICPCol">
	<img src="https://badgen.net/github/issues/OssianSong/ICPCol">
    <a href="https://angesec.com"><img src="https://img.shields.io/badge/blog-@%20%E6%9A%97%E6%A0%BC%E5%AE%89%E5%85%A8-blue.svg?style=social"></a>
</p>
<br>


## 介绍

备案查询是信息收集中不可或缺的一环，目前最权威的备案信息查询渠道便是工信部备案查询系统。由于每次通过网站查询域名信息时都需要输入验证码，大大影响查询速度，并且无法进行批量备案查询，因此编写了此程序。ICPCol支持进行单一备案查询和批量查询，支持使用Excel存储查询结果

请勿将程序用于非法用途，下载程序即承认所造成的恶劣影响与作者无关

如果本项目有帮助到你，可以点个`Star`支持作者。


## 环境要求

在使用之前需要使用 pip 安装依赖库文件

```python
pip install -r requirements.txt
```

直接运行 python 脚本或使用 `-h` 参数可以查看功能列表

```
C:\>python ICPCol.py
usage: python ICPCol.py [-t TARGET | -f FILE] [-o [FILENAME]] [-p PROXY] [--third-party] [-h]

 __     ______     ______   ______     ______     __
/\ \   /\  ___\   /\  == \ /\  ___\   /\  __ \   /\ \
\ \ \  \ \ \____  \ \  _-/ \ \ \____  \ \ \/\ \  \ \ \____
 \ \_\  \ \_____\  \ \_\    \ \_____\  \ \_____\  \ \_____\
  \/_/   \/_____/   \/_/     \/_____/   \/_____/   \/_____/  by OssianSong

options:
  -t TARGET      输入公司名/备案号/域名/IP查询对应备案信息
  -f FILE        从指定txt文件中读取数据进行批量查询
  -o [FILENAME]  指定文件名将数据保存到Excel中,参数为空时使用默认文件名
  -p PROXY       使用代理查询，指定使用的代理地址
  --third-party  使用第三方备案网站进行查询
  -h, --help     查看程序使用帮助
```



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

### 结果处理

在程序运行未指定 `-o` 参数时，会直接以表格的格式输出查询结果

指定 `-o` 参数可以将查询结果保存到Excel中，如果未在参数后指定文件名，则使用当前时间戳作为文件名保存

```
python ICPCol.py -f targets.txt -o XX集团有限公司
```

### 使用代理

在进行批量查询时，如果查询目标过多超200以上，可能会导致IP被封禁，可以使用代理进行查询，代理地址使用`http` 协议时可以通过 `<ip>:<port>` 的格式指定代理

```
python ICPCol.py -f targets.txt -p 127.0.0.1:10809
```

或者使用完整代理地址格式 `<protocol>://<ip>:<port>`

```
python ICPCol.py -f targets.txt -p http://127.0.0.1:10809
```

如果使用`socks5`协议则指定代理地址如下

```
python ICPCol.py -f targets.txt -p socks5://127.0.0.1:10808
```

在进行批量查询时，如果IP地址被封禁会暂停程序运行不中断，在手动更换IP地址或代理后输入 `c` 可以进行后续目标备案信息查询

### 第三方查询

通过 `--third-party` 可以指定使用第三方备案网站进行查询，查询结果准确性降低，但不会被封IP

```
python ICPCol.py -t baidu.com --third-party
```

<br>

如果程序运行出现问题或有其他程序优化方案，欢迎在`Issue`中指出
