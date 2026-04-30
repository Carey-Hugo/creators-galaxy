# CGHub 去中心化代码仓库技术方案

> 版本：V1.0  
> 状态：详细技术设计  
> 定位：去中心化代码仓库 + 贡献确权 + 智能合约分润  
> 集成：与创客星球积分体系、DAO治理打通

---

## 一、架构总览

### 1.1 设计目标

```
┌─────────────────────────────────────────────────────────────────┐
│                        CGHub 技术架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   用户层 ──▶ DApp (Web/Mobile) ──▶ API Gateway                 │
│                                           │                     │
│   区块链层 ◀── Smart Contracts ◀── Layer2 结算网络              │
│       │                                    │                     │
│   存储层 ◀── IPFS/Filecoin ◀── 代码片段分片存储                  │
│       │                                                       │
│   索引层 ◀── Graph Node ◀── 事件监听 ──▶ 贡献追踪引擎            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 核心设计原则

| 原则 | 说明 |
|------|------|
| **去中心化** | 代码存储在IPFS上，智能合约控制权限，无单点故障 |
| **贡献即确权** | 每次commit/push/PR都会被签名并记录到链上 |
| **规则即代码** | 分润规则通过智能合约执行，不可篡改 |
| **可插拔存储** | 支持IPFS/Arweave/Filecoin等去中心化存储方案 |
| **兼容Git** | 核心协议兼容Git，支持现有开发者工具 |

---

## 二、存储层设计

### 2.1 去中心化代码存储

```solidity
// 核心存储接口
interface ICodeStorage {
    // 存储代码片段
    function storeCode(bytes32 contentHash, string calldata filePath) external;
    
    // 获取代码片段
    function retrieveCode(bytes32 contentHash) external view returns (bytes memory);
    
    // 获取仓库CID
    function getRepoCID(address repoOwner, string calldata repoName) external view returns (bytes32);
}
```

### 2.2 存储架构

```
┌─────────────────────────────────────────────────────────────┐
│                    CGHub 存储层                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   IPFS      │    │  Arweave    │    │  Filecoin   │     │
│  │ (主存储)     │    │ (备份)      │    │ (冷存储)    │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            ▼                                 │
│                   ┌─────────────────┐                        │
│                   │   存储编排层     │                        │
│                   │ StorageOrchestrator│                      │
│                   └────────┬────────┘                        │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐             │
│         ▼                  ▼                  ▼             │
│   ┌──────────┐       ┌──────────┐       ┌──────────┐       │
│   │ RepoMeta │       │ CommitLog│       │ DiffData │       │
│   │ (链上)   │       │ (链上)   │       │ (链下)   │       │
│   └──────────┘       └──────────┘       └──────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 仓库元数据结构

```solidity
// 仓库元数据合约
contract RepoRegistry {
    struct Repository {
        address owner;              // 仓库所有者
        bytes32 ipfsCID;            // 最新代码的IPFS CID
        uint256 totalCommits;       // 总提交数
        uint256 totalContributors;  // 总贡献者数
        uint256 createdAt;          // 创建时间
        uint256 updatedAt;          // 更新时间
        RepoVisibility visibility;  // 可见性
    }
    
    enum RepoVisibility { 
        Public,      // 完全公开
        Protected,   // 仅贡献者可见
        Private      // 仅白名单可见
    }
    
    // 仓库创建事件
    event RepoCreated(
        address indexed owner,
        string name,
        bytes32 indexed repoCID,
        uint256 timestamp
    );
    
    // 贡献者添加事件
    event ContributorAdded(
        address indexed repoAddress,
        address indexed contributor,
        uint256 sharePercent
    );
}
```

---

## 三、贡献确权系统

### 3.1 贡献类型定义

