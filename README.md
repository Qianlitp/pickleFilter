# pickleFilter
a demo for filter unsafe callable object

利用对 load_reduce 函数添加装饰器，拦截了不信任的可调用对象，一定程度上减少 pickle模块 反序列缺陷所造成的危害。
