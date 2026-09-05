# 交接契约 v1

所有路径相对本次 production 根目录，UTF-8 编码。使用同一个 project_id、revision 和稳定 ID；路径变化不改变资产身份。用户指定的存储根目录优先，不硬编码作者电脑路径。凭据、签名下载地址、账户标识不进入公开交付包。

## 固定文件

- `01_world.md`：世界观。
- `02_story.md`：完整探索剧情与逐段逐镜执行脚本。
- `03_design_atlas.md`：人物、物品、关键场景的文字规则及真实设定图引用。
- `designs/`：实际设定图。图册的组成部分，不是用提示词代替图片。
- `handoff.json`：三份文档与下游资产的交接清单。
- `image_manifest.json`、`images/`：SOP 2 生成的剧情图像及来源。
- `video_manifest.json`、`videos/`：SOP 3 生成和交付的短视频及来源。
- `qa/`：检查结果；`requests/`：本地提交回执。回执可能含私密信息，不默认开源。

## handoff.json 字段

`schema_version` 固定 `1.0`；`project_id`、`revision`、`status` 必填。
`documents` 包含 `world`、`story`、`atlas` 三个相对路径。
`entities` 是对象数组，每项包含：
- `id`，如 `GLOBAL-TRAVELLER`、`ATL-CHAR-01`、`ATL-PROP-01`、`ATL-LOC-01`。
- `kind` 为 character / prop / location；`scope` 为 global / civilization。
- `version`、`locked_features` 字符串数组、`design_files` 路径数组、`status`。
- 可增加 `source`、`rights`、`state_variants`。global 必须真实存在或明确是首次创建的基线。

`segments` 是数组，每项包含 `id`、`duration_s`（15 至 20）、`story_anchor`（脚本章节标题）、`shots`。
每个 shot 包含 `id`、`start_s`、`end_s`（本段相对秒，连续覆盖整段）、`entity_ids`、`keyframe_ids`、`action`、`start_state`、`end_state`、`pov`、`era`。
`pov` 说明谁持有何种摄影机；`era` 区分当前、历史档案、重建，避免把档案当 Traveller 亲历。

## image_manifest.json 字段

包含 `schema_version`、`project_id`、`revision`、`status`、`images`。
images 每项包含 `id`、`shot_ids`、`entity_ids`、`reference_files`、`path`、`status`、`prompt`、`provider`、`model`、`qa`。
生成后增加 `sha256`、`width`、`height`、`request_id`、`source_revision`、`created_at`。失败项可保留，但不得被通过检查的镜头引用。

## video_manifest.json 字段

包含同样版本身份字段和 `videos`。每项包含 `id`、`segment_id`、`keyframe_ids`、`path`、`status`、`provider`、`model`、`qa`。
生成后增加 `duration_s`（实际文件测量）、`source_files`、`generation_ids`、`sha256`、`width`、`height`、`fps`、`audio`、`edit_notes`、`source_revision`。
平台原片时长另记 `generated_duration_s`；不得用目标时长冒充实测值。费用记录分开保存 `estimate`、`authorized_budget`、`actual_charge`（未知为 null）；余额变化不等于单任务账单。

## 状态与放行

status 使用 planned / generated / passed / failed / blocked / stale。只有实际文件存在且检查通过才能 passed。
- SOP 1：三份文档完整，entities 全部有通过检查的设定图，所有 segment 有可执行镜头，才将 handoff 标为 passed。
- SOP 2：脚本所需每个 keyframe_id 均有 passed 图像；提示词和空路径不算完成。
- SOP 3：每个 segment 对应 passed 的实际 MP4，时长均为 15–20 秒，全部解码成功，且通过视觉、声音和接镜检查。
- 上游改变身份、地理或剧情事实时递增 revision；依赖该项的下游标 stale，保留不受影响的资产，逐项重新检查。不要悄悄混合旧设定和新脚本。
- 文本完整但没有图片时，只能交付标明 blocked 的准备稿，不声称 SOP 1/2 已完成。允许按用户指定范围分批交付。