```solidity
// 贡献类型枚举
enum ContributionType {
    Commit,           // 代码提交
    PullRequest,      // PR合并
    IssueOpened,      // 发起Issue
    IssueComment,     // Issue评论
    CodeReview,       // 代码审查
    Documentation,    // 文档贡献
    BugReport,       // Bug报告
    TestContribution // 测试贡献
}

// 贡献记录结构
struct Contribution {
    uint256 id;
    address contributor;
    bytes32 repoHash;           // 仓库标识
    ContributionType type;
    uint256 weight;             // 权重（根据类型不同）
    string commitHash;          // Git commit hash
    uint256 timestamp;
    string metadataCID;         // 详细内容的IPFS CID
}
```

### 3.2 贡献权重矩阵

| 贡献类型 | 基础权重 | 说明 |
|---------|---------|------|
| Commit | 10 | 核心代码提交 |
| PullRequest (Merged) | 30 | PR被合并 |
| CodeReview | 15 | 代码审查通过 |
| IssueOpened | 5 | 有效Issue |
| IssueComment | 2 | 有价值的讨论 |
| BugReport (Verified) | 20 | 确认的Bug |
| Documentation | 8 | 文档改进 |
| TestContribution | 12 | 测试用例 |

### 3.3 贡献签名与验证

```solidity
// 贡献确权合约
contract ContributionRegistry {
    
    // 贡献记录
    mapping(bytes32 => Contribution) public contributions;
    
    // 仓库贡献者列表
    mapping(bytes32 => address[]) public repoContributors;
    
    // 贡献者权重
    mapping(bytes32 => mapping(address => uint256)) public contributorWeight;
    
    // 签名消息前缀
    bytes32 public constant SIGNING_PREFIX = keccak256(
        "CGHub Contribution Protocol"
    );
    
    // 记录贡献
    function recordContribution(
        address contributor,
        bytes32 repoHash,
        ContributionType ct,
        string calldata commitHash,
        string calldata metadataCID
    ) external returns (uint256) {
        // 验证签名（确保是贡献者本人签名）
        bytes32 contributionHash = keccak256(
            abi.encodePacked(
                SIGNING_PREFIX,
                contributor,
                repoHash,
                ct,
                commitHash,
                block.timestamp
            )
        );
        
        // 创建贡献记录
        uint256 contributionId = contributionsCount[repoHash]++;
        Contribution storage c = contributions[contributionHash];
        c = Contribution({
            id: contributionId,
            contributor: contributor,
            repoHash: repoHash,
            type: ct,
            weight: getWeight(ct),
            commitHash: commitHash,
            timestamp: block.timestamp,
            metadataCID: metadataCID
        });
        
        // 更新贡献者权重
        contributorWeight[repoHash][contributor] += c.weight;
        
        // 触发事件
        emit ContributionRecorded(
            contributionId,
            contributor,
            repoHash,
            ct,
            c.weight
        );
        
        return contributionId;
    }
    
    // 获取贡献者权重
    function getContributorWeight(
        bytes32 repoHash, 
        address contributor
    ) external view returns (uint256) {
        return contributorWeight[repoHash][contributor];
    }
}
```

### 3.4 链上贡献签名流程

