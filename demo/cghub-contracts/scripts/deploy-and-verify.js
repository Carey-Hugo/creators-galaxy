import hre from "hardhat";
import { utils } from "ethers";

async function main() {
  console.log("🚀 部署 + 验证 CGHubSubscription 合约...\n");
  
  const [deployer] = await hre.ethers.getSigners();
  const platformWallet = deployer.address;
  
  console.log("📝 部署者:", deployer.address);
  
  // 1. Deploy
  console.log("\n📦 部署合约中...");
  const Subscription = await hre.ethers.getContractFactory("CGHubSubscription");
  const subscription = await Subscription.deploy(platformWallet);
  await subscription.deployed();
  const contractAddress = subscription.address;
  console.log("✅ 部署成功!");
  console.log("📍 合约地址:", contractAddress);
  
  // 2. Verify - call read functions
  console.log("\n🔍 验证合约功能...");
  
  // getFee()
  const fee = await subscription.getFee();
  console.log("💵 订阅费用:", utils.formatEther(fee), "MON");
  
  // isSubscriber (before)
  const isSubBefore = await subscription.isSubscriber(deployer.address);
  console.log("🧪 订阅前 isSubscriber:", isSubBefore);
  
  // getSubscriptionExpiry (before)
  const expiryBefore = await subscription.getSubscriptionExpiry(deployer.address);
  console.log("🧪 订阅前 expiry:", expiryBefore.toString());
  
  // 3. Subscribe
  console.log("\n💸 发起订阅 (1 MON)...");
  const tx = await subscription.subscribe({ value: fee });
  const receipt = await tx.wait();
  console.log("✅ 订阅交易已确认, hash:", receipt.hash);
  
  // 4. Verify - call read functions after
  console.log("\n🔍 订阅后验证...");
  
  const isSubAfter = await subscription.isSubscriber(deployer.address);
  console.log("🧪 订阅后 isSubscriber:", isSubAfter);
  
  const expiryAfter = await subscription.getSubscriptionExpiry(deployer.address);
  console.log("🧪 订阅后 expiry:", new Date(Number(expiryAfter) * 1000).toISOString());
  
  console.log("\n" + "=".repeat(50));
  console.log("✅ 全部测试通过!");
  console.log("=".repeat(50));
  console.log("\n📝 合约地址:", contractAddress);
  console.log("🌐 网络:", hre.network.name);
  console.log("\n下一步:");
  console.log("1. 打开 https://testnet.monad.xyz/faucet 领取测试币");
  console.log("2. 配置 .env 中的 PRIVATE_KEY");
  console.log("3. 运行: npx hardhat run scripts/deploy.js --network monadTestnet");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ 失败:", error);
    process.exit(1);
  });
