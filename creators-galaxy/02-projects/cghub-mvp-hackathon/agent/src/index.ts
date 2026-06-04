/**
 * 入口：把 4 块串起来跑端到端，用于自测和 Demo 录屏（不依赖 MCP 客户端）。
 *
 * 全流程（前提：owner 已 createRound + fundRound）：
 *   1. sign  : Agent 签贡献 proof
 *   2. submit: 执行方上链 recordContributionBySig
 *   3.（owner finalizeRound —— 不在本脚本，白织/手动）
 *   4. claim : pending>0 → Cobo contractCall claimFor 分账
 *
 * TODO: 跑通前要先配好 .env（私钥、RPC、Cobo key）+ 白织给完整 ABI。
 */

import { recordContribution } from './contribution-recorder.js';
import { newPaymentId } from './x402-prover.js';
import { WalletAgent } from './wallet-agent.js';
import type { ContributionInput } from './types.js';

async function main() {
  const demoContributor = '0x1111111111111111111111111111111111111111'; // TODO 换成真实贡献者

  // 1. 签贡献
  const input: ContributionInput = {
    contributor: demoContributor,
    score: 50,
    source: 'github',
    evidenceId: 'pr-123',
    paymentId: newPaymentId(),
  };
  const signed = await recordContribution(input);
  console.log('[1] 已签名 proof：', signed.proof.proofHash);

  // 2. 上链（最小骨架，真实上链见 tools/submit-contribution.ts）
  console.log('[2] TODO: 调 submit-contribution 上链 recordContributionBySig');

  // 3. finalize 由 owner 做，跳过
  console.log('[3] 等 owner finalizeRound（不在本脚本）');

  // 4. 分账
  const agent = new WalletAgent();
  const pending = await agent.checkPending(demoContributor);
  console.log('[4] pending =', pending.toString());
  if (pending > 0n) {
    await agent.ensurePactReady();
    const res = await agent.claimForContributor(demoContributor);
    console.log('[4] claimFor 已提交：', res);
  }
}

main().catch((e) => {
  console.error('端到端失败：', e);
  process.exit(1);
});