```
┌──────────────────────────────────────────────────────────────────┐
│                    贡献确权流程                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. 开发者本地签名                                                │
│     ├── 计算 commit hash                                         │
│     ├── 使用私钥对贡献信息签名                                    │
│     └── 生成 signed message                                      │
│              │                                                  │
│              ▼                                                  │
│  2. 提交到 CGHub 节点                                            │
│     ├── 节点验证签名                                             │
│     ├── 节点计算权重                                             │
│     └── 节点调用合约记录贡献                                      │
│              │                                                  │
│              ▼                                                  │
│  3. 合约处理                                                     │
│     ├── 验证贡献者身份                                           │
│     ├── 记录贡献到 contributions mapping                         │
│     ├── 更新 contributorWeight                                    │
│     └── 触发 ContributionRecorded 事件                           │
│              │                                                  │
│              ▼                                                  │
│  4. 索引层同步                                                   │
│     ├── Graph Node 监听事件                                      │
│     ├── 更新贡献者排名                                           │
│     └── 更新仓库贡献图谱                                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 四、智能合约分润系统

### 4.1 分润合约架构

```solidity
// 分润池合约
contract ProfitSharingPool {
    
    // 仓库分润配置
    struct RepoSharingConfig {
        address repoAddress;        // 仓库地址
        uint256 totalShares;        // 总份额
        uint256 releaseSchedule;    // 释放计划（天数）
        uint256 startTime;          // 开始时间
        mapping(address => uint256) shares;  // 各贡献者份额
    }
    
    // 分润池
    struct SharePool {
        address token;              // 分润代币地址
        uint256 totalAmount;        // 总金额
        uint256 releasedAmount;     // 已释放金额
        mapping(address => uint256) claimed; // 已领取金额
    }
    
    // 创建分润池
    function createSharePool(
        address repoAddress,
        address[] calldata contributors,
        uint256[] calldata weights
    ) external {
        require(contributors.length == weights.length);
        
        uint256 totalWeight = 0;
        for (uint i = 0; i < weights.length; i++) {
            totalWeight += weights[i];
        }
        
        RepoSharingConfig storage config = repoConfigs[repoAddress];
        config.repoAddress = repoAddress;
        config.totalShares = totalWeight;
        config.startTime = block.timestamp;
        
        // 按权重计算份额
        for (uint i = 0; i < contributors.length; i++) {
            uint256 share = (weights[i] * 10000) / totalWeight; // 百分比 * 100
            config.shares[contributors[i]] = share;
        }
        
        emit SharePoolCreated(repoAddress, contributors.length);
    }
    
    // 释放分润（由合约自动执行或DAO投票触发）
    function releaseProfits(
        address repoAddress,
        address token,
        uint256 amount
    ) external onlyDAO {
        SharePool storage pool = pools[repoAddress][token];
        pool.totalAmount += amount;
        
        emit ProfitsDeposited(repoAddress, token, amount);
    }
    
    // 领取分润
    function claimProfits(
        address repoAddress,
        address token
    ) external {
        RepoSharingConfig storage config = repoConfigs[repoAddress];
        uint256 share = config.shares[msg.sender];
        require(share > 0, "Not a contributor");
        
        SharePool storage pool = pools[repoAddress][token];
        uint256 totalShare = (pool.totalAmount * share) / 10000;
        uint256 claimable = totalShare - pool.claimed[msg.sender];
        
        require(claimable > 0, "Nothing to claim");
        
        pool.claimed[msg.sender] += claimable;
        IERC20(token).transfer(msg.sender, claimable);
        
        emit ProfitsClaimed(msg.sender, repoAddress, token, claimable);
    }
}
```

### 4.2 分润规则引擎

```solidity
// 分润规则引擎
contract SharingRulesEngine {
    
    // 规则类型
    enum RuleType {
        FixedRatio,      // 固定比例
        WeightedScore,   // 加权评分
        TimeLocked,      // 时间锁释放
        MilestoneBased   // 里程碑触发
    }
    
    // 分润规则
    struct SharingRule {
        RuleType ruleType;
        uint256[] parameters;      // 根据ruleType不同，参数意义不同
        uint256 createdAt;
        address createdBy;
    }
    
    // 默认规则参数
    // FixedRatio: [contributorShare, daoShare, platformShare]
    // WeightedScore: [baseWeight, contributionTypes...]
    // TimeLocked: [vestingDuration, cliffPeriod, releasePercentage]
    // MilestoneBased: [milestoneIds..., triggerPercentages...]
    
    // 创建分润规则
    function createRule(
        bytes32 repoHash,
        RuleType ruleType,
        uint256[] calldata parameters
    ) external returns (bytes32 ruleHash) {
        // 规则需要DAO批准
        require(isDAO[msg.sender], "Only DAO can create rules");
        
        ruleHash = keccak256(abi.encodePacked(
            repoHash,
            ruleType,
            parameters,
            block.timestamp
        ));
        
        rules[repoHash] = SharingRule({
            ruleType: ruleType,
            parameters: parameters,
            createdAt: block.timestamp,
            createdBy: msg.sender
        });
        
        emit RuleCreated(repoHash, ruleHash, ruleType);
    }
    
    // 计算分润
    function calculateShares(
        bytes32 repoHash,
        address[] calldata contributors,
        uint256 totalAmount
    ) external view returns (uint256[] memory shares) {
        SharingRule storage rule = rules[repoHash];
        shares = new uint256[](contributors.length);
        
        if (rule.ruleType == RuleType.WeightedScore) {
            // 加权评分模式
            uint256[] memory weights = new uint256[](contributors.length);
            uint256 totalWeight = 0;
            
            for (uint i = 0; i < contributors.length; i++) {
                weights[i] = contributionRegistry.getContributorWeight(
                    repoHash, 
                    contributors[i]
                );
                totalWeight += weights[i];
            }
            
            for (uint i = 0; i < contributors.length; i++) {
                shares[i] = (totalAmount * weights[i]) / totalWeight;
            }
        }
        // ... 其他规则类型实现
    }
}
```

### 4.3 分润流程图

```
┌──────────────────────────────────────────────────────────────────┐
│                    智能合约分润流程                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  阶段1: 收益归集                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │  产品收入   │    │  商业授权   │    │   其他收入  │          │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘          │
│         └──────────────────┼──────────────────┘                 │
│                            ▼                                      │
│                   ┌─────────────────┐                            │
│                   │   收益归集合约   │                            │
│                   │ RevenueCollector │                            │
│                   └────────┬────────┘                            │
│                            │                                      │
│  阶段2: 规则执行                                                  │
│                            ▼                                      │
│                   ┌─────────────────┐                            │
│                   │  分润规则引擎    │                            │
│                   │ SharingRulesEng │                            │
│                   └────────┬────────┘                            │
│                            │                                      │
│         ┌──────────────────┼──────────────────┐                  │
│         ▼                  ▼                  ▼                  │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐             │
│  │ 贡献者  │       │   DAO   │       │  平台   │             │
│  │  份额   │       │   份额   │       │   份额   │             │
│  └────┬────┘       └────┬────┘       └────┬────┘             │
│       │                  │                  │                   │
│  阶段3: 释放与领取                                            │
│       │                  │                  │                   │
│       ▼                  ▼                  ▼                   │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐           │
│  │ 按规则   │       │  按规则   │       │ 按规则   │            │
│  │ 线性释放 │       │  投票解锁 │       │  锁定    │            │
│  └────┬────┘       └────┬────┘       └────┬────┘            │
│       │                  │                  │                   │
│       └──────────────────┼──────────────────┘                 │
│                            ▼                                      │
│                   ┌─────────────────┐                            │
│                   │  用户领取代币    │                            │
│                   │ claimProfits()  │                            │
│                   └─────────────────┘                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 五、与创客星球积分体系集成

