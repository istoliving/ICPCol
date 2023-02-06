# -*- coding: utf-8 -*-
from lib.beianxICP import BeianX
from lib.cmdline import cmdline
from lib.miitICP import Miit
from lib.options import Options
from lib.output import save_to_excel, print_table


if __name__ == '__main__':
    # 获取输入参数
    args = Options(cmdline())
    domain_list = []
    if args.is_main:
        icp = Miit(args.method, args.proxy)
    else:
        icp = BeianX(args.method)
    # 单个查询
    if args.target:
        domain_list = icp.query(args.target)
        if args.out_type == 'print':
            print_table(domain_list)
        else:
            save_to_excel(domain_list, args.filename)
    # 多个查询
    elif args.filename:
        try:
            count = 1
            with open(args.filename, 'r', encoding='utf-8') as f:
                for target in f.readlines():
                    print("[{}] 查询对象：{}".format(count, target.strip()))
                    domain_list = icp.query(target.strip())
                    count += 1
                    # 对输出结果进行处理
                    if args.out_type == 'print':
                        print_table(domain_list)
                    else:
                        save_to_excel(domain_list, args.out_file)
        except Exception as e:
            print(e)
            print("[×] 打开文件不存在，请确认文件位置！")
    else:
        raise ValueError("[×] 请先指定查询目标！")