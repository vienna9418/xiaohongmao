# 小红贸

企业小红书矩阵自动化运营后台。

## 当前阶段

V1 Phase 0：项目基础设施与脚手架。

## 文档

- V1 设计文档：`docs/superpowers/specs/2026-05-08-xiaohongmao-design.md`
- V1 实施计划：`docs/superpowers/plans/2026-05-08-xiaohongmao-v1-implementation-plan.md`

## 目录规划

```text
backend/       FastAPI 后端服务
frontend/      Vue 3 管理后台
infra/         基础设施配置
scripts/       开发辅助脚本
docs/          产品、设计、实施文档
```

## 开发约定

- 功能开发在 `feature/*` 分支进行。
- 合并到 `main` 前必须经过项目负责人确认。
- 每个可验收步骤都需要 commit 并 push 到 GitHub。