### 5.1 双代币集成

```solidity
// CGHub 与 MKT/STAR 集成接口
interface ITokenIntegration {
    
    // MKT 功能代币使用场景
    // - 购买高级功能
    // - 解锁私有仓库
    // - 支付高级服务
    
    // STAR 治理代币使用场景
    // - DAO投票权重
    // - 重要参数修改
    // - 规则制定
    
    // 贡献奖励 MKT
    function rewardContribution(
        address contributor,
        uint256 amount,
        bytes32 repoHash
    ) external {
        // 从平台池转出 MKT 给贡献者
        MKT.transfer(
            contributor, 
            calculateReward(msg.sender, amount)
        );
        
        // 触发贡献奖励事件
        emit ContributionRewarded(
            contributor, 
            repoHash, 
            amount
        );
    }
    
    // 锁定 STAR 用于治理
    function lockSTARForGovernance(
        address user,
        uint256 amount,
        uint256 duration
    ) external returns (uint256 votingPower) {
        // 转移 STAR 到锁仓合约
        STAR.transferFrom(user, starLockingContract, amount);
        
        // 计算投票权（时间加成）
        votingPower = amount * (1 + duration / 365 days);
        
        emit STARLocked(user, amount, votingPower);
    }
}
```

### 5.2 积分获取规则

