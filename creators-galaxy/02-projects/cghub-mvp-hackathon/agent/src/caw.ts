/**
 * caw CLI 封装：用 CAW 钱包发链上交易（在预建 pact 范围内）。
 * 钱包是 caw onboard 出来的 MPC/TSS 钱包，必须走 caw CLI 让本地 TSS 节点参与签名。
 * 前置：caw 已 onboard、CAW_PACT_ID 指向一个覆盖目标合约的 active pact。
 */

import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { config } from './config.js';

const exec = promisify(execFile);

/** 跑一条 caw 命令，解析 JSON（容忍前置噪声） */
async function caw(args: string[]): Promise<any> {
  const { stdout } = await exec(config.caw.bin, args, { maxBuffer: 16 * 1024 * 1024 });
  const start = stdout.indexOf('{');
  if (start < 0) throw new Error(`caw 无 JSON 输出: ${stdout.slice(0, 200)}`);
  return JSON.parse(stdout.slice(start));
}

/** caw tx call：发一笔合约调用，返回 txId + 初始状态 */
export async function cawTxCall(contract: string, calldata: string, requestId: string) {
  if (!config.caw.pactId) throw new Error('缺 CAW_PACT_ID，先建 pact');
  if (!config.caw.srcAddress) throw new Error('缺 CAW_SRC_ADDRESS（CAW 钱包地址）');
  const res = await caw([
    'tx', 'call',
    '--pact-id', config.caw.pactId,
    '--chain-id', config.caw.chainId,
    '--contract', contract,
    '--src-address', config.caw.srcAddress,
    '--calldata', calldata,
    '--request-id', requestId,
  ]);
  const r = res.result ?? res;
  if (res.success === false) throw new Error(`caw tx call 失败: ${res.message ?? JSON.stringify(res)}`);
  return { txId: r.id as string, status: r.status as string, requestId };
}

/** 轮询 caw tx get 直到上链确认，返回 tx hash */
export async function cawTxWait(txId: string, timeoutMs = 120_000): Promise<{ status: string; hash: string }> {
  const start = Date.now();
  for (;;) {
    const res = await caw(['tx', 'get', '--tx-id', txId]);
    const r = res.result ?? res;
    const status = r.status as string;
    if (status === 'Success') return { status, hash: r.transaction_hash as string };
    if (status === 'Failed' || status === 'Rejected') {
      throw new Error(`caw tx ${status}: ${r.sub_status ?? ''}`);
    }
    if (Date.now() - start > timeoutMs) throw new Error(`caw tx ${txId} 等待超时（最后状态 ${status}）`);
    await new Promise((res) => setTimeout(res, 5000));
  }
}
