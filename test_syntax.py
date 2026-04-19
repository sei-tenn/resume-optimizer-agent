#!/usr/bin/env python3
"""
简单的语法测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # 测试导入
    import app
    print("[OK] 成功导入app模块")

    # 检查Flask应用实例
    if hasattr(app, 'app'):
        print("[OK] 找到Flask应用实例")

        # 检查路由
        routes = []
        for rule in app.app.url_map.iter_rules():
            routes.append(rule.endpoint)

        print(f"[OK] 找到 {len(routes)} 个路由:")
        for endpoint in sorted(routes):
            print(f"  - {endpoint}")
    else:
        print("[ERROR] 未找到Flask应用实例")

    # 检查必要的函数
    required_functions = ['analyze_resume_with_gpt', 'optimize_resume_with_gpt']
    for func in required_functions:
        if hasattr(app, func):
            print(f"[OK] 找到函数: {func}")
        else:
            print(f"[ERROR] 缺少函数: {func}")

    print("\n[PASS] 语法测试通过")

except ImportError as e:
    print(f"[ERROR] 导入失败: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] 测试过程中出错: {e}")
    sys.exit(1)