# CGHub OPC 合伙人机制 + 智能合约设计白皮书

> **版本：** V1.0
> **日期：** 2026-05-22
> **作者：** Hermes（总助理）
> **定位：** 黑客松路演核心材料 + 合伙人招募说明书

---

## 一、为什么需要 OPC 合伙人机制？

### 1.1 传统创业的问题

```
传统创业：
① 创始人出资，雇佣员工
② 员工出卖时间，拿固定工资
③ 价值分配由创始人决定
④ 早期贡献者往往拿不到应得的回报
⑤ 员工没有动力把事情当成自己的事
```

### 1.2 CGHub 的解法：OPC 合伙人机制

```
CGHub OPC：
① 加入即贡献——你带着技能和时间加入，不要求出资
② 贡献即确权——你的每一笔贡献都被链上记录
③ 分配即合约——收益分配规则写在智能合约里
④ 退出即清算——离开时按贡献比例带走你应得的
```

**类比：Gitcoin Grants 空投逻辑**
> Gitcoin 的 Quadratic Funding 让早期贡献者获得代币空投奖励
> CGHub 让每个合伙人的贡献都被记录，未来平台升值时获得对应回报

---

## 二、OPC 合伙人体系

### 2.1 四种角色

```
┌──────────────────────────────────────────────────┐
│              CGHub 角色体系                       │
├──────────────────────────────────────────────────┤
│                                                  │
│  👤 创客（Maker）                                 │
│  ├── 定义：使用 CGHub 的独立创客                  │
│  ├── 权益：拥有个人主页+作品集                    │
│  └── 义务：按项目贡献                             │
│                                                  │
│  🤝 贡献者（Contributor）                         │
│  ├── 定义：在项目中贡献时间和技能的人             │
│  ├── 权益：获得项目收益分成+链上记录              │
│  └── 义务：按时完成任务，接受 DAO 监督            │
│                                                  │
│  🎫 船票持有者（Token Holder）                    │
│  ├── 定义：持有 CGHub 船票代币的人               │
│  ├── 权益：治理投票权+平台收益分成                │
│  └── 义务：参与 DAO 治理（最低参与率要求）        │
│                                                  │
│  ⭐ 合伙人（Partner）                             │
│  ├── 定义：核心贡献者，获得合伙人资格             │
│  ├── 权益：收益分成+决策权+平台增值红利          │
│  └── 义务：持续贡献，不低于季度最低贡献门槛       │
│                                                  │
└──────────────────────────────────────────────────┘
```

### 2.2 船票系统（核心创新）

```
什么是船票？
① 船票 = CGHub DAO 成员资格证明
② 船票 = 治理权代币（1票/票）
③ 船票 = 平台收益分配权（按持有量分红）
④ 船票 = 终身有效（除非主动退出）

船票如何获得？（三种路径）

路径一：贡献获得（主要）
├── 完成项目 → 获得船票积分
├── 积分达标 → 兑换船票
└── 参考 Gitcoin 空投逻辑：早期贡献者获得更多

路径二：购买获得（次要）
├── 公开募集期：白名单价格购买
├── 公募期：公开价格购买
└── 限制：单人持有上限（防止大户垄断）

路径三：赠予（特殊情况）
├── 对平台有重大贡献者
├── 决策：DAO 投票决定
└── 比例限制：总发行量5%上限
```

---

## 三、智能合约设计

### 3.1 核心合约架构

