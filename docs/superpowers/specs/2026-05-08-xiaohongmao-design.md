# 小红贸 V1 设计文档

日期：2026-05-08
项目目录：`D:\v1b\xiaohongmao`
版本范围：V1，企业小红书矩阵自动化运营后台，生产稳定版。

## 1. 产品定位

小红贸是面向企业的小红书矩阵运营后台。V1 聚焦内容矩阵业务，提供账号矩阵管理、AI 选题/文案、Prompt 配置、Skill 库、自动发布、自动采集、数据回流、开放 API、风控审计能力。

V1 明确采用“生产稳定版”目标：不是只跑通 Demo，而是具备任务锁、Worker 池、重试、监控、告警、异常恢复和可审计日志。

合规边界：系统服务于企业自有或已授权账号的运营自动化，不设计验证码绕过、黑产引流、批量骚扰、隐匿风控等能力。

## 2. 一级产品结构

1. 工作台
2. 账号矩阵
3. 内容工厂
4. AI 中心
5. 自动发布
6. 自动采集
7. 开放 API
8. 风控审计
9. 系统设置

## 3. 核心模块设计

### 3.1 工作台

工作台展示全局运营状态：今日待发布任务、今日采集任务、发布成功率、失败任务、账号健康分、爆款内容、AI 生成任务消耗、异常告警。

### 3.2 账号矩阵

账号矩阵是账号资产和数据复盘的统一入口，不再单独设置“数据复盘”一级模块。

账号列表展示：账号昵称、账号定位、负责人、粉丝数、近 7 日发布数、近 7 日曝光、近 7 日点赞、近 7 日收藏、近 7 日评论、爆文数、失败发布数、采集状态、账号健康分。

账号详情包含：基础信息、内容列表、自动发布记录、自动采集记录、数据趋势、账号画像、异常日志。

### 3.3 内容工厂

内容工厂覆盖从选题到发布后的数据回流：选题池 -> AI 生成 -> 人工编辑 -> 素材绑定 -> 审核 -> 排期 -> 自动发布 -> 自动采集 -> 数据回流账号矩阵。

内容状态：draft、ai_generated、editing、reviewing、scheduled、publishing、published、collecting、completed、failed。

### 3.4 AI 中心

AI 中心包含 AI 选题、AI 文案、Prompt 设置。

AI 选题输入：账号定位、目标人群、产品/服务、竞品关键词、近期热点、历史爆文数据。输出：选题标题、内容角度、用户痛点、种草逻辑、适合账号、推荐发布时间、风险提醒。

AI 文案支持：标题生成、正文生成、标签生成、评论区引导语、多账号差异化改写、爆文结构仿写、敏感词自检、品牌语气统一。

Prompt 设置支持：Prompt 模板、Prompt 变量、模型选择、温度参数、输出格式、适用账号、适用内容类型、版本管理、测试运行、效果评分。

### 3.5 Skill 库

Skill 是可复用的 AI 工作流模板。V1 支持爆文拆解、竞品笔记分析、标题生成、小红书种草文案、多账号差异化改写、违规词检测、评论回复建议等 Skill。

Skill 数据结构包含：skill_id、名称、描述、输入字段 Schema、Prompt 模板、输出 Schema、适用账号类型、适用内容类型、版本、评分、启用状态。

### 3.6 自动发布

自动发布采用 Playwright 浏览器自动化、账号独立 Browser Profile、任务队列、状态机、失败截图和结构化日志。

发布流程：创建任务 -> Worker 领取任务 -> 加载账号浏览器环境 -> 打开创作后台 -> 检查登录状态 -> 填写标题/正文/标签 -> 上传图片或视频 -> 预览校验 -> 发布或定时发布 -> 保存截图与结果 -> 更新任务状态。

发布状态：pending、running、login_required、uploading、submitting、success、failed、cancelled。

### 3.7 自动采集

自动采集必须接入 V1。采集分为内容数据和账号数据。

内容数据：曝光/阅读、点赞、收藏、评论、分享、涨粉贡献、发布时间、当前状态、违规/限流提示。

账号数据：粉丝数、关注数、获赞与收藏、近 7/30 天内容表现、互动趋势、爆文数量、低效内容数量。

