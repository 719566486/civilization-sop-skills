# 制作交接契约 2.0 · 美术交付记录，不是运行时 Manifest

先读 [命名与职责规则](art_naming.md)。所有制作文件UTF-8，路径相对production根目录；正式美术路径用snake_case。三个技能可单独使用，不依赖仓库外的规范文件。

## 固定主文件

- 01_world.md、02_story.md、03_design_atlas.md：三份主文档。
- handoff.json：剧情/设定的制作交接。
- image_delivery.json、video_delivery.json：图像/视频制作交付记录，取代旧的manifest命名。
- source、reference、history、preview、runtime、qa、requests：按命名规则分区。

正式Asset ID/Asset Key、最终Runtime Path、数据库Metadata、Manifest和Godot Import全部由开发登记。内部production_ref仅用于本制作表关联，不能替代正式标识。

## 顶层

三个JSON均包含schema_version=`2.0`、project_id、story_snapshot（如story_001）、status、delivery_status。
status：planned / generated / passed / failed / blocked / stale，指制作检查状态。
delivery_status：draft / ready_for_development / approved_for_runtime，分别为准备、可提交开发、开发确认的运行时交付。passed只说明媒体检查通过，不代表开发登记完成。
节点和角色引用不做美术文件名拼接，也不用顶层revision统管所有资产。

## handoff.json

documents包含world/story/atlas相对路径；entities每项包含production_ref、kind(character/prop/location)、scope(global/civilization)、locked_features、design_files及下述“资产记录”。nodes每项包含production_ref、duration_s(15–20)、story_anchor、shots。shots每项包含production_ref、start_s、end_s、entity_refs、keyframe_refs、action、start_state、end_state、pov、era，连续覆盖节点时长。

## 资产记录（实体及每个image/video均填写）

- production_ref：内部引用；asset_name：稳定逻辑名称提案或开发确认名称；name_status：proposed/confirmed。
- revision：每项资产rNNN；change_type：new/modified；purpose与runtime_export_format。
- files：source/runtime/preview/reference/history五类路径数组（本次资产修订的文件，旧历史另保留供previous对照）；dependencies：相对依赖路径数组。
- software：工具与版本对象数组；provenance：category、source、license_scope、evidence数组，所有未知值显式unknown。
- specifications：依媒介填写必要规格（见命名规则）。source_availability：available/not_available及原因。
- developer_registration：status pending/confirmed、asset_id、asset_key、runtime_path、confirmation。没有开发提供信息则后三个标识为null且confirmation为null；确认后原样引用。pending不得装成confirmed。
- proposed_runtime_filename：可为空，只是命名提案，不是最终Runtime Path。
- status与qa：制作状态及逐项检查。实体design_files必须指向真实设定图；媒体path为当前检查的真实文件，并属于files列表。

只有开发确认名称与注册资料后才能把文件列入runtime。该区不能放历史后缀、可编辑源、提示词和QA；目录runtime只是交付分区，不是Godot项目根。新角色词如有必要，写入developer_approved_roles，记录role与confirmation；没有确认不能使用。

## image_delivery.json

images数组每项除资产记录外还有shot_refs、entity_refs、reference_files、prompt、provider、model；生成后增加sha256、width、height、request_id、source_story_snapshot、created_at。规格至少有width、height、color_space、has_alpha、lossless、usage。设定图复用不表示所有图像都可作runtime。

## video_delivery.json

videos数组每项除资产记录外还有node_ref、keyframe_refs、provider、model；生成后增加duration_s（实测）、generated_duration_s、source_files、generation_ids、sha256、width、height、fps、audio、edit_notes、source_story_snapshot。规格至少有width、height、duration_s、fps、codec、has_audio。声音依赖还需记录audio_specifications的时长/采样率/声道/循环要求；没有音轨明确false，不伪造信息。

费用另记estimate、authorized_budget、actual_charge（未知null），不把余额差当单项账单。

## 放行与变更

SOP1需三文档完整、相关实体设定图均passed、逐镜可执行；SOP2需每个所需关键帧有passed实图；SOP3需各节点有passed且15–20秒的实片。缺工具可交blocked准备稿。缺开发登记仍可ready_for_development，不能approved_for_runtime。

同用途修改递增该资产revision，历史文件不能覆盖，已确认运行时路径和名称不变。文稿因果变化更新story_snapshot；依赖旧内容的下游标stale并重验，不把文稿版本当资产revision。确需新增资产先交开发确认。

2.0不静默接受旧1.0清单。旧数据先参考迁移对照，保留原件，只迁移制作表字段，不自动分配正式ID或重命名用户现有资源。

## SOP1叙事扩展：无人前文明

执行本技能还必须遵守 [遗迹与证据契约](ruins-evidence.md) 的ruins_1.0字段。handoff携带无人前提、evidence_plan.json、author_only_files与player_asset_refs；每镜有evidence_refs及player_visible_content，每节点有三层知识与未解疑点，每实体明确present_role和audience。

SOP2/3读取本包时，只把player_transmission允许的遗迹／物件／历史碎片内容制作成玩家传回资产；author_only母图可用于风格/结构约束但不能直接当剧情画面。不得加入当地居民，也不得从作者完整历史中擅自补上答案旁白。旧2.0校验器的结构通过不覆盖本扩展语义，需单独QA。
