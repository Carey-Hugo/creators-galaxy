# Agent 火堆 · agent/

掌火人：大番薯。方案见 `docs/Agent方案设计.md`。

## 干嘛的

Agent 用 agentSigner 私钥把贡献签成合约认的 EIP-712 证明，再让 CAW 钱包把交易发上链（记录贡献 / 代领分账）。签名在 Cobo 服务端完成，本机不需要装 caw、不需要 TSS 分片。

闭环：`agentSigner 签 proof（链下）→ CAW 钱包 contractCall 上链 → ContributionPool 验签记账 / claimFor 分账`。

## 队友怎么跑（拉下来即用）

```bash
cd agent
npm install
npm run dev    # 端到端自测：签贡献 → CAW 上链 recordContributionBySig
npm run api    # 起 HTTP API 给前端（默认 :8787），见 docs/API.md
npm run mcp    # 起 MCP server（stdio）
```

`.env` 已随仓库提交（私有库），凭证都在里面，**不用再配**。`abi/ContributionPool.abi.json` 也在仓库里。签名走 Cobo 服务端，所以任何机器都能用同一把 CAW 钱包。

## 目录

```
agent/
├── src/
│   ├── config.ts                # env + EIP-712 domain/types
│   ├── types.ts                 # ContributionProof 等类型
│   ├── abi.ts                   # 运行时加载 abi/
│   ├── contribution-recorder.ts # 模块1：组织 proof + EIP-712 签名
│   ├── x402-prover.ts           # 模块2：x402 支付层（待接 Cobo payment）
│   ├── executor.ts              # Cobo SDK 发交易（CAW 钱包当 executor）
│   ├── wallet-agent.ts          # 模块3：checkPending + claimFor
│   ├── mcp-server.ts            # 模块4：MCP 工具服务
│   └── index.ts                 # 入口：端到端串联
├── tools/                       # MCP 工具：sign/submit-contribution、check-pending、trigger-claim
├── abi/ContributionPool.abi.json
├── docs/{Agent方案设计.md, API.md}
├── .env / .env.example
├── package.json / tsconfig.json
```

## 现状

- ✅ 记录链路实测上链：`npm run dev` 跑通 sign → CAW recordContributionBySig（Sepolia）
- ✅ ABI / EIP-712 / 哈希规则 / proofSalt 全部对齐链上合约（链上实测一致）
- ✅ proof/signature HTTP API 可用（前端对接见 docs/API.md）
- ⏳ claimFor 分账：代码已接同机制，待 owner `finalizeRound` 后可实测
- ⏳ x402：待团队定演到多深（方案 3.3）

## 关键配置（已在 .env）

- `AGENT_PRIVATE_KEY`：agentSigner（链上 `agentSigner()` 对应私钥）
- `AGENT_WALLET_API_KEY` / `_WALLET_UUID`：CAW 钱包凭证
- `CAW_PACT_ID` / `CAW_SRC_ADDRESS`：发交易用的 pact 与 CAW 钱包地址
- `POOL_ADDRESS` / `USDC_ADDRESS` / `PROJECT_ID` / `ROUND_ID`：合约参数
