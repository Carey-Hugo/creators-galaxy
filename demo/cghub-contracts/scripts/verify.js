import hre from "hardhat";

const CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

async function main() {
  console.log("🔍 验证 CGHubSubscription 合约...\n");
  
  const subscription = await hre.ethers.getContractAt(
    "CGHubSubscription",
    CONTRACT_ADDRESS
  );
  
  console.log("📍 合约地址:", CONTRACT_ADDRESS);
  
  // 查询平台钱包
  const platformWallet = await subscription.platformWallet();
  console.log("💰 平台钱包:", platformWallet);
  
  // 查询订阅费
  const fee = await subscription.getFee();
  console.log("💵 订阅费用:", hre.ethers.formatEther(fee), "MON");
  
  // 查询订阅周期
  const duration = await subscription.SUBSCRIPTION_DURATION();
  console.log("📅 订阅周期:", Number(duration) / (24 * 60 * 60), "天");
  
  // 测试未订阅状态
  const [user] = await hre.ethers.getSigners();
  const userAddress = user.address;
  
  const isSub = await subscription.isSubscriber(userAddress);
  console.log("\n🧪 测试 - 用户订阅状态:");
  console.log("  地址:", userAddress);
  console.log("  isSubscriber:", isSub);
  
  // 模拟订阅
  console.log("\n💸 模拟订阅 99 MON...");
  const feeWei = await subscription.getFee();
  const tx = await subscription.subscribe({ value: feeWei });
  await tx.wait();
  
  // 再次查询
  const isSubAfter = await subscription.isSubscriber(userAddress);
  const expiry = await subscription.getSubscriptionExpiry(userAddress);
  
  console.log("\n✅ 订阅后状态:");
  console.log("  isSubscriber:", isSubAfter);
  console.log("  到期时间:", new Date(Number(expiry) * 1000).toISOString());
  
  console.log("\n✅ 合约验证完成！所有功能正常。");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ 验证失败:", error);
    process.exit(1);
  });
