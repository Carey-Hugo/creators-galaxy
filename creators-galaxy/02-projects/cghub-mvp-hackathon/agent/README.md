# Agent 火堆 · agent/

掌火人：大番薯。方案见 `docs/Agent方案设计.md`。

## 干嘛的

Agent 把贡献签成合约认的 EIP-712 证明，再驱动 Cobo 钱包把资金池里的钱按分数分给贡献者。这版是**骨架**，多数逻辑是最小实现 + `TODO`，等依赖到位再填。

## 目录

```
agent/
├── src/
│   ├── config.ts                # env + EIP-712 domain/types
│   ├── types.ts                 # ContributionProof 等共享类型
│   ├── abi.ts                   # 运行时加载 abi/ 下的真 ABI
│   ├── contribution-recorder.ts # 模块1：组织 proof + EIP-712 签名
│   ├── x402-prover.ts           # 模块2：Cobo 原生 x402 支付
│   ├── wallet-agent.ts          # 模块3：Cobo 调用（claimFor / payment / pending）
│   ├── mcp-server.ts            # 模块4：MCP 工具服务（stdio）
│   └── index.ts                 # 入口：端到端串联
├── tools/                       # MCP 工具
│   ├── sign-contribution.ts
│   ├── submit-contribution.ts
│   ├── check-pending.ts
│   └── trigger-claim.ts
├── abi/                         # ABI 由合约负责人提供，放 ContributionPool.abi.json（见 abi/README.md）
├── .env.example
├── package.json
└── tsconfig.json
```

## 跑

```bash
npm install
cp .env.example .env   # 填私钥、RPC、Cobo key
npm run dev            # 端到端自测
npm run mcp            # 起 MCP server
```

## 跑通前的依赖（都在方案第九节）

- `AGENT_PRIVATE_KEY`：必须等于链上 `agentSigner()`，找白织要
- `abi/ContributionPool.abi.json`：合约负责人提供，丢进 `abi/` 即可（代码运行时读，缺了会报错）
- `EXECUTOR_PRIVATE_KEY` + `SEPOLIA_RPC_URL`：发记录交易用
- Cobo 三件套：`AGENT_WALLET_API_URL/API_KEY/WALLET_UUID`
- x402 演到多深、谁发记录交易：待团队 Day3 定
