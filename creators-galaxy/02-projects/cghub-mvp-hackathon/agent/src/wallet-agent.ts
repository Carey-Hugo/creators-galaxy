/**
 * 模块 3：Cobo Agentic Wallet 调用
 * 封装 Cobo SDK：contractCall 调 claimFor 分账、payment 走 x402、读 pending、拉审计。
 * Pact/Policy 护栏流程照 03-caw-example/quickstart.ts。
 */

import { ethers } from 'ethers';
import {
  AuditApi,
  Configuration,
  PactsApi,
  TransactionsApi,
  type PactSpecInput,
} from '@cobo/agentic-wallet';
import { loadPoolAbi } from './abi.js';
import { config } from './config.js';
import type { X402Proof } from './types.js';

export class WalletAgent {
  private ownerCfg = new Configuration({ apiKey: config.cobo.apiKey, basePath: config.cobo.basePath });
  private pactsApi = new PactsApi(this.ownerCfg);
  private auditApi = new AuditApi(this.ownerCfg);
  private txApi?: TransactionsApi; // pact-scoped，ensurePactReady 后才有

  /**
   * 提交/复用 Pact，轮询到 active，建一个 pact-scoped 的 TransactionsApi。
   * TODO: Pact 复用（别每次都新提交）；Policy 阈值从配置读。
   */
  async ensurePactReady(): Promise<void> {
    const spec: PactSpecInput = {
      policies: [
        {
          name: 'cghub-distribute',
          type: 'transfer',
          rules: {
            effect: 'allow',
            when: { chain_in: [config.cobo.chainId] },
            // TODO: 分账上限阈值，按 Demo 资金量配
            deny_if: { amount_gt: '1000' },
          },
        },
      ],
      completion_conditions: [{ type: 'time_elapsed', threshold: '86400' }],
    };

    const resp = await this.pactsApi.submitPact({
      wallet_id: config.cobo.walletUuid,
      intent: 'CGHub Agent 贡献分账',
      spec,
    });
    const pactId = resp.data.result.pact_id;
    const apiKey = await this.waitForPactActive(pactId);
    this.txApi = new TransactionsApi(new Configuration({ apiKey, basePath: config.cobo.basePath }));
  }

  private async waitForPactActive(pactId: string): Promise<string> {
    const terminal = new Set(['rejected', 'expired', 'revoked', 'completed']);
    for (;;) {
      const pact = (await this.pactsApi.getPact(pactId)).data.result;
      const status = pact.status ?? '';
      if (status === 'active' && pact.api_key) return pact.api_key;
      if (terminal.has(status)) throw new Error(`Pact terminal status: ${status}`);
      await new Promise((r) => setTimeout(r, 5000));
    }
  }

  /** 读合约 pending()，判断有没有可领。走只读 RPC，不经 Cobo */
  async checkPending(contributor: string): Promise<bigint> {
    const provider = new ethers.JsonRpcProvider(config.chain.rpcUrl);
    const pool = new ethers.Contract(config.chain.poolAddress, loadPoolAbi(), provider);
    return pool.pending(config.round.projectId, config.round.roundId, contributor);
  }

  /**
   * pending>0 时走 Cobo contractCall 调 claimFor 代领。
   * 钱从 ContributionPool → contributor，调用方不碰钱。
   */
  async claimForContributor(contributor: string): Promise<{ txId: string; status: string }> {
    if (!this.txApi) throw new Error('先调 ensurePactReady()');

    const iface = new ethers.Interface(loadPoolAbi());
    const calldata = iface.encodeFunctionData('claimFor', [
      config.round.projectId,
      config.round.roundId,
      contributor,
    ]);

    const res = (
      await this.txApi.contractCall(config.cobo.walletUuid, {
        chain_id: config.cobo.chainId,
        contract_addr: config.chain.poolAddress,
        calldata,
        value: '0',
        sponsor: true, // Cobo Gasless 代付，Demo 不用自己备 gas
      })
    ).data.result as any;

    return { txId: res.id, status: res.status };
  }

  /** x402 支付层结算 */
  async payX402(challenge: string): Promise<X402Proof> {
    if (!this.txApi) throw new Error('先调 ensurePactReady()');
    const res = (
      await this.txApi.payment(config.cobo.walletUuid, {
        protocol: 'x402',
        x402_payment_required: challenge,
      })
    ).data.result as any;
    return { paymentId: res.id ?? '', status: res.status, retryHeaders: res.retry_headers };
  }

  /** 拉审计日志，Demo 展示用 */
  async getAuditTrail(limit = 20): Promise<unknown[]> {
    const logs = await this.auditApi.listAuditLogs(
      config.cobo.walletUuid,
      undefined, undefined, undefined, undefined,
      undefined, undefined, undefined, undefined,
      limit,
    );
    return (logs.data.result as any)?.items ?? [];
  }
}