```
┌─────────────────────────────────────────────────────┐
│              CGHub 合约架构                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  CGHubToken.sol（船票代币）                        │
│  ├── ERC20 标准                                    │
│  ├── 总量上限：10,000,000 CGX                      │
│  ├── 分配：创客40% / 贡献者30% / 团队15% / 国库15%│
│  └── 治理功能：投票权重                            │
│                                                     │
│  CGHubContribution.sol（贡献记录合约）             │
│  ├── 贡献类型：代码 / 内容 / 设计 / 运营           │
│  ├── 贡献积分：按类型×难度×质量计算               │
│  ├── 审核机制：DAO 投票确认                       │
│  └── 记录不可篡改                                  │
│                                                     │
│  CGHubProject.sol（项目合约）                       │
│  ├── 项目创建                                      │
│  ├── 分配规则设置                                  │
│  ├── 里程碑管理                                    │
│  └── 收益释放                                      │
│                                                     │
│  CGHubDAO.sol（治理合约）                          │
│  ├── 提案系统                                      │
│  ├── 投票机制                                      │
│  ├── 执行机制                                      │
│  └── 合伙人资格管理                                │
│                                                     │
│  CGHubDistributor.sol（分配合约）                  │
│  ├── 收益聚合                                      │
│  ├── 按规则分配                                    │
│  └── 链上自动执行                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 3.2 CGHubToken.sol（代币合约）

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";

contract CGHubToken is ERC20, ERC20Votes {
    uint256 public constant MAX_SUPPLY = 10_000_000 * 10**18;

    // 分配比例
    uint256 public constant MAKER_ALLOCATION = 40;      // 创客：40%
    uint256 public constant CONTRIBUTOR_ALLOCATION = 30; // 贡献者：30%
    uint256 public constant TEAM_ALLOCATION = 15;        // 团队：15%
    uint256 public constant TREASURY_ALLOCATION = 15;    // 国库：15%

    address public governance;
    address public treasury;

    constructor(
        address _governance,
        address _treasury
    ) ERC20("CGHub Token", "CGX") EIP712("CGHub", "1.0") {
        governance = _governance;
        treasury = _treasury;

        // 初始铸造（根据合约地址分配）
        _mint(msg.sender, MAX_SUPPLY);
    }

    // 铸造新代币（仅治理合约可调用）
    function mint(address to, uint256 amount) external {
        require(msg.sender == governance, "Only governance");
        require(totalSupply() + amount <= MAX_SUPPLY, "Max supply exceeded");
        _mint(to, amount);
    }

    // 销毁代币（用于惩罚机制）
    function burn(address from, uint256 amount) external {
        require(msg.sender == governance, "Only governance");
        _burn(from, amount);
    }
}
```

### 3.3 CGHubContribution.sol（贡献记录合约）

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract CGHubContribution is Ownable {
    enum ContributionType { Code, Content, Design, Operations }
    enum Status { Pending, Approved, Rejected }

    struct Contribution {
        address contributor;
        ContributionType kind;
        uint256 points;
        string description;
        Status status;
        uint256 projectId;
        uint256 timestamp;
    }

    uint256 public contributionCount;
    mapping(uint256 => Contribution) public contributions;
    mapping(address => uint256[]) public contributorHistory;

    event ContributionSubmitted(
        uint256 indexed id,
        address indexed contributor,
        ContributionType kind,
        uint256 points
    );
    event ContributionApproved(uint256 indexed id, uint256 points);
    event ContributionRejected(uint256 indexed id);

    // 提交贡献
    function submitContribution(
        address contributor,
        ContributionType kind,
        uint256 points,
        string memory description,
        uint256 projectId
    ) external onlyOwner returns (uint256) {
        contributionCount++;
        contributions[contributionCount] = Contribution({
            contributor: contributor,
            kind: kind,
            points: points,
            description: description,
            status: Status.Pending,
            projectId: projectId,
            timestamp: block.timestamp
        });
        contributorHistory[contributor].push(contributionCount);
        emit ContributionSubmitted(contributionCount, contributor, kind, points);
        return contributionCount;
    }

    // 审核贡献（DAO投票后由治理合约调用）
    function approveContribution(uint256 id) external onlyOwner {
        require(contributions[id].status == Status.Pending, "Not pending");
        contributions[id].status = Status.Approved;
        emit ContributionApproved(id, contributions[id].points);
    }

    // 驳回贡献
    function rejectContribution(uint256 id) external onlyOwner {
        require(contributions[id].status == Status.Pending, "Not pending");
        contributions[id].status = Status.Rejected;
        emit ContributionRejected(id);
    }

    // 查询某地址的累计积分
    function getTotalPoints(address contributor) external view returns (uint256) {
        uint256 total;
        for (uint256 i = 0; i < contributorHistory[contributor].length; i++) {
            uint256 id = contributorHistory[contributor][i];
            if (contributions[id].status == Status.Approved) {
                total += contributions[id].points;
            }
        }
        return total;
    }
}
```

### 3.4 CGHubProject.sol（项目合约）

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract CGHubProject is Ownable {
    struct Project {
        address owner;
        string name;
        string description;
        uint256 totalBudget;
        uint256 remainingBudget;
        address[] contributors;
        mapping(address => uint256) shareRatio; // 千分比
        mapping(address => uint256) earned;
        bool completed;
    }

    uint256 public projectCount;
    mapping(uint256 => Project) public projects;

    event ProjectCreated(uint256 indexed id, address owner, uint256 budget);
    event ContributionAdded(uint256 indexed projectId, address contributor, uint256 share);
    event PayoutReleased(uint256 indexed projectId, address contributor, uint256 amount);
    event ProjectCompleted(uint256 indexed id);

    // 创建项目
    function createProject(
        string memory name,
        string memory description,
        uint256 budget
    ) external returns (uint256) {
        projectCount++;
        Project storage p = projects[projectCount];
        p.owner = msg.sender;
        p.name = name;
        p.description = description;
        p.totalBudget = budget;
        p.remainingBudget = budget;
        emit ProjectCreated(projectCount, msg.sender, budget);
        return projectCount;
    }

    // 设置贡献者分配比例
    function setContributorShare(
        uint256 projectId,
        address contributor,
        uint256 sharePermille // 千分比，如 400 = 40%
    ) external onlyOwner {
        Project storage p = projects[projectId];
        require(p.owner == msg.sender, "Not owner");
        require(sharePermille <= 1000, "Max 100%");
        p.contributors.push(contributor);
        p.shareRatio[contributor] = sharePermille;
    }

    // 释放收益
    function releasePayout(uint256 projectId, address contributor) external onlyOwner {
        Project storage p = projects[projectId];
        uint256 share = p.shareRatio[contributor];
        uint256 amount = (p.remainingBudget * share) / 1000;

        require(amount > 0, "No balance");
        p.remainingBudget -= amount;
        p.earned[contributor] += amount;

        // 转账（实际项目中会调用代币合约）
        payable(contributor).transfer(amount);
        emit PayoutReleased(projectId, contributor, amount);
    }

    // 标记项目完成
    function completeProject(uint256 projectId) external onlyOwner {
        projects[projectId].completed = true;
        emit ProjectCompleted(projectId);
    }
}
```

