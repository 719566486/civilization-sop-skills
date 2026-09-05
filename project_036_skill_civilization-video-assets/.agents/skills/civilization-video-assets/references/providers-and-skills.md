# 后端与技能：发现、核验、按需加载

## Kling MCP

从当前会话可发现工具选择 Kling，首先调用 who_am_i，读取它返回的接口版本与模型参数。不要凭旧项目的参数名、最长秒数或积分价格发起新请求。确认图生视频、多图/首尾帧、原生音频分别是否支持。工具可见、OAuth 成功、账户有余额、项目可操作是不同状态。

建立参考图编号与实体 ID 的映射；使用上传工具实际返回的资源标识，不把本地路径或外部链接随便塞入上传资源字段。提交前保存完整任务意图；提交后先保存 ID 再处理其他输出。网络不确定先查原任务，避免重复收费。

## Flova CLI

通过 PATH 或用户提供位置发现 CLI；`flova version`（不是 --version）、`flova auth status` 是只读基础检查。保存令牌不代表账户余额正确；在实际生产前以 `flova account user` 和目标项目可访问性核验当前账户，脱敏展示，绝不打印凭据。

已安装 flova skill 时加载其相关生命周期章节。没有技能但有 CLI 时通过 `flova --help`、具体子命令帮助确认当前命令后执行，不臆造私有接口。登录属于用户参与的步骤；Windows 浏览器授权使用交互式终端，不能把无 TTY 导致的 empty token 直接判断为凭据损坏。

一次只发一个创作 run，平台拥有生成与运行状态。材料上传回执成功还要核对平台能读取。文字消息 completed 不代表视频已生成。当前本地 flova 技能指出其不直接交付烧录字幕、字幕轨或字幕文件；运行时再核实，若要求字幕则使用已授权的后期步骤或明确缺失，不伪称 Flova 已输出字幕。

## 技能职责表

| 技能/工具 | 职责 | 何时需要 |
|---|---|---|
| imagegen | Codex 内置生图、参考编辑 | SOP 1设定图、SOP 2关键帧路线之一 |
| gpt-image-2 / Image2 adapter | 接入实际图像服务商 | 用户选择该路线且已配置；不是内置生图别名 |
| flova | Flova项目、素材、运行、审阅、导出 | 选择Flova且有该技能时加载 |
| Kling MCP | 图生视频等模型调用 | 选择Kling；工具不是名为skill的必装包 |
| hyperframes | HyperFrames 工作流入口 | 实际使用该框架前加载 |
| general-video | 自定义多镜头编排 | HyperFrames剪辑流程 |
| hyperframes-core / hyperframes-cli | 时间轴、媒体组织、预览和渲染 | 编写/导出HyperFrames工程 |
| hyperframes-audio | 混音、淡化、对白闪避 | HyperFrames声音后期 |
| media-use | 音乐音效、媒体处理与来源 | 需要音频/媒体获取处理时 |
| hyperframes-keyframes / hyperframes-animation | 补充运镜/叠加动画 | 按设计需要，不是AI视频生成的替代 |
| hyperframes-creative | 非动画创意规范 | 使用框架进行声音/视觉规划时 |
| FFmpeg / ffprobe | 拼接、字幕、解码、时长、响度 | 轻量后期与最终文件验收；工具不等于同名skill |
| Whisper或其他转写工具 | 核对真实对白和字幕 | 有对白字幕时；识别结果仍需听辨 |

Remotion、ViMax、music、kling-cli 属于潜在替代流程或本地安装项，不是本套 SOP 的强制依赖；不能仅因作者机器有目录就声称每个历史片段都使用过它们。

## 费用

价格随模型、长度、分辨率、声音、重试而变。确认单项估价与总预算、无法锁定费用时的不确定性，再提交。用户允许范围内继续执行，不反复索要同一许可。账单不可得时实际费用写 unknown，不用余额差冒充。
