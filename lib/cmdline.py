import argparse
import textwrap


def cmdline():
    banner = """\
   __     ______     ______   ______     ______     __        
  /\ \   /\  ___\   /\  == \ /\  ___\   /\  __ \   /\ \     
  \ \ \  \ \ \____  \ \  _-/ \ \ \____  \ \ \/\ \  \ \ \____  
   \ \_\  \ \_____\  \ \_\    \ \_____\  \ \_____\  \ \_____\ 
    \/_/   \/_____/   \/_/     \/_____/   \/_____/   \/_____/ 

                        Version：v2.0.0      Author：OssianSong"""
    parser = argparse.ArgumentParser(
        prog="python ICPCol.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("\033[1;35m"+banner+"\033[0m"),
        exit_on_error=False,
        add_help=False)
    target = parser.add_argument_group("input")
    target.add_argument("-t", metavar="TARGET", type=str, help="输入公司名/备案号/域名/IP地址 询对应备案信息")
    target.add_argument("-f", metavar="FILE", type=str, help="从指定txt文件中读取数据进行批量查询")

    result = parser.add_argument_group("output")
    result.add_argument("-o", metavar="FILENAME", nargs='?', default=argparse.SUPPRESS,
                        help="指定文件名将数据保存到Excel中,参数为空时使用默认文件名")
    result.add_argument("-s", metavar="SIMPLE_FILE", nargs='?', default=argparse.SUPPRESS,
                        help="生成FOFA查询语法并保存到txt中,参数为空时使用默认文件名")

    option = parser.add_argument_group("options")
    option.add_argument("-p", metavar="PROXY", type=str, help="使用代理查询,指定使用的代理地址,格式：[Protocol://IP:Port]")
    option.add_argument("-tp","--third-party", action="store_true", default=False, help="使用非官方备案网站进行查询,不保证结果精确性")
    option.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='查看程序使用帮助')
    return parser