---

## 四、合伙人收益分配规则

### 4.1 收益来源

```
① 项目收益分成
   ├── 发起项目：收益的 10% 进入平台池
   ├── 参与项目：按贡献比例分配
   └── 平台池：按船票持有量分配

② 平台增值收益
   ├── 手续费收入
   ├── 订阅收入
   └── 国库收益

③ 早期合伙人红利（类 Gitcoin 空投）
   └── 黑客松参与者/早期贡献者获得额外代币分配
```

### 4.2 季度分红机制

```
每季度结束，平台池收益按以下方式分配：

第一步：计算合伙人贡献积分
第二步：积分换算为分配权重
第三步：按权重分配 USDC 收益
第四步：链上自动执行
```

### 4.3 退出机制

```
主动退出：
① 提交退出申请
② DAO 审核（7天冷静期）
③ 按累计贡献积分兑换代币
④ 代币转出，钱包清零

被动退出（低于门槛）：
① 连续两个季度未达最低贡献门槛
② 警告一次（30天补救期）
③ 未补救 → 降级为普通贡献者
④ 船票保留，但治理权重降为 0
```

---

## 五、黑客松场景应用

### 5.1 Hackathon 项目分配模板

```
黑客松项目分配建议（标准版）：

发起人（你）：30%
核心开发者A：25%
核心开发者B：20%
设计师：15%
运营/内容：10%

总计：100%
```

### 5.2 Hackathon 评委问题回答

**Q：你们怎么分钱？**
> 我们用智能合约。分配规则在项目发起时就设定好，部署到链上后谁也改不了。项目完成后，收益按预设比例自动分配，不需要任何第三方。

**Q：早期合伙人有什么好处？**
> 参考 Gitcoin 的逻辑——早期贡献者获得更多。黑客松参与者、项目贡献者，都会获得 CGHub 代币（船票）空投，这些代币代表着未来平台的治理权和收益分配权。

**Q：没有代币怎么激励？**
> 短期：贡献积分 + 实物回报（黑客松奖金/产品股份）
> 长期：代币空投 + 季度分红

---

*最后更新：2026-05-22 by Hermes（总助理）*
