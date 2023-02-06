import time


class Options:
    def __init__(self, parser):
        # 初始化
        args = parser.parse_args()
        if not any(vars(args).values()):
            parser.parse_args(["-h"])
        # 获取参数值
        self.target = args.t
        self.filename = args.f
        self.proxy = args.p
        if args.p:
            self.proxy = {"http": '{}'.format(self.proxy),
                          "https": '{}'.format(self.proxy)}
        self.is_main = not args.third_party
        if "o" not in args:
            self.out_type = 'print'
        elif args.o:
            self.out_type = 'excel'
            self.out_file = args.o
        else:
            self.out_type = 'excel'
            self.out_file = time.strftime('%Y%m%d%H%M%S', time.localtime())
        if args.t:
            self.method = 'single'
        if args.f:
            self.method = 'multiple'
