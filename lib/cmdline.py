import argparse
import textwrap


def cmdline():
    banner = """\
       __     ______     ______   ______     ______     __        
      /\ \   /\  ___\   /\  == \ /\  ___\   /\  __ \   /\ \     
      \ \ \  \ \ \____  \ \  _-/ \ \ \____  \ \ \/\ \  \ \ \____  
       \ \_\  \ \_____\  \ \_\    \ \_____\  \ \_____\  \ \_____\ 
        \/_/   \/_____/   \/_/     \/_____/   \/_____/   \/_____/  by OssianSong"""
    parser = argparse.ArgumentParser(
        prog="python ICPCol.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(banner),
        exit_on_error=False,
        add_help=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", metavar="TARGET", type=str, help="输入公司名/备案号/域名/IP查询对应备案信息")
    group.add_argument("-f", metavar="FILE", type=str, help="从指定txt文件中读取数据进行批量查询")
    parser.add_argument("-o", metavar="FILENAME", nargs='?', default=argparse.SUPPRESS,
                        help="指定文件名将数据保存到Excel中,参数为空时使用默认文件名")
    parser.add_argument("-p", metavar="PROXY", type=str, help="使用代理查询，指定使用的代理地址")
    parser.add_argument("--third-party", action="store_true", default=False, help="使用第三方备案网站进行查询")
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='查看程序使用帮助')
    return parser