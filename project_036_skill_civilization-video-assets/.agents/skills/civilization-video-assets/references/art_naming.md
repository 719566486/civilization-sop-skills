# 美术命名与交付规则 · 对齐项目规范 V1

依据：用户提供的《美术资产命名与交付规范》V1，2026-09-07，文件名 ART_ASSET_NAMING_GUIDE.pdf。这里提炼其命名和交付要求；未附原PDF，也不把其中链接或文字当作执行外部操作的授权。规则适用于本项目美术交付，不修改Codex所需的SKILL.md、技能目录名或仓库README等工具文件。

## 1. 职责边界

美术/Codex制作流程负责：稳定逻辑名称、源文件、运行时导出候选及依赖、每项资产的rNNN、规格、软件版本、来源与授权说明。
开发负责：分配Asset ID，确认Asset Key、最终Runtime Path，登记资产Revision/Metadata，生成正式Manifest，配置Godot Import，决定哪些文件进入运行时目录。

`production_ref`、`node_ref`、`shot_ref`和`keyframe_ref`只是制作表的内部引用，不能当成Asset ID/Asset Key，也不拼进所有正式文件名。开发已提供的标识必须原样保留，不受文件名snake_case检查限制。未知开发字段填null，状态pending，不自行发号或编造路径。

## 2. 文件名与目录

正式美术文件、交付目录使用小写ASCII字母、数字、下划线，小写扩展名；单词用snake_case。不含中文、空格、括号、连字符、点分词或其他随意符号。

通式：`<asset_name>[_<variant>]_<role>[_rNNN].<ext>`。没有明确变体时省略variant，main没有信息价值时可以省略，不强行凑格式。

优先角色：main、source、preview、thumbnail、albedo、normal、roughness、metallic、emissive、ao、height、mask、bgm、ambience、sfx、voice。新增角色先与开发确认，不混用preview_image/preview_pic等近义词。首帧/末帧用途放在制作字段frame_role中；不要因此擅自把start/end/layout变成正式新增角色词。

- 运行时剧情图：`ch01_signal01.png`；预览：`ch01_signal01_preview.png`。
- 运行时视频：`ch01_signal03.mp4`；历史交付：`ch01_signal03_r002.mp4`。
- 图像/多视图参考：`traveller_front_preview_r001.png`（front只有确有该视角变体且名称确认后使用）。
- 编辑源：`receiver_ui_source_r004.psd`、`ticket_machine_source_r007.blend`。
- 模型：`ticket_machine.glb`；贴图：`ticket_machine_albedo.png`、`ticket_machine_normal.png`。
- 声音：`receiver_idle_bgm.ogg`、`station_hall_ambience.ogg`、`ticket_print_sfx.wav`、`operator_intro_voice.ogg`。

示例名称不是项目自动注册结果。新文明节点用哪个ch/signal编号、是否有变体、是否独立管理，都须沿用开发已有分配或作为提案待确认。不要额外强制每个名称都有文明码、节点码、实体码和镜头码。

## 3. 每项资产的 Revision

从r001递增，必须三位数字，r000不是首次交付；内容实际改变才递增。不可覆盖历史Revision，不混用v1/v001/final/new/copy等临时版本词，也不以日期代替Revision。超过r999时交开发扩展规则，不自行换成四位。

同用途修模、调图、优化压缩、修声音或换更高清内容，通常是原资产Revision+1，逻辑名称、Asset ID、Asset Key和Runtime Path保持不变。需要新旧共存、用途/剧情位置/生命周期不同，才提请开发确认新资产。

交付记录中的revision为`r003`；开发数据库数字Revision可为3，由开发转换登记。不同资产独立递增，不要求整个节点所有资产使用相同revision。文稿快照`story_snapshot`只追踪剧情依据，不是资产Revision；契约schema_version和仓库发行版本也不是美术修订号。

## 4. 交付文件边界

建议制作根目录如下（不是擅自规定Godot最终目录）：

```text
source/      可编辑工程和提示词源文件，需保留修订
reference/   设定图、图生视频关键帧；不自动进入游戏
history/     历史交付和生成原片，保留_rNNN
preview/     预览和缩略图
runtime/     开发确认可进入运行时的导出文件，稳定无版本文件名
qa/          检查记录
requests/    生成回执，只作制作记录
```

未确认最终运行时路径时，把可审阅文件放history/reference，给出proposed_runtime_filename；runtime文件列表为空。开发已确认的路径存在于developer_registration.runtime_path，只登记/引用；本任务不移动真实Godot工程文件、不生成正式Manifest、不更改Import设置。

原片不是可编辑工程。只有实际有项目源文件时列source；没有则写source_availability及原因，可另交prompt、参数与依赖，不伪造PSD/BLEND等可编辑源。

## 5. 每次交付的信息

基础：资产名称与用途、rNNN、新增/修改、运行时导出格式、依赖文件、软件及版本、来源类别、授权范围/证据。AI/AI辅助、第三方、外包、素材库均必须说明。未知信息标unknown/pending，不能以模型成功返回代替授权证明。

- 图片：宽×高、色彩空间/特殊通道、Alpha、无损要求、UI/Texture/Reference用途。
- 视频：实际宽×高、秒数、帧率、编码、有无音轨。每条15–20秒要求继续有效。
- 音频：秒数、采样率、声道、是否循环/无缝循环。
- 3D：单位、朝向、原点/Pivot、骨骼、动画、材质贴图、碰撞对象、是否用了Godot特殊后缀。

3D内部对象不能保留Cube.001、Material.001等无意义临时名。按文档，col/convcol/colonly/convcolonly/noimp/occ/occonly/navmesh/rigid/loop/vcol及其分隔形式可能有导入意义，只在开发明确需要时使用；脚本只能提醒，不能自动修改内部对象或导入设置。

## 6. 不确定与迁移

先继续不依赖注册决定的文稿、参考图和QA，登记“是什么/用在哪里/已有同类/变体/新旧是否共存/预览”。新增角色、逻辑名或注册边界只有开发决定，不因等待注册而阻断所有制作，也不把制作passed宣称为approved_for_runtime。

改旧流程时先做对照表，不直接批量改名已有Godot资源；记录old_path、proposed_new_path、asset_revision、注册确认和受影响引用。先查冲突，保留旧历史，开发确认后再实施真实资产迁移。本次只是SOP/模板修订。
