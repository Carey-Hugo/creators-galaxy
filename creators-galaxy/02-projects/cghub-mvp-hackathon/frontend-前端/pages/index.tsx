import { useEffect, useState } from "react";
import { ContributionForm } from "../components/ContributionForm";
import { WalletConnect } from "../components/WalletConnect";
import { DistributionView } from "../components/DistributionView";
import { useContributionPool } from "../hooks/useContributionPool";
import { useWallet } from "../hooks/useWallet";
import { useCoboWallet } from "../hooks/useCoboWallet";

interface ContributionItem {
  id: string;
  title: string;
  amount: string;
  description: string;
  status: "pending" | "submitted" | "distributed";
}

export default function Home() {
  const [contributions, setContributions] = useState<ContributionItem[]>([]);
  const [distributionResult, setDistributionResult] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  const {
    address,
    signer,
    chainId,
    shortAddress,
    isConnected,
    isLoading: walletLoading,
    error: walletError,
    connectWallet,
    disconnect,
  } = useWallet();
  const { isCoboReady, connectCoboWallet, requestDistribution } = useCoboWallet();
  const {
    round,
    score,
    claimed,
    pending,
    loading: contractLoading,
    error: contractError,
    refresh,
  } = useContributionPool(address, signer);

  useEffect(() => {
    const saved = window.localStorage.getItem("cghub-contributions");
    if (saved) {
      setContributions(JSON.parse(saved));
    }
  }, []);

  useEffect(() => {
    if (contributions.length > 0) {
      window.localStorage.setItem("cghub-contributions", JSON.stringify(contributions));
    }
  }, [contributions]);

  const handleSubmit = async (values: {
    title: string;
    amount: string;
    description: string;
  }) => {
    const newContribution: ContributionItem = {
      id: `${Date.now()}`,
      title: values.title,
      amount: values.amount,
      description: values.description,
      status: "pending",
    };

    setContributions((current) => [newContribution, ...current]);
    setMessage("贡献记录已保存。请先连接钱包并刷新链上状态。合约上链需要 Agent 返回 proof + signature。" );

    if (!isConnected) {
      await connectWallet();
    }

    if (!isCoboReady) {
      await connectCoboWallet();
    }
  };

  return (
    <main className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">CGHub MVP 黑客松</p>
          <h1>前端火堆：ContributionPool 合约对接</h1>
          <p>目标：读取 Sepolia 合约状态、展示我的分数/可领金额、并为 Agent 签名上链打基础。</p>
        </div>
        <WalletConnect
          address={address}
          isConnected={isConnected}
          isLoading={walletLoading}
          error={walletError}
          chainId={chainId}
          onConnect={connectWallet}
          onDisconnect={disconnect}
        />
      </header>

      <section className="panel">
        <div className="panel-header">
          <h2>贡献提交</h2>
          <p>填写贡献内容后，前端将记录本地状态并等待 Agent 返回 proof/signature 上链。</p>
        </div>
        <ContributionForm onSubmit={handleSubmit} />
      </section>

      <section className="panel grid-two">
        <div>
          <div className="panel-header">
            <h2>链上合约状态</h2>
          </div>
          <div className="status-box">
            <p>{message || "请连接钱包并刷新链上数据。"}</p>
            <p>合约读取：{contractLoading ? "加载中..." : contractError ? contractError : "正常"}</p>
            <p>当前钱包：{address ? shortAddress : "未连接"}</p>
            <p>当前分数：{score}</p>
            <p>已领取：{claimed}</p>
            <p>可领取：{pending}</p>
            <p>Round 是否存在：{round ? (round.exists ? "是" : "否") : "未知"}</p>
            <p>Round 是否 finalize：{round ? (round.finalized ? "已结束" : "未结束") : "未知"}</p>
            <button className="button secondary" onClick={refresh}>
              刷新链上数据
            </button>
          </div>
        </div>
        <DistributionView result={distributionResult} />
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>贡献记录</h2>
        </div>
        <div className="contribution-list">
          {contributions.length === 0 ? (
            <p>暂无贡献记录，提交后会在这里显示。</p>
          ) : (
            contributions.map((item) => (
              <article key={item.id} className="contribution-card">
                <h3>{item.title}</h3>
                <p>{item.description}</p>
                <p>金额：{item.amount}</p>
                <p>状态：{item.status}</p>
              </article>
            ))
          )}
        </div>
      </section>
    </main>
  );
}
