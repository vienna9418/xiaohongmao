# 小红贸 GitHub 开发工作流

本文件定义小红贸 V1 的 GitHub 分支节奏、提交节奏和合并审批规则。

## 1. 总原则

- 所有开发步骤必须提交并推送到 GitHub。
- 功能开发不得直接写入 `main`。
- 所有合并到 `main` 的操作必须先获得项目负责人明确同意。
- 未经同意，我只能推送 feature/fix/chore 分支，不能执行 merge、rebase 合入主线、强推主线。
- 每个分支保持小范围、可验收、可回滚。

## 2. 分支模型

### 2.1 main

`main` 是稳定主线，代表当前可追溯、可运行的基线。只有经过用户同意后才能合并。

### 2.2 feature/*

用于新功能开发，例如：

- `feature/repo-foundation`
- `feature/backend-scaffold`
- `feature/frontend-scaffold`
- `feature/auth-rbac`
- `feature/account-matrix`
- `feature/content-factory`
- `feature/ai-prompt-skill`
- `feature/publish-worker`
- `feature/collect-worker`
- `feature/open-api-webhook`

### 2.3 fix/*

用于 bug 修复，例如：`fix/publish-task-retry`。

### 2.4 chore/*

用于工具链、文档、CI、配置维护，例如：`chore/github-actions`。

## 3. 开发节奏

每个开发单元按以下顺序执行：

1. 从最新 `main` 创建分支。
2. 完成该单元的代码、测试、文档。
3. 本地运行对应验证命令。
4. Git commit。
5. Git push 到远程同名分支。
6. 向用户汇报：分支名、commit、改动摘要、验证结果。
7. 等待用户同意是否合并。
8. 用户同意后，才执行合并到 `main` 并推送。

## 4. 合并规则

合并前必须向用户明确询问，例如：

> 分支 `feature/backend-scaffold` 已推送，验证通过。是否同意合并到 `main`？

只有用户明确回复同意后，才能执行：

```bash
git checkout main
git pull --ff-only
git merge --no-ff feature/<name>
git push origin main
```

如果用户要求修改，则继续在原 feature 分支提交并推送，不合并。

## 5. 提交规范

提交格式：

```text
type(scope): summary
```

常用 type：

- `feat`：新功能
- `fix`：修复
- `docs`：文档
- `test`：测试
- `chore`：工程配置
- `ci`：CI/CD
- `refactor`：重构

示例：

```text
feat(accounts): add account matrix api
test(publish): cover publish state transitions
chore(infra): add docker compose services
```

## 6. 推荐阶段分支节奏

### Phase 0

- `feature/repo-foundation`
- `feature/infra-compose`
- `feature/backend-scaffold`
- `feature/frontend-scaffold`

### Phase 1

- `feature/auth-models`
- `feature/auth-jwt`
- `feature/admin-layout`

### Phase 2

- `feature/account-matrix-api`
- `feature/account-matrix-ui`
- `feature/content-workflow-api`
- `feature/content-factory-ui`

### Phase 3

- `feature/ai-adapter`
- `feature/prompt-engine`
- `feature/skill-library`
- `feature/ai-center-ui`

### Phase 4

- `feature/publish-state-machine`
- `feature/celery-runtime`
- `feature/playwright-profile-manager`
- `feature/publish-executor`
- `feature/publish-console-ui`

### Phase 5

- `feature/collect-scheduler`
- `feature/content-metrics-collector`
- `feature/account-metrics-collector`
- `feature/account-metrics-rollup`

### Phase 6

- `feature/api-key-auth`
- `feature/public-api`
- `feature/webhook-delivery`
- `feature/risk-audit`
- `feature/github-actions`

## 7. Skill 使用策略

用户授权最多安装 40 个辅助 Skill。原则：

- 不为凑数量安装 Skill，只在具体开发阶段需要时安装。
- 安装前优先判断是否能显著提升质量或效率。
- 新安装 Skill 后提醒需要重启 Codex 才能生效。
- 开发中如需要 UI、测试、后端架构、CI、文档等专项 Skill，可按阶段安装。

当前阶段先不额外安装 Skill；进入前端 UI、自动化测试、CI 或复杂后端设计时，再按需安装。
