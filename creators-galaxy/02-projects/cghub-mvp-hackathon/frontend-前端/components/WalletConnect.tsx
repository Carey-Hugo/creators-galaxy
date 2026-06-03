import { useEffect, useMemo, useState } from "react";
import { ethers } from "ethers";

export function WalletConnect() {
  const [address, setAddress] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const shortAddress = useMemo(() => {
    if (!address) return "";
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  }, [address]);

  useEffect(() => {
    if (error) {
      console.warn("钱包连接错误", error);
    }
  }, [error]);

  const connectWallet = async () => {
    setError(null);
    if (typeof window === "undefined") {
      setError("未检测到浏览器环境。请在浏览器中打开该页面。");
      return;
    }

    const anyWindow = window as any;
    if (!anyWindow.ethereum) {
      setError("未检测到浏览器钱包。请安装 MetaMask 或 Cobo Agentic Wallet 扩展。");
      return;
    }

    setIsLoading(true);
    try {
      const provider = new ethers.BrowserProvider(anyWindow.ethereum);
      await provider.send("eth_requestAccounts", []);
      const signer = await provider.getSigner();
      const connectedAddress = await signer.getAddress();
      setAddress(connectedAddress);
      setIsConnected(true);
    } catch (connectError) {
      setError("钱包连接失败，请检查钱包并重试。");
      console.error(connectError);
    } finally {
      setIsLoading(false);
    }
  };

  const disconnect = () => {
    setIsConnected(false);
    setAddress(null);
  };

  return (
    <div className="wallet-panel">
      {isConnected ? (
        <>
          <div>
            <p>已连接钱包</p>
            <strong>{shortAddress}</strong>
          </div>
          <button className="button secondary" onClick={disconnect}>
            断开连接
          </button>
        </>
      ) : (
        <>
          <button className="button primary" disabled={isLoading} onClick={connectWallet}>
            连接 MetaMask
          </button>
          <p className="hint">如果你有 Cobo Agentic Wallet，请在浏览器中打开并授权。</p>
          {error ? <p className="hint">{error}</p> : null}
        </>
      )}
    </div>
  );
}
