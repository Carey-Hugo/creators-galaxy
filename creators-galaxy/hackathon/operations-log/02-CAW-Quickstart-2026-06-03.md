# CAW Quickstart 跑通 · Day 17

> 2026-06-03  ·  Hugo + Hermes
> 任务：Cobo Agentic Wallet 最小闭环演示（黑客松 Cobo 赛道必做）

---

## 一、目标

证明 CGHub Agent 可以：
1. 通过 Cobo Agentic Wallet 自主创建钱包（Agent 持有凭证，非 Portal 注册）
2. 在策略约束下执行链上操作
3. 触发超限时被 Policy 在服务端拦截，不上链

---

## 二、实操记录

### 2.1 安装 caw CLI

```bash
curl -fsSL https://raw.githubusercontent.com/CoboGlobal/cobo-agentic-wallet/master/install.sh | bash
# caw v0.2.84
```

### 2.2 Onboard（创建 Agent + MPC 钱包）

```bash
caw onboard --agent-name "CGHub-MVP-Agent" --wait
```

耗时：1分4秒
- 1/5 Agent provision：`caw_agent_54eeddcfaffb424f`
- 2/5 TSS Node 下载
- 3/5 TSS Node 初始化（节点 ID `cobo2G9oVQPRkquen4FAW1E3XBW7dyqt3F2C6dFKdhEeRXjW4H`）
- 4/5 TSS Node 启动
- 5/5 MPC Wallet 创建：`3a0bfd41-c5b6-410a-8bfa-0ab09b2199b0`

**生成地址：**
- ETH (Sepolia)：`0xf140fc225dcb2a94475f84a7a5b0b2c3768715c4`
- SOL：`Cx6rq3v7WJ8D8sFMmxjP3D4mywcUpFaMdHwvibz1Ttwg`

### 2.3 Faucet 领测试 ETH

```bash
caw faucet deposit --token-id SETH --address 0xf140fc225dcb2a94475f84a7a5b0b2c3768715c4
```

- 领取：0.01 SETH
- Faucet TX ID：`7fe4e5b0-41ca-46ac-8cb7-0e41d4908bc8`
- 45 秒后到账（balance 查询返回 0.01 SETH）

### 2.4 提交 Pact

```bash
caw pact submit \
  --intent "CGHub Agent: Test 0.001 SETH transfer on Sepolia" \
  --policies '[{
    "name":"sepolia-test-allow",
    "type":"transfer",
    "rules":{
      "effect":"allow",
      "when":{"chain_in":["SETH"],"token_in":[{"chain_id":"SETH","token_id":"SETH"}]},
      "deny_if":{"amount_gt":"0.002"}
    }
  }]' \
  --completion-conditions '[{"type":"tx_count","threshold":"2"}]'
```

**Pact ID**：`21949238-b169-4aea-a750-efcaa42e59e1`
**状态**：`active`（**未配对 App，自动批准**）

> **关键观察**：CLI 输出明确说"未配对 → 自动批准；配对后会转人工审批"

### 2.5 合规转帐（Policy 允许）

```bash
caw tx transfer \
  --pact-id 21949238-b169-4aea-a750-efcaa42e59e1 \
  --src-address 0xf140fc225dcb2a94475f84a7a5b0b2c3768715c4 \
  --dst-address 0x1111111111111111111111111111111111111111 \
  --token-id SETH --amount 0.001 --chain-id SETH \
  --description "CGHub quickstart: allowed 0.001 SETH transfer" \
  --request-id cghub-test-001
```

- TX ID：`d8115cc8-fb02-4be1-9d16-838f931d1b8e`
- **Transaction Hash**：`0x28015a0708ebc14aad46e808f9a737fe24d2016384d1eb8ac3941962d92cf09c`
- **Status**：`Success` ✅
- 实际 gas：0.000171516596118 SETH

### 2.6 超额转帐（Policy 拒绝）