采集频率：账号概览每天 1-2 次；内容数据在发布后 1h、6h、24h、72h、7d 采集；异常账号提高采集频率。

### 3.8 开放 API

V1 提供 API 接口，方便外部系统集成。

核心 API：账号 API、内容 API、AI 生成 API、Skill 执行 API、发布任务 API、采集任务 API、数据查询 API、Webhook API。

认证方式：后台用户使用 JWT；外部系统使用 API Key + 签名；Webhook 使用 Webhook Secret。

### 3.9 风控审计

风控审计用于保证系统可控、可追踪。V1 支持敏感词检测、相似文案提醒、重复素材提醒、单账号并发锁、异常任务告警、操作日志、任务日志、失败截图归档。

## 4. 技术栈选择

前端：Vue 3 + Vite + TypeScript + Element Plus + Pinia + ECharts。

后端：Python FastAPI + SQLAlchemy 2.x + Alembic。

数据库：PostgreSQL。

缓存与队列：Redis + Celery + Celery Beat。

自动化：Playwright Python。

AI：OpenAI-compatible API Adapter，支持多模型供应商切换。

文件存储：MinIO，接口兼容 S3，后续可切 OSS/S3。

日志监控：Structlog 或 Loguru，后续接 Sentry。

部署：V1 使用 Docker Compose；后续可迁移 Kubernetes。

## 5. 后端结构

建议后端模块：auth、users、accounts、contents、assets、ai、prompts、skills、publish、collect、metrics、integrations、risk、audit、webhooks。

核心数据表：users、roles、permissions、teams、platform_accounts、account_profiles、contents、content_assets、content_schedules、publish_tasks、publish_records、collect_tasks、metric_snapshots、prompt_templates、prompt_versions、skills、skill_runs、api_keys、webhook_configs、risk_rules、risk_events、audit_logs。

## 6. UI 风格与操作动线

小红贸 V1 的 UI 目标是现代化、简洁、高效，适合企业运营团队长时间使用。界面应减少装饰性元素，突出任务状态、数据变化和下一步操作。

### 6.1 视觉风格

整体风格：现代 SaaS 后台，浅色优先，支持后续扩展暗色模式。主色建议使用小红书关联但不过度艳丽的红色系作为强调色，搭配中性色背景和高对比文字。

设计关键词：清爽、克制、数据清晰、状态明确、操作路径短。

页面布局：顶部显示全局搜索、通知、当前团队与用户；左侧为一级导航；主区域使用卡片、表格、Tab、抽屉和弹窗组合。重要操作使用主按钮，危险操作必须二次确认。

### 6.2 信息层级

工作台优先呈现“今天要做什么”和“哪里异常”：待发布、待采集、失败任务、账号异常、爆文内容。账号矩阵优先呈现账号健康与关键指标，不让用户先进入详情页才能判断账号状态。

内容工厂以状态流转为核心，从草稿、AI 生成、审核、排期、发布、采集形成清晰流水线。自动发布和自动采集页面以任务队列为核心，突出状态、失败原因、重试入口、截图日志。

### 6.3 操作动线

核心动线一：账号运营

账号矩阵 -> 账号详情 -> 查看数据趋势 -> 发现低效/爆款 -> 进入内容工厂调整选题。

核心动线二：AI 内容生产

内容工厂 -> 选择账号/人设 -> 选择 Skill -> 选择 Prompt -> AI 生成 -> 人工编辑 -> 审核 -> 排期。

核心动线三：自动发布

内容详情 -> 创建发布任务 -> 自动发布队列 -> 查看实时状态 -> 成功归档或失败重试。

核心动线四：自动采集

发布成功 -> 自动创建采集计划 -> 周期采集 -> 指标回流账号矩阵和内容详情。

### 6.4 交互规范

表格支持筛选、排序、批量操作、列配置和保存视图。任务状态使用颜色和图标区分：等待、运行、成功、失败、需登录、已取消。复杂配置使用分步骤表单，避免一个页面堆满所有字段。AI 生成结果支持一键采纳、局部重写、版本对比和回滚。

## 7. 前端结构

建议前端模块：dashboard、accounts、contents、ai、prompts、skills、publish、collect、api-center、risk、settings。

