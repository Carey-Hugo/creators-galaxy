import hre from "hardhat";

const CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

async function main() {
  const provider = hre.ethers.provider;
  
  // Check if contract code exists at address
  const code = await provider.getCode(CONTRACT_ADDRESS);
  console.log("Contract code at address:", code.length, "chars");
  console.log("First 100 chars:", code.substring(0, 100));
  
  if (code === "0x") {
    console.log("\n❌ NO CONTRACT FOUND at this address!");
  } else {
    console.log("\n✅ Contract exists");
  }
}

main().then(() => process.exit(0)).catch(console.error);
