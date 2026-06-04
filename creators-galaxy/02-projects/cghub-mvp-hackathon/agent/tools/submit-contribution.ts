/**
 * MCP 工具：submit-contribution
 * 把签好的 (proof, signature) 上链，调 recordContributionBySig。
 * 这步要发交易、出 gas —— 执行方钱包是谁待定（方案第九节第 3 条）。
 */

import { ethers } from 'ethers';
import { z } from 'zod';
import { loadPoolAbi } from '../src/abi.js';
import { config } from '../src/config.js';
import type { ContributionProof } from '../src/types.js';

export const submitContributionTool = {
  name: 'submit-contribution',
  description: '把 Agent 签好的贡献 proof 上链（recordContributionBySig），发交易出 gas',
  inputSchema: {
    proof: z.record(z.string(), z.string()).describe('sign-contribution 产出的 proof'),
    signature: z.string().describe('EIP-712 签名'),
  },
  async handler(args: { proof: Record<string, string>; signature: string }) {
    // TODO: 执行方私钥来源待定（方案第九节第 3 条）
    const provider = new ethers.JsonRpcProvider(config.chain.rpcUrl);
    const executor = new ethers.Wallet(config.executorPrivateKey, provider);
    const pool = new ethers.Contract(config.chain.poolAddress, loadPoolAbi(), executor);

    // 字符串还原成合约要的类型
    const p = args.proof;
    const proof: ContributionProof = {
      projectId: BigInt(p.projectId),
      roundId: BigInt(p.roundId),
      contributor: p.contributor,
      score: BigInt(p.score),
      proofHash: p.proofHash,
      paymentIdHash: p.paymentIdHash,
      nonce: BigInt(p.nonce),
      deadline: BigInt(p.deadline),
    };

    const tx = await pool.recordContributionBySig(proof, args.signature);
    const receipt = await tx.wait();
    return { txHash: receipt.hash };
  },
};
