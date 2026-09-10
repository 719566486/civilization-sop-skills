# 命名规范迁移 · 2026-09-10

依据《美术资产命名与交付规范》V1（2026-09-07），本次只更新SOP、三个skill、图解、示例与校验器；不批量改真实资产、不修改Godot资源引用。开源包1.3，交接契约2.0。

| 原约定 | 新约定 |
|---|---|
| 文明/实体/镜头大写码拼文件名 | 以已确认稳定asset_name为核心，小写snake_case；内部引用仅作制作表关联 |
| v001版本，或整包r1 | 每项美术资产独立r001；文稿快照独立字段story_snapshot |
| 成片final加版本后缀 | runtime/ch01_signal03.mp4；history/ch01_signal03_r002.mp4 |
| 图像/视频manifest | image_delivery.json与video_delivery.json；正式Manifest由开发生成 |
| 默认制作目录等于运行时素材目录 | source/reference/history/preview/runtime明确分开；由开发决定导入 |
| 制作ID默认等于资产身份 | production_ref不替代Asset ID；正式ID、Key、Path为空直至开发提供 |
| 只登记图像/视频基础规格 | 加上图片通道/Alpha/色彩，音频循环信息，3D单位/Pivot/骨骼及导入后缀，来源和授权 |

旧1.0清单不被新版自动接受。先保留旧件，人工/受控映射id→production_ref、引用字段→refs、全局revision→story_snapshot，再为每项资产补rNNN、文件分区与developer_registration；无法确认旧编号与正式资产的对应时保持pending，不凭转换创建新Asset ID。

修订史已保存在本地备份及GitHub历史。图文及安装入口沿用，不因美术命名规范改变Codex技能调用名。
