// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title CGHubSubscription
 * @notice 创客星球订阅合约 - 部署在 Monad 测试网
 * @dev 订阅费 1 MON，订阅周期 1 年
 */
contract CGHubSubscription {
    // ============================================
    // State Variables
    // ============================================
    
    /// 订阅费用：1 MON (转换为 wei)
    uint256 public constant SUBSCRIPTION_FEE = 1 * 10**18;
    
    /// 订阅周期：365 天 (秒)
    uint256 public constant SUBSCRIPTION_DURATION = 365 days;
    
    /// 平台钱包地址（接收订阅费）
    address public immutable platformWallet;
    
    /// 用户订阅信息：address => 到期时间戳
    mapping(address => uint256) public subscriptions;
    
    // ============================================
    // Events
    // ============================================
    
    event Subscribed(address indexed user, uint256 startTime, uint256 endTime, uint256 amount);
    event SubscriptionExtended(address indexed user, uint256 newEndTime);
    
    // ============================================
    // Errors
    // ============================================
    
    error InsufficientPayment();
    error TransferFailed();
    
    // ============================================
    // Constructor
    // ============================================
    
    constructor(address _platformWallet) {
        require(_platformWallet != address(0), "Invalid wallet address");
        platformWallet = _platformWallet;
    }
    
    // ============================================
    // Main Functions
    // ============================================
    
    /**
     * @notice 订阅（一次性付费 1 MON）
     * @dev 如果已订阅，自动续期
     */
    function subscribe() external payable {
        if (msg.value < SUBSCRIPTION_FEE) {
            revert InsufficientPayment();
        }
        
        uint256 currentExpiry = subscriptions[msg.sender];
        uint256 newExpiry;
        
        if (currentExpiry > block.timestamp) {
            // 已订阅：追加时间
            newExpiry = currentExpiry + SUBSCRIPTION_DURATION;
        } else {
            // 未订阅或已过期：从现在开始计时
            newExpiry = block.timestamp + SUBSCRIPTION_DURATION;
        }
        
        subscriptions[msg.sender] = newExpiry;
        
        // 转账给平台钱包
        (bool success, ) = platformWallet.call{value: msg.value}("");
        if (!success) {
            revert TransferFailed();
        }
        
        emit Subscribed(msg.sender, block.timestamp, newExpiry, msg.value);
    }
    
    /**
     * @notice 查询用户是否在有效订阅期内
     * @param user 用户地址
     * @return bool 是否有效订阅
     */
    function isSubscriber(address user) external view returns (bool) {
        return subscriptions[user] > block.timestamp;
    }
    
    /**
     * @notice 查询用户订阅到期时间
     * @param user 用户地址
     * @return uint256 到期时间戳（0 = 从未订阅）
     */
    function getSubscriptionExpiry(address user) external view returns (uint256) {
        if (subscriptions[user] > block.timestamp) {
            return subscriptions[user];
        }
        return 0;
    }
    
    /**
     * @notice 查询当前订阅费率
     * @return uint256 费用（wei）
     */
    function getFee() external pure returns (uint256) {
        return SUBSCRIPTION_FEE;
    }
    
    // ============================================
    // Admin Functions (for future upgrade)
    // ============================================
    
    /// 允许合约接收 ETH（用于退款等场景）
    receive() external payable {}
}