| 操作 | 获得积分 | 积分类型 |
|------|---------|---------|
| 创建公开仓库 | 100 | MKT |
| 每提交一次Commit | 10 | MKT |
| PR被合并 | 30 | MKT + 5 STAR |
| CodeReview通过 | 15 | MKT |
| 有效Issue | 5 | MKT |
| Bug报告被确认 | 20 | MKT + 3 STAR |
| 获得他人捐赠 | 全额 | MKT |

### 5.3 积分消耗规则

| 操作 | 消耗积分 | 积分类型 |
|------|---------|---------|
| 创建私有仓库 | 500/月 | MKT |
| 使用高级CI/CD | 100/次 | MKT |
| 紧急技术支持 | 200/次 | MKT |
| DAO提案押金 | 1000 | STAR |
| 提案辩论期加速 | 500 | STAR |

---

## 六、DAO治理集成

### 6.1 治理合约架构

```solidity
// CGHub DAO 治理合约
contract CGHubDAO {
    
    // 治理参数
    uint256 public constant VOTING_PERIOD = 7 days;
    uint256 public constant PROPOSAL_THRESHOLD = 1000e18; // 1000 STAR
    uint256 public constant QUORUM = 0.2e18; // 20% 法定人数
    
    // 提案状态
    enum ProposalState {
        Pending,
        Active,
        Queued,
        Executed,
        Failed,
        Canceled
    }
    
    // 提案结构
    struct Proposal {
        uint256 id;
        address proposer;
        bytes32 repoHash;           // 关联的仓库（如果是仓库相关提案）
        Target[] targets;           // 调用的目标合约
        uint256[] values;           // 调用时发送的ETH值
        bytes[] calldatas;          // 调用数据
        uint256 startTime;
        uint256 endTime;
        uint256 forVotes;
        uint256 againstVotes;
        bool executed;
        bool canceled;
    }
    
    // 提案可执行的操作类型
    enum ActionType {
        UpdateSharingRule,     // 更新分润规则
        AddContributor,        // 添加贡献者
        RemoveContributor,     // 移除贡献者
        UpdateRewardRate,      // 更新奖励 rate
        UpgradeContract,       // 升级合约
        PauseRepo,             // 暂停仓库
        ChangeVisibility      // 修改可见性
    }
    
    // 提案结构
    struct Target {
        address target;
        ActionType actionType;
        bytes params;
    }
}
```

### 6.2 治理流程

