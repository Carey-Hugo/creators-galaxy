/**
 * 模块 2：x402 证明生成
 * 走 Cobo 原生 payment(x402) 做支付层结算，不自己实现 facilitator。
 * 产出的 paymentId 会被 contribution-recorder 哈希进 paymentIdHash 做对账。
 *
 * 说明：x402 在闭环里是"支付层"那一环，分账主线本身走 claimFor（见 wallet-agent）。
 * x402 演到多深待团队拍（方案 3.3），这里给最小骨架。
 */

import type { X402Proof } from './types.js';
import type { WalletAgent } from './wallet-agent.js';

/**
 * 拿一个 x402-enabled 端点的 402 挑战，丢给 Cobo 结算。
 * @param challenge Base64 编码的 Payment-Required 挑战（来自 402 响应头）
 *
 * TODO:
 *  1. 需要一个 x402-enabled 端点；MVP 可以自己起个最小服务返回 402，或用现成 demo 端点
 *  2. 挑战的获取流程（fetch → 402 → 取头）这里先省略，等端点定了再补
 */
export async function generateX402Proof(
  walletAgent: WalletAgent,
  challenge: string,
): Promise<X402Proof> {
  const result = await walletAgent.payX402(challenge);
  return result;
}

/** 生成业务支付 id（进 paymentIdHash）。最小实现，先用时间戳串 */
export function newPaymentId(prefix = 'pay'): string {
  const d = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  return `${prefix}-${d}-${Math.random().toString(36).slice(2, 8)}`;
}
