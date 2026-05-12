import hre from "hardhat";

const CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

async function main() {
  const subscription = await hre.ethers.getContractAt(
    "CGHubSubscription",
    CONTRACT_ADDRESS
  );
  
  console.log("Testing getFee()...");
  try {
    const fee = await subscription.getFee();
    console.log("Fee:", hre.ethers.formatEther(fee), "MON");
  } catch(e) {
    console.log("getFee failed:", e.message);
  }
  
  console.log("\nTesting isSubscriber()...");
  try {
    const [user] = await hre.ethers.getSigners();
    const isSub = await subscription.isSubscriber(user.address);
    console.log("isSubscriber:", isSub);
  } catch(e) {
    console.log("isSubscriber failed:", e.message);
  }
}

main().then(() => process.exit(0)).catch(console.error);
