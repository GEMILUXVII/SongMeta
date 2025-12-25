# SongMeta

音乐元数据处理器 - 批量处理MP3文件并生成格式化元数据

## 功能

- 从文件名中提取《》内的歌曲名并重命名
- 读取JSON元数据转换发布时间戳
- 通过QQ音乐API获取原唱歌手信息
- 自动下载专辑封面
- 生成JavaScript格式的元数据文件

## 使用

```bash
uv run python cli.py --source <源目录> --output <输出目录>
```

### 参数

| 参数 | 说明 |
|------|------|
| `-s, --source` | 源文件目录（必需） |
| `-o, --output` | 输出目录（默认 ./output） |
| `--covers` | 封面保存目录 |
| `--skip-api` | 跳过QQ音乐API调用 |

## 示例

```bash
uv run python cli.py --source D:\Desktop\starlight\audio\合集·瞳歌 --output D:\Desktop\starlight\audio\合集·瞳歌\output
```

## 许可证

本项目采用 [BSD 3-Clause License](LICENSE) 开源。

Copyright (c) 2025, GEMILUXVII

This software is licensed under the BSD 3-Clause License. Redistribution and use in source and binary forms, with or without modification, are permitted provided that the conditions of the license are met.

This software is provided "as is", without warranty of any kind. See the [LICENSE](LICENSE) file for details.
