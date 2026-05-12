import hre from "hardhat";

async function main() {
  console.log("🚀 开始部署 CGHubSubscription 合约...\n");
  
  // 获取部署者账户
  const [deployer] = await hre.ethers.getSigners();
  console.log("📝 部署者地址:", deployer.address);
  
  // 平台钱包地址暂时用 deployer，正式环境替换为冷钱包
  const platformWallet = deployer.address;
  
  console.log("💰 平台收款地址:", platformWallet);
  console.log("📅 订阅费用: 99 MON");
  console.log("📅 订阅周期: 365 天\n");
  
  const Subscription = await hre.ethers.getContractFactory("CGHubSubscription");
  const subscription = await Subscription.deploy(platformWallet);
  
  // 等待合约部署完成
  await subscription.deployed();
  
  // 获取合约地址
  const contractAddress = subscription.address;
  
  console.log("✅ 部署成功！");
  console.log("📍 合约地址:", contractAddress);
  console.log("\n--- 验证信息 ---");
  console.log("🔍 Chain ID:", hre.network.config.chainId);
  console.log("🔍 Network:", hre.network.name);
  console.log("\n--- 下一步 ---");
  console.log("1. 将合约地址记录到 index.html");
  console.log("2. 在前端代码中替换 CONTRACT_ADDRESS");
  console.log("3. 打开 https://testnet.monad.xyz/faucet 领取测试币");
  console.log("4. 运行测试: npx hardhat run scripts/verify.js --network monadTestnet");
  
  // 保存部署信息
  const deploymentInfo = {
    network: hre.network.name,
    chainId: hre.network.config.chainId,
    contractAddress: contractAddress,
    deployer: deployer.address,
    subscriptionFee: "99 MON",
    subscriptionDuration: "365 days",
    timestamp: new Date().toISOString()
  };
  
  console.log("\n📦 部署信息 JSON:");
  console.log(JSON.stringify(deploymentInfo, null, 2));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ 部署失败:", error);
    process.exit(1);
  });
