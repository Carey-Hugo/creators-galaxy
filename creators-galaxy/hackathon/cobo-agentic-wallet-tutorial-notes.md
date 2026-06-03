# Cobo Agentic Wallet 开发者教程 · 团队速读笔记

> 来源：官方教程 https://docs.google.com/document/d/14rwdgmao_pwOxZozwaZA97k8C-HvG_0fEi703QY8wEo  
> 整理者：Hermes（CGHub Hackathon 备战）  
> 时间：2026-06-03

## 1. CAW 是什么

Cobo Agentic Wallet = 给 AI Agent 用的**链上钱包**。
- Agent 直接拥有钱包能力：转账、合约调用、消息签名
- 支持人类监管：配合 CAW App 做"配对 + Pact 审批"
- 底层基于 **MPC-TSS**（多方计算门限签名），密钥不集中

## 2. 三种接入方式（推荐顺序）

| 方式 | 适用 | 备注 |
|------|------|------|
| **Skills** | Agent 自动接入 | 官方推荐，能力最强 |
| **MCP Server** | 通用 AI Agent | 标准 MCP 协议 |
| **CLI / API / SDK** | 程序化直接控制 | 最底层，最灵活 |

## 3. 核心概念

### Wallet（钱包）
- 每个 Agent 可创建多个钱包（每次 `caw onboard` 创建一个 profile）
- 多链同地址：ETH 类型代表所有 EVM 链

### Profile（配置文件）
- 路径：`~/.cobo-agentic-wallet/profiles/profile_caw_agent_xxxx/`
- 包含 credentials、tss-node 配置、密钥分片
- 默认操作只对 `default_profile` 生效

### TSS Node（门限签名节点）
- 必须**持续运行**
- 用于钱包创建 + 签名
- 启动命令：`cobo-tss-node start --caw`
- 初次启动报错 "invalid node ID" 属正常，先忽略等钱包创建完成

### Pact（策略合约）
- Agent 发起交易前必须提交 Pact
- 人类在 App 端审批
- 审批通过后，Agent 在 Pact 规则限制内自由发起交易
- Pact 批准后会生成**新的 API Key**，后续交易必须用这个 Key

### App 配对
- 8 位数字配对码
- TestFlight App 支持 **Mock 登录**（任意字符串即可）
- ⚠️ Mock 登录不要充真实大额资产
- 备份好钱包文件，丢失无法恢复

## 4. 关键 API 端点

```
POST   /api/v1/principals/provision      # 创建初始 API Key + agent_id
POST   /api/v1/wallets                   # 创建钱包（需 main_node_id）
GET    /api/v1/wallets                   # 查看钱包列表
POST   /api/v1/wallets/{uuid}/addresses  # 创建地址（chain_type: ETH/SOL）
POST   /api/v1/wallets/pairs/initiate    # 发起配对，返回 8 位配对码 token
POST   /api/v1/pacts/submit              # 提交 Pact 策略
GET    /api/v1/pacts/{pact_id}           # 查看 Pact 状态
```

## 5. 完整流程（从 0 到 1）

```
1. 安装 caw CLI（通过 Skills 脚本）
2. 启动 tss-node
3. provision → 拿到 agent_id + api_key
4. 创建 wallet → 拿到 wallet_uuid
5. 创建 address → 拿到链上地址
6. initiate pair → 拿到配对码
7. App 端输入配对码 → MPC 交互完成配对
8. submit pact → App 端审批
9. 用 Pact 生成的 API key 发起交易
```

## 6. 实战示例：Uniswap V3 Swap on Base

**Step 1 - 创建 Pact：**
```bash
export PATH="$HOME/.cobo-agentic-wallet/bin:$HOME/.local/bin:$PATH"

POLICIES=$(jq -c -n '[{
  "name":"base-eth-usdc-uniswap-v3-swap",
  "type":"contract_call",
  "rules":{
    "effect":"allow",
    "when":{
      "chain_in":["BASE_ETH"],
      "target_in":[
        {"chain_id":"BASE_ETH","contract_addr":"0x2626664c2603336E57B271c5C0b26F421741e481"},
        {"chain_id":"BASE_ETH","contract_addr":"0x4200000000000000000000000000000000000006"},
        {"chain_id":"BASE_ETH","contract_addr":"0x833589fcd6edb6e08f4c7c32d4f71b54bdA02913"}
      ]
    },
    "deny_if":{"usage_limits":{"rolling_24h":{"tx_count_gt":1}}},
    "always_review":true
  }
}]')

caw pact submit \
  --name "Swap 0.0005 ETH to USDC on Base" \
  --intent "Swap 0.0005 ETH to USDC on Base via Uniswap V3" \
  --original-intent "我已经完成配对了..." \
  --recipe-slugs uniswap-v3-swap \
  --policies "$POLICIES" \
  --completion-conditions '[{"type":"tx_count","threshold":"1"}]' \
  --execution-plan "# ..." \
  --context '{"chain_id":"BASE_ETH","token_in":"BASE_ETH","token_out":"BASE_USDC","amount_in_eth":"0.0005","amount_out_min_usdc":"0.994208"}'
```

**Step 2 - App 批准后，用 pact_id 发起交易：**
```bash
CALLDATA=$(caw util abi encode \
  --method "exactInputSingle((address,address,uint24,address,uint256,uint256,uint160))" \
  --args '[["0x420...","0x833...","500","0xfd6...","500000000000000","994208","0"]]' | jq -r .calldata)

caw tx call \
  --pact-id 66204d5d-2a26-454a-82d2-d8eb2ee7c80f \
  --chain-id BASE_ETH \
  --contract 0x2626664c2603336E57B271c5C0b26F421741e481 \
  --calldata "$CALLDATA" \
  --value 0.0005 \
  --src-address 0xfd65955567d69f97d6a0c5985a819a9a220c55f9 \
  --request-id base-eth-usdc-swap-20260601-0001
```

## 7. 环境地址

| 环境 | 用途 | 官网 |
|------|------|------|
| 正式环境 | 生产 | https://agenticwallet.cobo.com/agentic-wallet |
| 开发者环境 | 测试（有 Open API docs） | https://agenticwallet.dev.cobo.com/agentic-wallet |

API 文档：https://api-core.agenticwallet.dev.cobo.com/api/v1/docs

## 8. SDK

- **Python**：`pip install cobo-agentic-wallet`
  - 仓库：https://github.com/CoboGlobal/cobo-agentic-wallet-python-sdk
  - 已封装常用 Agent 框架的 Tools
- **TypeScript**：`npm install @cobo/agentic-wallet`
  - 仓库：https://github.com/CoboGlobal/cobo-agentic-wallet-typescript-sdk

## 9. 黑客松 MVP 集成建议

**对 CGHub 价值：**
- 每个 Agent 配 CAW 钱包 → 价值分配自动结算
- Pact 策略 = CGHub 治理规则的可执行版本
- App 端审批 = 人类在关键节点的话语权

**最小闭环 Demo：**
1. 创客提交贡献 → Agent 评估 → 自动发放星钻（USDC 收款）
2. 每个 Agent 持 CAW 钱包接收奖励
3. Pact 限制支出规则（如 24h 不超过 N 笔）
4. 人类通过 App 监督异常交易

## 10. 小作业（官方布置）

- ✅ 通过 Agent + Skills 完成任意钱包操作（转账/合约调用/消息签名）
- ✅ 通过 API / SDK 完成任意 DeFi 操作

---

## 核心心智模型（一句话）

**CAW = 让 AI Agent 真正"持有资产 + 执行链上动作 + 接受人类监管" 的合规钱包。**