```
┌──────────────────────────────────────────────────────────────────┐
│                        DAO 治理流程                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  阶段1: 提案创建                                                  │
│  ├── 任何人锁定 1000 STAR 发起提案                                │
│  ├── 提案内容：修改哪个仓库的哪个规则                              │
│  └── 提案进入 Pending 状态                                        │
│              │                                                    │
│              ▼                                                    │
│  阶段2: 社区讨论                                                  │
│  ├── 7 天讨论期                                                   │
│  ├── 在论坛/社交媒体讨论提案内容                                  │
│  └── 可以修改提案细节                                             │
│              │                                                    │
│              ▼                                                    │
│  阶段3: 投票                                                      │
│  ├── STAR 持有者 1 STAR = 1 票                                   │
│  ├── 投票可以投 赞成/反对/弃权                                    │
│  ├── 需要 >50% 赞成票且 quorum 达到才算通过                       │
│  └── 投票期 3 天                                                 │
│              │                                                    │
│              ▼                                                    │
│  阶段4: 执行                                                      │
│  ├── 通过后 2 天 timelock 延迟                                    │
│  ├── 自动执行合约调用                                             │
│  └── 如果是规则变更，自动更新分润规则                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 6.3 治理场景示例

| 场景 | 提案内容 | 所需票数 |
|------|---------|---------|
| 修改仓库分润比例 | 从 8:2 改为 9:1（贡献者:DAO） | >50% 赞成，quorum=20% |
| 添加贡献者 | 将新贡献者加入分润池 | >50% 赞成，quorum=20% |
| 紧急暂停仓库 | 因安全原因暂停某仓库 | >60% 赞成，quorum=30% |
| 合约升级 | 升级到新版本合约 | >66% 赞成，quorum=40% |
| 规则重置 | 重置某仓库的分润规则 | >75% 赞成，quorum=50% |

---

## 七、技术栈选型

### 7.1 区块链层

| 组件 | 选择 | 理由 |
|------|------|------|
| L1 区块链 | Ethereum/Polygon/BNB Chain | 生态成熟，安全可靠 |
| L2 扩容 | Polygon PoS / Arbitrum | 低 gas，快的确认 |
| 智能合约语言 | Solidity 0.8+ | 成熟生态，EVM兼容 |
| 开发框架 | Hardhat + OpenZeppelin | 安全标准，可升级模式 |

### 7.2 存储层

| 组件 | 选择 | 理由 |
|------|------|------|
| 代码存储 | IPFS + Filecoin | 去中心化，成熟稳定 |
| 元数据存储 | Arweave | 永久存储，低廉 |
| 索引服务 | The Graph | 高效查询，事件索引 |
| CDN | Pinata / Infura | IPFS pinning 服务 |

### 7.3 应用层

| 组件 | 选择 | 理由 |
|------|------|------|
| 后端框架 | Node.js / Go | 高性能，团队熟悉 |
| API | GraphQL + REST | 灵活查询，与前端解耦 |
| 前端框架 | React / Next.js | 成熟生态，SSR支持 |
| 钱包连接 | WalletConnect | 跨平台支持好 |
| Git 操作 | isomorphic-git | 纯 JS Git 实现 |

### 7.4 基础设施

| 组件 | 选择 | 理由 |
|------|------|------|
| 节点服务 | Alchemy / Infura | 可靠的 RPC |
| 监控 | The Graph + Dune Analytics | 链上数据分析 |
| CI/CD | GitHub Actions + IPFS uploading | 自动化部署 |
| DID | ENS + 创客星球DID | 去中心化身份 |

---

## 八、安全设计

### 8.1 合约安全措施

```solidity
// 安全修饰符
modifier onlyDAO() {
    require(isDAO[msg.sender], "Not authorized");
    _;
}

modifier nonReentrant() {
    _reentrancyGuard = 1;
    _;
    _reentrancyGuard = 0;
}

