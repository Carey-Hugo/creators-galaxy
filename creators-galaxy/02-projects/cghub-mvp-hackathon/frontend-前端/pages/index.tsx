import { useEffect, useState } from "react";
import { ContributionForm } from "../components/ContributionForm";
import { WalletConnect } from "../components/WalletConnect";
import { DistributionView } from "../components/DistributionView";
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
  const { connectCoboWallet, isCoboReady, requestDistribution } = useCoboWallet();

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
    setMessage("贡献记录已保存，准备调用 Cobo SDK 发起分配。");

    if (!isCoboReady) {
      setMessage("正在初始化 Cobo Agentic Wallet，请先连接钱包。");
      await connectCoboWallet();
    }

    try {
      const distributionInfo = await requestDistribution({
        contributionId: newContribution.id,
        amount: values.amount,
        note: values.title,
      });
      setDistributionResult(distributionInfo);
      setContributions((current) =>
        current.map((item) =>
          item.id === newContribution.id
            ? { ...item, status: "distributed" }
            : item
        )
      );
      setMessage("已完成 Cobo 分账请求；请在 Cobo App 中确认 Pact 审批。" );
    } catch (error) {
      setMessage(
        "Cobo 分账请求失败。请检查 Cobo Agentic Wallet 登录状态或 SDK 配置。"
      );
    }
  };

  return (
    <main className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">CGHub MVP 黑客松</p>
          <h1>前端火堆：贡献记录 + Cobo Wallet 分账</h1>
          <p>目标：实现贡献提交、钱包连接、Cobo 分账触发、贡献和分配状态展示。</p>
        </div>
        <WalletConnect />
      </header>

      <section className="panel">
        <div className="panel-header">
          <h2>贡献提交</h2>
          <p>填写贡献内容并触发分账请求，走通 Demo 演示闭环。</p>
        </div>
        <ContributionForm onSubmit={handleSubmit} />
      </section>

      <section className="panel grid-two">
        <div>
          <div className="panel-header">
            <h2>当前进度</h2>
          </div>
          <div className="status-box">
            <p>{message || "请先连接钱包并提交一笔贡献。"}</p>
            <p>Cobo Wallet 状态：{isCoboReady ? "已准备" : "未准备"}</p>
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
