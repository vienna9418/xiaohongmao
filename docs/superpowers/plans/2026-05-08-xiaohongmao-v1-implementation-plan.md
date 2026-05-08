# 小红贸 V1 实施计划

日期：2026-05-08
目标：按生产稳定版实现小红贸 V1，覆盖账号矩阵、内容工厂、AI 中心、Prompt/Skill、自动发布、自动采集、开放 API、风控审计。

## 0. 开发规则

- 每个可验收步骤必须本地测试、commit、push GitHub。
- 默认分支：main。
- 功能开发使用 feature/* 分支；阶段完成后合入 main。
- 提交格式：type(scope): summary。
- 自动发布/自动采集仅用于企业自有或授权账号，不实现验证码绕过、风控规避、骚扰式操作。

## 1. Phase 0：项目脚手架与基础设施

### 1.1 仓库基础文件

交付物：.gitignore、.editorconfig、README 更新、docs 目录结构。

验证：git status 干净；README 能说明本地启动目标。

提交：chore(repo): add base repository files

### 1.2 Docker Compose 基础服务

交付物：docker-compose.yml，包含 PostgreSQL、Redis、MinIO。

验证：docker compose up -d 能启动基础服务。

提交：chore(infra): add docker compose services

### 1.3 后端 FastAPI 脚手架

交付物：backend 目录、pyproject.toml、FastAPI app、健康检查接口、配置模块、日志模块。

验证：后端启动后 GET /health 返回 ok。

提交：feat(backend): scaffold fastapi service

### 1.4 前端 Vue 脚手架

交付物：frontend 目录、Vue 3 + Vite + TypeScript + Element Plus + Pinia + ECharts。

验证：前端能启动并访问基础页面。

提交：feat(frontend): scaffold vue admin app

## 2. Phase 1：认证、权限、后台框架

### 2.1 用户与权限模型

交付物：users、roles、permissions、teams 数据模型；Alembic 迁移。

验证：迁移可执行；测试库能创建默认管理员。

提交：feat(auth): add user role permission models

### 2.2 登录与 JWT

交付物：登录接口、刷新 token、当前用户接口、密码哈希。

验证：pytest 覆盖登录成功/失败/鉴权。

提交：feat(auth): add jwt login flow

### 2.3 前端后台布局

交付物：登录页、主布局、左侧导航、顶部栏、路由守卫。

验证：未登录跳转登录；登录后进入工作台。

提交：feat(ui): add admin layout and login page

## 3. Phase 2：账号矩阵与内容工厂

### 3.1 账号矩阵后端

交付物：platform_accounts、account_profiles、metric_snapshots 基础模型；账号 CRUD API。

验证：pytest 覆盖账号创建、查询、更新、删除。

提交：feat(accounts): add account matrix api

### 3.2 账号矩阵前端

交付物：账号列表、账号卡片、账号详情 Tab、基础指标展示。

验证：可创建账号并在列表展示。

提交：feat(accounts): add account matrix pages

### 3.3 内容工厂后端

交付物：contents、content_assets、content_schedules 模型；内容 CRUD、状态流转 API。

验证：pytest 覆盖 draft -> reviewing -> scheduled 等状态流转。

提交：feat(contents): add content workflow api

### 3.4 内容工厂前端

交付物：内容列表、内容编辑器、状态筛选、素材绑定入口。

验证：可创建内容、编辑内容、变更状态。

提交：feat(contents): add content factory pages

## 4. Phase 3：AI 中心、Prompt、Skill

### 4.1 AI Adapter

交付物：OpenAI-compatible adapter、模型配置、超时/重试、结构化输出校验。

验证：Mock AI 响应测试通过。

提交：feat(ai): add openai compatible adapter

### 4.2 Prompt 管理

交付物：prompt_templates、prompt_versions 模型；Prompt 变量渲染、版本管理、测试运行 API。

验证：pytest 覆盖变量渲染、版本切换、缺失变量报错。

提交：feat(prompts): add prompt template engine

### 4.3 Skill 库

交付物：skills、skill_runs 模型；Skill 输入 Schema、Prompt 绑定、输出 Schema 校验、执行 API。

验证：pytest 覆盖 Skill 执行成功、Schema 校验失败。

提交：feat(skills): add skill library engine

### 4.4 AI 前端页面

交付物：AI 生成页、Prompt 设置页、Skill 库页、Skill 执行记录页。

验证：可选择账号、Skill、Prompt 并生成内容草稿。

提交：feat(ai): add ai center pages

## 5. Phase 4：自动发布生产稳定版

### 5.1 发布任务模型与状态机

交付物：publish_tasks、publish_records；状态 pending/running/login_required/uploading/submitting/success/failed/cancelled。

验证：pytest 覆盖合法/非法状态流转。

提交：feat(publish): add publish task state machine

### 5.2 Celery Worker 基础

交付物：Celery app、Redis broker、Worker 启动配置、任务日志、失败重试。

验证：测试任务可异步执行并写回状态。

提交：feat(worker): add celery task runtime

### 5.3 Playwright Profile 管理

交付物：账号独立 browser profile/storage_state 管理、登录状态检测接口。

验证：Mock 页面测试通过；不同账号 profile 相互隔离。

提交：feat(publish): add playwright profile manager

### 5.4 自动发布执行器

交付物：发布表单填写、素材上传、提交、截图、失败日志。真实平台选择器集中配置，便于维护。

验证：Mock 创作后台页面端到端测试通过。

提交：feat(publish): add automated publish executor

### 5.5 发布前端页面

交付物：发布任务队列、状态详情、失败截图、重试/取消按钮。

验证：前端可创建任务并查看状态变化。

提交：feat(publish): add publish task console

## 6. Phase 5：自动采集生产稳定版

### 6.1 采集任务模型与周期调度

交付物：collect_tasks、metric_snapshots；发布后 1h/6h/24h/72h/7d 周期计划。

验证：Celery Beat 能生成采集任务。

提交：feat(collect): add collect scheduling

### 6.2 内容数据采集器

交付物：笔记曝光、点赞、收藏、评论、分享、状态提示采集逻辑。

验证：Mock 数据页面解析测试通过。

提交：feat(collect): add content metrics collector

### 6.3 账号数据采集器

交付物：粉丝数、获赞收藏、近 7/30 天趋势、异常状态采集逻辑。

验证：Mock 账号后台页面解析测试通过。

提交：feat(collect): add account metrics collector

### 6.4 数据回流账号矩阵

交付物：账号健康分、趋势图、爆文/低效内容统计。

验证：采集数据写入后账号矩阵指标更新。

提交：feat(accounts): connect collected metrics to matrix

## 7. Phase 6：开放 API、Webhook、风控审计

### 7.1 API Key 与签名认证

交付物：api_keys 模型、签名校验、中间件、接口权限。

验证：pytest 覆盖签名正确/错误/过期。

提交：feat(api): add api key signature auth

### 7.2 开放 API

交付物：账号、内容、AI、Skill、发布任务、采集任务、指标查询 API。

验证：OpenAPI 文档完整；接口测试通过。

提交：feat(api): add public integration endpoints

### 7.3 Webhook

交付物：webhook_configs、事件投递、重试、签名。

验证：Mock Webhook 接收端测试通过。

提交：feat(webhook): add event delivery

### 7.4 风控审计

交付物：敏感词、相似文案、重复素材、账号并发锁、操作日志、任务日志、异常告警。

验证：pytest 覆盖规则命中、审计日志写入、账号锁互斥。

提交：feat(risk): add risk audit controls

## 8. CI 与质量门禁

- 后端：pytest。
- 前端：lint、typecheck、build。
- Docker：compose config 校验。
- Playwright：默认只跑 Mock 页面测试。

提交：ci: add github actions quality checks

## 9. V1 最终验收

验收流程：初始化服务 -> 创建账号 -> 配置 Prompt -> 创建 Skill -> AI 生成内容 -> 排期发布 -> Worker 自动发布 Mock 流程 -> 自动采集 Mock 数据 -> 账号矩阵展示趋势 -> 外部 API 查询指标 -> 审计日志完整。

验收提交：release: prepare xiaohongmao v1 baseline
