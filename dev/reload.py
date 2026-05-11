import sys

# 需要热加载的模块
PROJECT_PREFIX = (
    "launcher",
    "ui",
    "agent",
    "planner",
    "actions",
    "tools",
    "scene",
    "graph",
    "runtime",
    "llm",
    "controller",
    "houdini_adapter"
)


def hot_reload():
    """热加载，通过删除sys.modules中已加载的模块，再重新加载实现"""
    need_remove = []
    for module_name in sys.modules:
        if module_name.startswith(PROJECT_PREFIX):
            need_remove.append(module_name)
    for module_name in need_remove:
        del sys.modules[module_name]
        print("reload:", module_name)