// 权限分级
contract AccessControl {
    // 角色定义
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant MANAGER_ROLE = keccak256("MANAGER_ROLE");
    bytes32 public constant CONTRIBUTOR_ROLE = keccak256("CONTRIBUTOR_ROLE");
    
    // 多签管理
    mapping(bytes32 => address[]) public multiSigApprovers;
    mapping(bytes32 => uint256) public requiredApprovals;
}
```

### 8.2 安全检查清单

| 检查项 | 说明 |
|-------|------|
| 溢出检查 | 使用 Solidity 0.8+ 自动溢出检查 |
| 重入保护 | 检查effects-interactions模式 |
| 权限控制 | 关键操作需要多签或DAO批准 |
| 紧急暂停 | 合约支持紧急暂停功能 |
| 存款限额 | 单笔存款有上限 |
| 速率限制 | 操作频率限制 |
| 审计 | 上线前完成第三方审计 |

---

## 九、核心合约部署图

```
┌──────────────────────────────────────────────────────────────────┐
│                    CGHub 核心合约部署                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 2 (Polygon/Arbitrum)                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌────────────────┐   ┌────────────────┐                │   │
│  │  │ RepoRegistry   │   │ ContributionReg │                │   │
│  │  │ (仓库注册)     │   │ (贡献记录)       │                │   │
│  │  └───────┬────────┘   └───────┬────────┘                │   │
│  │          │                    │                         │   │
│  │          └────────┬───────────┘                         │   │
│  │                   ▼                                      │   │
│  │  ┌────────────────────────────────┐                      │   │
│  │  │     SharingRulesEngine         │                      │   │
│  │  │        (分润规则引擎)           │                      │   │
│  │  └────────────────┬───────────────┘                      │   │
│  │                   │                                      │   │
│  │          ┌────────┴────────┐                            │   │
│  │          ▼                 ▼                            │   │
│  │  ┌────────────────┐ ┌────────────────┐                 │   │
│  │  │ ProfitSharing  │ │  TokenPool      │                 │   │
│  │  │     Pool       │ │ (代币池)        │                 │   │
│  │  └────────────────┘ └────────────────┘                 │   │
│  │                                                          │   │
│  │  ┌────────────────────────────────┐                      │   │
│  │  │         CGHubDAO               │                      │   │
│  │  │      (治理合约)                │                      │   │
│  │  └────────────────────────────────┘                      │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Layer 1 (Ethereum Mainnet)                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌────────────────┐   ┌────────────────┐                │   │
│  │  │     MKT        │   │     STAR       │                │   │
│  │  │  (功能代币)    │   │  (治理代币)     │                │   │
│  │  └────────────────┘   └────────────────┘                 │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 十、数据流设计

### 10.1 代码上传流程

```
┌──────────────────────────────────────────────────────────────────┐
│                    代码上传与确权流程                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  开发者端                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ git push → CGHub CLI                                      │   │
│  │    │                                                      │   │
│  │    ├── 计算文件 hash (SHA-256)                           │   │
│  │    ├── 使用私钥签名 commit metadata                       │   │
│  │    ├── 上传代码片段到 IPFS                                │   │
│  │    └── 获取 IPFS CID                                     │   │
│  └─────────────────────┬─────────────────────────────────────┘   │
│                        │                                          │
│                        ▼                                          │
│  CGHub 节点层                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  验证签名 ──▶ 解析 commit 信息                           │   │
│  │       │                                                  │   │
│  │       ▼                                                  │   │
│  │  调用合约:                                                │   │
│  │  recordContribution(                                      │   │
│  │      contributor,                                         │   │
│  │      repoHash,                                            │   │
│  │      ContributionType.Commit,                            │   │
│  │      commitHash,                                          │   │
│  │      metadataCID                                          │   │
│  │  )                                                        │   │
│  │       │                                                  │   │
│  │       ▼                                                  │   │
│  │  更新仓库元数据                                            │   │
│  │  触发链上事件                                              │   │
│  │                                                          │   │
│  └─────────────────────┬─────────────────────────────────────┘   │
│                        │                                          │
│                        ▼                                          │
│  索引层                                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ The Graph 监听 ContributionRecorded 事件                 │   │
│  │      │                                                    │   │
│  │      ├── 更新贡献者排行榜                                  │   │
│  │      ├── 更新仓库贡献图                                    │   │
│  │      └── 更新实时统计数据                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.2 分润领取流程

```
┌──────────────────────────────────────────────────────────────────┐
│                    分润领取流程                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  用户操作                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ DApp 显示可领取金额                                        │   │
│  │      │                                                  │   │
│  │      ▼                                                  │   │
│  │ 点击"领取" → 连接钱包                                     │   │
│  │      │                                                  │   │
│  │      ▼                                                  │   │
│  │ 调用合约: claimProfits(repoAddress, token)              │   │
│  └─────────────────────┬─────────────────────────────────────┘   │
│                        │                                          │
│                        ▼                                          │
│  合约验证                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  1. 验证用户是贡献者 (share > 0)                         │   │
│  │  2. 计算可领取金额                                        │   │
│  │     = (总金额 × 份额比例) - 已领取                       │   │
│  │  3. 检查合约余额充足                                     │   │
│  │  4. 转移代币到用户钱包                                    │   │
│  │  5. 更新已领取记录                                        │   │
│  │  6. 触发事件                                              │   │
│  │                                                          │   │
│  └─────────────────────┬─────────────────────────────────────┘   │
│                        │                                          │
│                        ▼                                          │
│  完成                                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  代币到账 ──▶ DApp 显示余额更新 ──▶ 历史记录更新         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 十一、API 设计

