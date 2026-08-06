# 文件版本管理规则

当前有效文件：

不带版本号文件。

历史文件：

*_v1.py
*_v2.py
*_v3.py
*_v4.py

统一归档：

archive/

归档目录约定：

- `archive/backtest/`：旧回测与风险分析实现。
- `archive/scripts/legacy/`：被 V5 入口替代的数据/因子脚本。
- `archive/scripts/research/`：历史研究辅助脚本。
- `archive/results/`：冻结的历史回测与实验结果。
- `archive/tools/`：一次性迁移和旧调试工具。

当前结果规范：

新 V5 结果必须使用带版本的结果目录；禁止重新生成无版本的根目录 CSV、PNG 或 `results/` 目录。
