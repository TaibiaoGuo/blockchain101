package cache

import "time"

type StudentIssues struct {
    StudentNickName      string  `json:"student_nick_name"`
    StudentShortId       string  `json:"student_short_id"`
    TotalIssuesCount     int     `json:"total_issues_count"`
    OpeningIssuesCount   int     `json:"opening_issues_count"`
    OpeningIssuesList    []Issue `json:"opening_issues_list"`
    ClosedIssuesCount    int     `json:"closed_issues_count"`
    ClosedIssuesList     []Issue `json:"closed_issues_list"`
    TotalCommentsCount   int     `json:"total_comments_count"`
    OpeningCommentsCount int     `json:"opening_comments_count"`
    OpeningCommentsList  []Issue `json:"opening_comments_list"`
    ClosedCommentsCount  int     `json:"closed_comments_count"`
    ClosedCommentsList   []Issue `json:"closed_comments_list"`
    UpdatedTime string // StudentIssues更新时间
}

// 一个原始issue例子
/*
{
  "url": "https://api.github.com/repos/TaibiaoGuo/blockchain101/issues/32",
  "repository_url": "https://api.github.com/repos/TaibiaoGuo/blockchain101",
  "labels_url": "https://api.github.com/repos/TaibiaoGuo/blockchain101/issues/32/labels{/name}",
  "comments_url": "https://api.github.com/repos/TaibiaoGuo/blockchain101/issues/32/comments",
  "events_url": "https://api.github.com/repos/TaibiaoGuo/blockchain101/issues/32/events",
  "html_url": "https://github.com/TaibiaoGuo/blockchain101/issues/32",
  "id": 618878159,
  "node_id": "MDU6SXNzdWU2MTg4NzgxNTk=",
  "number": 32,
  "title": "比特币的价值真的跟它现在的价格相匹配吗？",
  "user": {
    "login": "Johnieljl",
    "id": 62162180,
    "node_id": "MDQ6VXNlcjYyMTYyMTgw",
    "avatar_url": "https://avatars1.githubusercontent.com/u/62162180?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/Johnieljl",
    "html_url": "https://github.com/Johnieljl",
    "followers_url": "https://api.github.com/users/Johnieljl/followers",
    "following_url": "https://api.github.com/users/Johnieljl/following{/other_user}",
    "gists_url": "https://api.github.com/users/Johnieljl/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/Johnieljl/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/Johnieljl/subscriptions",
    "organizations_url": "https://api.github.com/users/Johnieljl/orgs",
    "repos_url": "https://api.github.com/users/Johnieljl/repos",
    "events_url": "https://api.github.com/users/Johnieljl/events{/privacy}",
    "received_events_url": "https://api.github.com/users/Johnieljl/received_events",
    "type": "User",
    "site_admin": false
  },
  "labels": [
    {
      "id": 1889506732,
      "node_id": "MDU6TGFiZWwxODg5NTA2NzMy",
      "url": "https://api.github.com/repos/TaibiaoGuo/blockchain101/labels/%E6%AF%94%E7%89%B9%E5%B8%81",
      "name": "比特币",
      "color": "f1a4f9",
      "default": false,
      "description": ""
    },
    {
      "id": 1889506084,
      "node_id": "MDU6TGFiZWwxODg5NTA2MDg0",
      "url": "https://api.github.com/repos/TaibiaoGuo/blockchain101/labels/%E9%87%91%E8%9E%8D",
      "name": "金融",
      "color": "65d8bf",
      "default": false,
      "description": ""
    }
  ],
  "state": "open",
  "locked": false,
  "assignee": null,
  "assignees": [

  ],
  "milestone": null,
  "comments": 3,
  "created_at": "2020-05-15T10:50:22Z",
  "updated_at": "2020-11-19T12:38:50Z",
  "closed_at": null,
  "author_association": "NONE",
  "active_lock_reason": null,
  "body": "比特币的价格在前段时间有小幅下降，但这几天又再次登上9000W美元每枚的高位，个人觉得炒作成分特别大，大家的看法呢？\r\n彦126",
  "closed_by": null,
  "performed_via_github_app": null
}
*/
type Issue struct {
    IssueId         int    `json:"issue_id"`
    Title           string `json:"title"`
    Body            string `json:"body"`
    State           string // issue状态，open为正常状态
    CreatedTime     time.Time
    UpdatedTime     time.Time    // issue内容最后更新时间
    Comments        int       // 评论条数
    CommentsDetails []Comment // 评论内容
}

// 一个原始comment例子
/*
{
    "url": "https://api.github.com/repos/TaibiaoGuo/blockchain101/issues/comments/709804335",
    "html_url": "https://github.com/TaibiaoGuo/blockchain101/issues/32#issuecomment-709804335",
    "issue_url": "https://api.github.com/repos/TaibiaoGuo/blockchain101/issues/32",
    "id": 709804335,
    "node_id": "MDEyOklzc3VlQ29tbWVudDcwOTgwNDMzNQ==",
    "user": {
      "login": "W-health",
      "id": 72654863,
      "node_id": "MDQ6VXNlcjcyNjU0ODYz",
      "avatar_url": "https://avatars2.githubusercontent.com/u/72654863?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/W-health",
      "html_url": "https://github.com/W-health",
      "followers_url": "https://api.github.com/users/W-health/followers",
      "following_url": "https://api.github.com/users/W-health/following{/other_user}",
      "gists_url": "https://api.github.com/users/W-health/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/W-health/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/W-health/subscriptions",
      "organizations_url": "https://api.github.com/users/W-health/orgs",
      "repos_url": "https://api.github.com/users/W-health/repos",
      "events_url": "https://api.github.com/users/W-health/events{/privacy}",
      "received_events_url": "https://api.github.com/users/W-health/received_events",
      "type": "User",
      "site_admin": false
    },
    "created_at": "2020-10-16T05:40:23Z",
    "updated_at": "2020-10-16T05:40:23Z",
    "author_association": "NONE",
    "body": "比特币本身属性类似于黄金，因此，它的价格受到市场需求、开采成本等各项因素的影响。就当前来说，比特币的开采主要通过挖矿来完成，主要有矿场主、云算力投资者两类人参与，最主要的成本就是矿机、电费。受比特币产量减半影响，云算力投资者因为电费、托管费、矿机成本整体而言都比较高，因此，就当前价格来说挖矿的收益是不足以支付电费的，所以几乎所有的云算力投资者都已停止了挖矿。矿场主因为具备极大的主动权，可以寻觅到更低的电价，尤其是在四川、甚至国外一些地方，电费可以比云算力投资者少一倍、甚至更低，所以在不考虑矿机成本的前提下，挖矿收益比电费更多，所以目前处于一个微利的状态，还在继续挖矿。因此，比特币价格和它当前的价值是大致匹配的，毕竟矿机寿命是有限的，一般1.5年到2年就无法使用，之后就需要重新购置矿机，另外，经营矿场过程中也会遇到其他问题和风险。欣219",
    "performed_via_github_app": null
  }
*/
type Comment struct {
    CommentId   int    `json:"comment_id"`
    Body        string `json:"body"`
    CreatedTime time.Time
    UpdatedTime time.Time
}
