# Agent 记忆系统优化笔记

> 参考：https://github.com/MrtWallace/ai-web3-school/blob/main/notes/agent-memory-optimization.md
> 更新：2026-05-26

## 三层记忆架构

```
┌─────────────────────────────────────────┐
│  热层：MEMORY.md（~900 chars，限2200）      │
│  ├── 环境配置、品牌规范、Tailscale等        │
│  ├── 每轮固定注入，prefix-cache友好         │
│  └── fact_store 未覆盖的关键信息           │
└─────────────────────────────────────────┘
           │ 按需调用
           ▼
┌─────────────────────────────────────────┐
│  温层：fact_store（19条facts）             │
│  ├── 用户偏好、学习风格、项目概念           │
│  ├── Holographic SQLite（trust_score）    │
│  └── 按需recall，不每轮注入                │
└─────────────────────────────────────────┘
           │ 手动精确搜索
           ▼
┌─────────────────────────────────────────┐
│  冷层：Obsidian vault + session文件       │
│  └── 不主动注入，按需搜索                  │
└─────────────────────────────────────────┘
```

## 与原文的差异（我们已跳过的坑）

| 原文问题 | 我们现状 |
|---------|---------|
| observation/experience 双重存储 | fact_store 干净，无experience类型 |
| retain_every_n_turns=1 过快 | 我们的holographic无auto_retain |
| auto_recall 每轮注入 | 无auto_recall，按需调用 |
| 99%满需手动清理 | 已瘦身前置完成 |
| 45个未用tool | 待评估（未来优化方向） |

## fact_store 当前状态

```sql
分类分布：user_pref(1) · general(2) · concept(1) · project(4) · brand(1) · config(2) · learning(2) · preference(5) · role(1)
总计：19条facts（去重后）
信任分：general=0.4，其余=0.5
无内部重复 ✅
```

## 维护 cron

| 任务 | 频率 | Job ID |
|------|------|--------|
| fact_store bloat diagnostic | 每周一 09:00 | 92bd83d3610d |
| MEMORY + fact_store 去重检查 | 每周一 09:00 | d667e6a5515a |

## 待实现项

- [ ] 30天未recall → `cold:auto` 软删除标签
- [ ] proof_count 保护机制
- [ ] Tool 精简（45个未用tool待评估）
- [ ] 前60字符匹配 → 自动合并重复observation