```bash
caw tx transfer \
  --pact-id 21949238-b169-4aea-a750-efcaa42e59e1 \
  --src-address 0xf140fc225dcb2a94475f84a7a5b0b2c3768715c4 \
  --dst-address 0x1111111111111111111111111111111111111111 \
  --token-id SETH --amount 0.005 --chain-id SETH \
  --request-id cghub-test-002
```

**结果**：
```json
{
  "code": "TRANSFER_LIMIT_EXCEEDED",
  "message": "matched_pact_transfer_deny_if",
  "details": {
    "tier": "pact",
    "policy_type": "transfer",
    "policy_id": "69900cc0-a737-4326-bf19-b49375051a52"
  }
}
```

✅ **被正确拒绝，HTTP 403，未上链**

---

## 三、核心收获

### 3.1 跑通的概念链

```
Agent (caw CLI) 
  → submitPact (请求授权，附带 policies + completion_conditions)
    → Pact active (未配对自动批；配对走 Owner App 审批)
      → transferTokens (policy 评估: 0.001 allow, 0.005 deny)
        → on-chain success / policy_denied (server-side, 不上链)
          → audit log (结构化记录)
```

### 3.2 CGHub MVP 关键映射

| CAW 概念 | CGHub 场景 |
|---------|-----------|
| Agent (caw_ja...3jkc) | CGHub 贡献追踪 AI Agent |
| Wallet (MPC) | 创客星球收益分配钱包 |
| Pact | 某次分配任务（如：6月奖金分发） |
| Policy (deny_if amount_gt) | 防止 Agent 超额转帐（安全护栏） |
| Owner App Pair | Hugo 在手机审批（人为兜底） |
| Audit log | 链上贡献 + 分配的完整审计 |

### 3.3 实操发现

- **`--src-address` 必须显式传**，CLI 不会自动选源地址（虽然文档说"自动选最高余额"）
- **Pact 不配对就能跑**，但 production 场景必须配对 App（人工审批）
- **Deny 响应结构化**：`code` + `reason` + `details.policy_id`，Agent 可基于此做 retry 或通知
- **API Key 在 CLI 里脱敏**（`caw_ja...3jkc`），需要走 CLI 或从 profile/credentials 文件读全

---

## 四、卡点记录

### 4.1 App 配对受阻（华为 HarmonyOS）

- **设备**：华为 nova 5 / HarmonyOS 3.0
- **问题**：Cobo Agentic Wallet App 在出境易虚拟机里闪退
- **可能原因**：GMS 依赖 + 容器兼容性
- **决策**：**暂跳过 App 配对**，先用 CLI auto-approved 模式跑通技术闭环
- **后续**：如果 Demo 需要"人工审批"环节，用海外 Android/iPhone 真机或延期解决

### 4.2 SDK quickstart.ts 未跑（备选已替代）

- `quickstart.ts` 依赖真实 API Key（CLI 隐藏），需要从 profile 拿全
- 但**已用 CLI 完整跑通同一流程**（提交 Pact → 成功 + 拒绝），效果等同 SDK 演示
- 后续可补 SDK 真实 Key 版本

---

## 五、产出文件

| 路径 | 说明 |
|------|------|
| `hackathon/operations-log/02-CAW-Quickstart-2026-06-03.md` | 本文档 |
| `/tmp/caw-onboard.log` | onboard 完整日志 |
| `/tmp/caw-pact-submit.json` | Pact 提交响应 |
| `/tmp/caw-tx-allowed.json` | 合规转帐响应 |
| `/tmp/caw-tx-denied.json` | 拒绝响应（结构化） |

---

## 六、明日 / 下一步

- [ ] 写 `.env` 让 `npm run quickstart` 也能跑（用 profile 拿全 key）
- [ ] 跑 SDK 完整 quickstart 补充代码演示
- [ ] 配对 App（Hackathon Demo 前解决）
- [ ] x402 微支付示例（CGHub 核心场景）

---

> **Tag:** #CAW #Cobo #AgenticWallet #Hackathon #Day17 #MPC #Pact #Policy