### 11.1 核心 API 端点

```
GraphQL Schema:
```graphql
type Repository {
  id: ID!
  owner: Address!
  name: String!
  cid: String!
  contributors: [Contributor!]!
  totalCommits: Int!
  sharingConfig: SharingConfig
}

type Contributor {
  address: Address!
  totalWeight: Int!
  contributions: [Contribution!]!
  claimable: TokenBalance
}

type Contribution {
  id: ID!
  type: ContributionType!
  weight: Int!
  timestamp: Int!
  commitHash: String
}

type SharingConfig {
  ruleType: RuleType!
  contributorShare: Int!
  daoShare: Int!
  vestingPeriod: Int!
}

type Query {
  repository(owner: Address!, name: String!): Repository
  contributors(repoHash: ID!): [Contributor!]!
  contributionHistory(contributor: Address!): [Contribution!]!
  claimableAmount(contributor: Address!, repoHash: ID!): TokenBalance!
}

type Mutation {
  createRepository(name: String!, visibility: Visibility!): Repository!
  recordContribution(
    repoHash: ID!, 
    type: ContributionType!, 
    commitHash: String!
  ): Contribution!
  claimProfits(repoHash: ID!, token: String!): Transaction!
  createProposal(action: ProposalAction!): Proposal!
  vote(proposalId: ID!, support: Boolean!): Vote!
}
```
```

---

## 十二、实施路线图

### 阶段一：MVP（3个月）
- [ ] 核心合约开发（RepoRegistry, ContributionRegistry, ProfitSharingPool）
- [ ] 基础存储集成（IPFS）
- [ ] 简单的Web界面
- [ ] 基本贡献记录功能

### 阶段二：完整功能（6个月）
- [ ] 完整的分润规则引擎
- [ ] DAO治理模块
- [ ] 与MKT/STAR代币集成
- [ ] Git完整兼容（CLI工具）
- [ ] 移动端App

### 阶段三：生态扩展（12个月）
- [ ] 去中心化节点网络
- [ ] 第三方开发者API
- [ ] 插件市场
- [ ] 跨链支持
- [ ] 高级企业功能

---

## 附录

### A. 合约接口汇总

| 合约 | 地址 | 功能 |
|------|------|------|
| RepoRegistry | TBD | 仓库创建与管理 |
| ContributionRegistry | TBD | 贡献记录与确权 |
| SharingRulesEngine | TBD | 分润规则管理 |
| ProfitSharingPool | TBD | 分润执行 |
| CGHubDAO | TBD | 治理投票 |
| MKT | TBD | 功能代币 |
| STAR | TBD | 治理代币 |

### B. 事件清单

| 事件 | 参数 | 说明 |
|------|------|------|
| RepoCreated | owner, name, repoCID | 新仓库创建 |
| ContributorAdded | repo, contributor, share | 贡献者添加 |
| ContributionRecorded | id, contributor, repo, type, weight | 贡献记录 |
| ProfitsDeposited | repo, token, amount | 收益存入 |
| ProfitsClaimed | user, repo, token, amount | 收益领取 |
| ProposalCreated | id, proposer, targets | 提案创建 |
| VoteCast | voter, proposalId, support, weight | 投票 |

---

> **文档版本**: V1.0  
> **最后更新**: 2025年5月1日  
> **维护者**: CGHub Technical Team