# Civilization SOP Skills · 文明资产制作三部曲

一句文明想法 → 世界观、Traveller 探索脚本、真实设定图册 → 剧情图像 → 每条 15–20 秒视频资产。

![三个SOP流程图](docs/workflow.png)

[打开介绍用流程图](docs/workflow.html) · [可编辑Mermaid源文件](docs/workflow.mmd) · [技能与工具说明](docs/tooling.md)

## 图文介绍

[从这里阅读三个 SOP 的图文导览](docs/visual-guide.md)。每个阶段各有一张可分享的流程详图，并链接到逐步操作手册。

### SOP 1 · 把一句想法，变成可制作的文明

![SOP 1 图解](docs/sop-1-illustrated.png)

### SOP 2 · 把设定图册，变成连续剧情图像

![SOP 2 图解](docs/sop-2-illustrated.png)

### SOP 3 · 把剧情关键帧，变成可用短视频

![SOP 3 图解](docs/sop-3-illustrated.png)

## 三个技能

| SOP | 调用名 | 主输入 | 主输出 |
|---|---|---|---|
| 1 文明创作总设定 | `$civilization-blueprint` | 一句话、可选已有母资产 | 世界观、脚本、含真实图的设定图册 |
| 2 图像资产生产 | `$civilization-image-assets` | SOP 1三份交付及实际设定图 | 连续剧情图、视频关键帧、对应清单 |
| 3 视频资产生产 | `$civilization-video-assets` | 脚本、设定图、SOP 2图片 | 每条15–20秒MP4、来源与验收记录 |

SOP 1 的设定图锁定“长什么样”；SOP 2 的剧情帧描述“正在发生什么”。人物、道具、场景均建立稳定ID，跨文明母资产可复用，每个文明的新实体单独设计。输出目录由使用者指定，不依赖作者电脑路径。


## v1.1 逐步操作手册

每份手册都覆盖七项：逐步工具、输入输出、参数与提示词、验收标准、失败返工、文件命名版本、单节点资产清单。

- [SOP 1 完整操作手册](project_034_skill_civilization-blueprint/.agents/skills/civilization-blueprint/references/operations-manual.md)
- [SOP 2 完整操作手册](project_035_skill_civilization-image-assets/.agents/skills/civilization-image-assets/references/operations-manual.md)
- [SOP 3 完整操作手册](project_036_skill_civilization-video-assets/.agents/skills/civilization-video-assets/references/operations-manual.md)

## 安装与调用

外层 `project_034_skill_*` 至 `project_036_skill_*` 用于归档命名；实际技能在各包的 `.agents/skills/` 中，文件夹名与 SKILL.md 的 name 相同。每个技能自带交接契约，可单独安装。无需复制其他技能或作者的模型、媒体和凭据。

将需要的内层技能目录复制到目标项目的 `.agents/skills/`，例如：

```text
你的项目/
  .agents/skills/
    civilization-blueprint/SKILL.md
    civilization-image-assets/SKILL.md
    civilization-video-assets/SKILL.md
```

完整复制每个目录，包括 references 与 agents；不要只复制 SKILL.md。也可将 GitHub 仓库地址和下表内层路径交给 `$skill-installer`，并明确你允许的安装路径。安装后在目标项目打开 Codex；未发现技能时重启会话。

| 技能 | 仓库内安装源路径 |
|---|---|
| civilization-blueprint | `project_034_skill_civilization-blueprint/.agents/skills/civilization-blueprint` |
| civilization-image-assets | `project_035_skill_civilization-image-assets/.agents/skills/civilization-image-assets` |
| civilization-video-assets | `project_036_skill_civilization-video-assets/.agents/skills/civilization-video-assets` |

```text
$civilization-blueprint 创建一个亚特兰蒂斯文明，输出到我指定的制作目录。
$civilization-image-assets 读取该制作目录的三份文档与设定图，生成剧情关键帧。
$civilization-video-assets 读取该目录的脚本、图册和关键帧，先核验Kling与Flova，使用可用且已授权的路线制作每条15–20秒的视频。
```

也可以明确要求顺序执行全部三阶段。技能不会携带账户权限，也不会把写作请求理解为无限费用授权。未配置生成工具时会完成可准备的文稿和任务表，并如实标记媒体阶段未完成。

安装结构与调用方式依据 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。本包是标准 Codex 文件夹技能，不是 Flova 云端 Skill，不会自动上传到 Flova。

## 工具选择

图像：Codex内置imagegen，或使用者实际配置的Image2服务。
视频：Kling MCP **或** Flova CLI；检查两者配置，但不强制同时安装。
后期：按需选择 FFmpeg，或 HyperFrames 及相关技能。只有素材生成需求时不强制复杂剪辑框架。
本地历史 gpt-image-2 适配器使用 Pilio 第三方服务；其他使用者可以采用自己的合法可用接口。不要把第三方服务当作内置 imagegen。模型参数、账户、时长、上传限制与计费均在运行时核验。

## 示例、验证与发布

`examples/atlantis/` 是缩略交接演示，包含一段18秒规划，所有媒体状态为 planned。它不是完整世界设定，更不是已经生成的图片或视频。

```text
python scripts/validate_bundle.py
python scripts/validate_bundle.py --production 你的制作目录
```

前一命令验证包结构、示例ID引用与时间表；后一命令还检查真实交接文件，拒绝缺少必要媒体的 passed 状态。它不代替看图、观看视频、试听和完整解码。

可将本目录整体上传到自己的 GitHub 仓库。提供 MIT LICENSE；许可仅涵盖本仓库原创流程、模板、示例和脚本，不包含原项目IP、美术资产、外部工具或第三方生成服务权利。未附原项目媒体、账户信息、临时签名URL或供应商技能全文。

验证与限制见 [QA报告](docs/QA.md)。本包封装与核验制作流程，示例未调用付费图像或视频生成。媒体生产效果需在使用者实际配置的环境中验证。
