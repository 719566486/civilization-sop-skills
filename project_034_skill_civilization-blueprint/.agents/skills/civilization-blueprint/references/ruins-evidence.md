# 无人遗迹与玩家证据契约 · ruins_1.0

## 前提与时间层

所有探索当下的场景均为已废弃的前文明遗迹，无该文明现存居民。Traveller与明确授权的外来装备可以出现。普通生态是否存活由文明设定决定，不能以生态细节变相加入说话生物、当地智慧群体或任务向导。

每个重要地区同时写四层：昔日用途和使用者；废弃原因及经过时间；目前可见状态；它为何还保存这些证据。曾经的人群属于历史，不安排成当前演员。不要默认满城尸体或恐怖化；离去、毁灭与失联可依故事设置，作者内部需有一致解释。

古设备可以周期性动作、输出故障码或重复有限录音，但不能与Traveller自由问答。录音不默认存在；使用时要解释存储、供能和缺失，并让它只回答局部问题。自动清扫也不能成为维持满城有人生活假象的便利借口。

## 三层知识与玩家自主推理

1. author_truth：内部完整历史与因果，为设计保持一致；不出现在传回画面的字幕、旁白或图册标签中。
2. traveller_knowledge：他截至此节点实际观察过的事实与可撤回假设；不允许知道未去过的地点或未读取的线索。
3. player_evidence：玩家真正得到的影像、照片、声音或物件扫描内容。明确写出visible_fact，不把“曾经是水权贵族”之类解释当成直接可见事实。

关键结论尽量有两类独立痕迹交叉支持，例如建筑接入差异与配额陶牌；同一铭文拍两次不算独立证据。证据不充分时，保留不确定程度和有依据的替代解释，不能声称唯一答案。允许有未解部分，但必需推断不能依赖从未向玩家提供的线索。

Traveller台词宜为“磨痕朝下……这里也许曾沿导轨移动”，而不是“128年前三派一致表决下沉”。不要让片尾全知总结把玩家的解释工作接管。明确区分机械功能被实验验证与历史动机仍未知。

## 在制作表中追加的字段

保留交接schema_version=2.0及原命名字段；以下为SOP1必填的叙事扩展。旧2.0脚本校验器不会自动验证这些语义，要在QA中单独核对，不把字段存在等同于叙事通过。

handoff顶层：
```json
{
  "narrative_contract_version": "ruins_1.0",
  "world_state": "abandoned_precursor_ruins",
  "present_civilization_population": 0,
  "player_reconstructs_history": true,
  "evidence_plan": "evidence_plan.json",
  "player_asset_refs": [],
  "author_only_files": ["01_world.md", "02_story.md", "03_design_atlas.md", "evidence_plan.json"]
}
```

player_asset_refs是待生成或已生成的制作引用白名单，不是运行时Manifest。正式发布前必须解析到已验收实际文件；原始内部证据表可能包含答案，不能直接发给玩家。除非确有混合用途，asset记录的audience用author_only或player_transmission；role词和文件命名不因此增加新后缀。

每镜追加：era=present_ruins（有特批历史碎片则明确记录媒介）；evidence_refs；player_visible_content；allowed_inference；spoiler_constraints。每实体追加present_role=external_explorer / external_equipment / ruin / relic / historical_depiction；不允许present_resident。历史描绘必须依附具体遗物或记录，不可变成站在遗迹内的活人。

## 单条证据记录模板

```json
{
  "evidence_ref": "evidence_01",
  "node_refs": ["node_01"],
  "shot_refs": ["shot_01"],
  "transmitted_asset_refs": ["frame_01"],
  "source_entity_ref": "water_gate",
  "visible_fact": "关闭的闸门内侧有向下平行磨痕，缝隙被盐结晶填满",
  "preservation_reason": "遮蔽侧磨痕未被直接海流冲刷",
  "author_truth": "闸体曾受控下放；这条证据本身不能解释动机",
  "traveller_observation": "磨痕大体同向，尚不能判断发生年代",
  "supported_inferences": ["闸体可能沿导轨移动过"],
  "alternative_explanations": ["灾变中沿原有导轨下滑"],
  "does_not_prove": ["下沉获得全民同意", "城市当下仍有人"],
  "corroborating_evidence_refs": [],
  "confidence": "tentative",
  "spoiler_constraints": ["不配完整历史复原", "不自动显示历史答案字幕"],
  "status": "planned"
}
```

## 反向验收与旧稿迁移

逐镜检查：是否有当地活人／人影／对话NPC；残留声光是否被误说成有人；建筑是否仍像刚有人维护；推断是否超出可见证据；是否把内部答案或完整盛世全景当传回内容；一个关键结论是否只能靠作者知道。

由“有人文明”迁移时，不能只删除画面中的居民：须重写引导动机、交接物件、机关操作知识来源、对白、证据链与遗弃状态。更新story_snapshot；受影响的SOP2/3资产标stale，保留旧图与rNNN历史，不静默当作当前合格。无需自动重新生图，按用户新的制作请求再执行。
