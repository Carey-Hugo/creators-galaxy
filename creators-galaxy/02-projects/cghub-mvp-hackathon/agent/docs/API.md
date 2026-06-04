# Agent HTTP API（给前端）

> 给前端火堆（老实人）对接。前端不碰链、不碰私钥、不碰 CAW 凭证，调下面这几个接口就行。
> 起服务：`npm run api`（默认 `http://localhost:8787`，改 `PORT` 环境变量）。已开 CORS。

## 接口

### 1. 签贡献（拿 proof + signature）

```
POST /api/sign-contribution
Content-Type: application/json

{
  "contributor": "0x贡献者地址",
  "score": 50,
  "source": "github",
  "evidenceId": "pr-123",
  "paymentId": "可选，不传自动生成"
}
```

返回：

```json
{
  "proof": {
    "projectId": "1", "roundId": "1", "contributor": "0x...",
    "score": "50", "proofHash": "0x...", "paymentIdHash": "0x...",
    "nonce": "...", "deadline": "..."
  },
  "signature": "0x...(65字节EIP-712签名)"
}
```

> proof 里的数字字段是字符串（避免 JSON 丢精度），上链前会还原成 uint256。
> 这步只用 agentSigner 私钥，不依赖 CAW。

### 2. 上链记录

```
POST /api/submit-contribution
{ "proof": {...上一步的proof...}, "signature": "0x..." }
```

返回：`{ "txHash": "0x..." }`

> 也可以前端不调这个、由我后端自动上链。看你方便，二选一。

### 3. 查可领金额

```
GET /api/pending?contributor=0x贡献者地址
```

返回：`{ "pending": "...", "score": "...", "claimed": "..." }`（单位是 USDC 最小单位）

### 4. 触发分账（Cobo 代领）

```
POST /api/trigger-claim
{ "contributor": "0x贡献者地址" }
```

返回：`{ "txId": "...", "status": "..." }`，无可领时返回 `{ "skipped": true, "reason": "..." }`

> 这步后端持 CAW 凭证、走 Cobo contractCall 调合约 claimFor。需要 Cobo 钱包已开通（见下）。

## 关于 CAW 凭证

CAW 的 API Key / pact key 是机密，**不下发前端**——claim/支付都走上面的接口，由后端持凭证执行。

前端若要展示钱包信息，我可以提供**非机密**的：Cobo 钱包地址 + wallet UUID + 链（Sepolia/SETH）。这些等 Cobo 钱包开通后给。

> ⏳ 待办：Cobo Agentic Wallet 还没开通（谁开、谁审批 Pact 待定）。开通前接口 1/2/3 能用（不依赖 CAW），接口 4 跑不了。
> 如果前端是想自己用 Cobo SDK 做"连接钱包/支付 UI"，那是另一回事——告诉我具体场景，我们对一下，因为 CAW 是服务端 agent 钱包，跟前端钱包连接不是一个东西。