页面优先级：登录页、后台主布局、账号矩阵、账号详情、内容工厂、AI 生成页、Prompt 配置页、Skill 库、发布任务页、采集任务页、开放 API 配置页、风控审计页。

## 8. 并发与任务方案

API 层使用 FastAPI async；任务调度使用 Celery Beat；任务执行使用 Celery Worker 多进程；浏览器自动化使用 Playwright Worker 池；AI 调用使用异步 HTTP 并发；采集入库使用批量写入。

并发控制规则：每个账号同一时间只允许 1 个发布或采集任务；全局发布并发限制；全局采集并发限制；AI 生成并发限制；任务失败自动重试；任务超时熔断；任务全链路日志追踪。

## 9. 测试方案

后端测试：pytest、httpx AsyncClient、测试 PostgreSQL/Redis。重点覆盖内容状态流转、Prompt 渲染、Skill 执行、发布状态机、采集状态机、API 权限、Webhook 签名。

自动化测试：Playwright Mock 页面测试，覆盖登录状态检测、发布表单填写、素材上传、发布成功识别、失败截图保存、采集字段解析。真实小红书后台测试只作为人工验收或受控环境验证。

AI 测试：Prompt 快照测试、输出 Schema 校验、敏感词检测、多账号差异化检测。

E2E 测试：创建账号 -> 配置 Prompt -> 创建 Skill -> AI 生成内容 -> 排期自动发布 -> 自动采集数据 -> 账号矩阵查看效果。

## 10. GitHub 交付流程

V1 开发要求每个明确开发步骤都上传 GitHub。开发流程采用小步提交、小步推送，保证每个阶段都可回滚、可审查、可部署。

### 10.1 分支策略

主分支：main，保持可运行状态。

开发分支：dev，用于集成 V1 日常开发。

功能分支：feature/<module-name>，例如 feature/auth、feature/accounts、feature/ai-center、feature/publish-worker。

修复分支：fix/<issue-name>。

### 10.2 每步开发要求

每个开发步骤必须包含：实现代码、必要测试、README 或接口文档更新、运行验证记录。步骤完成后执行本地测试，通过后提交 Git commit，并推送到 GitHub。

提交格式：type(scope): summary，例如 feat(accounts): add account matrix list，test(publish): cover publish task state machine。

### 10.3 推送节奏

Phase 0 到 Phase 6 每个子任务完成后都推送一次。关键节点需要创建 Pull Request 或至少保留清晰 commit 历史。自动发布、自动采集、AI Prompt/Skill 引擎这类高风险模块必须先进入 feature 分支，验证通过后再合入 dev。

### 10.4 GitHub Actions

后续配置 GitHub Actions，至少包含：后端测试、前端 lint/build、Docker Compose 配置检查。自动化浏览器真实平台测试不放入默认 CI，只跑 Mock 页面测试，避免依赖外部平台状态。

### 10.5 待提供信息

开始首次推送前需要确定 GitHub 仓库地址、认证方式和默认分支策略。如果还没有仓库，需要先在 GitHub 创建空仓库，或由本地初始化后推送到新仓库。

## 11. 开发阶段

Phase 0：项目初始化、Docker Compose、数据库、Redis、MinIO、代码规范、API 文档。

Phase 1：登录、用户、团队、角色权限、后台主布局。

Phase 2：账号矩阵、内容工厂、素材上传、内容状态流转。

Phase 3：AI 中心、Prompt 设置、Skill 库、AI 生成 API。

Phase 4：自动发布，包含 Playwright Profile、任务状态机、失败截图、任务日志、账号锁。

Phase 5：自动采集，包含账号数据、内容数据、周期采集、数据回流账号矩阵。

Phase 6：开放 API、Webhook、风控审计、监控告警。

## 12. 验收标准

V1 验收必须满足：能够管理多个企业自有小红书账号；能够通过 AI 生成选题和文案；能够配置 Prompt 和 Skill；能够创建发布任务并由 Worker 自动执行；能够自动采集账号和内容数据；账号矩阵能够展示数据趋势和异常；开放 API 可创建内容、执行 Skill、创建发布/采集任务、查询指标；所有关键操作有审计日志。

