/**
@program: stat
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/12/20 05:06 GMT+8
*/
package githubapi

import (
    "reflect"
    "stat/pkg/cache"
    "testing"
)

var issueTestData = []byte(
    `{
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
}`)

func wantedIssueHelper() cache.Issue {
    issueCreatedTime, _ := rfc3339NanoTimeParse("2020-05-15T10:50:22Z")
    issueUpdatedTime, _ := rfc3339NanoTimeParse("2020-11-19T12:38:50Z")
    issue := cache.Issue{
        IssueId:     32,
        Title:       "比特币的价值真的跟它现在的价格相匹配吗？",
        Body:        "比特币的价格在前段时间有小幅下降，但这几天又再次登上9000W美元每枚的高位，个人觉得炒作成分特别大，大家的看法呢？\r\n彦126",
        State:       "open",
        CreatedTime: issueCreatedTime,
        UpdatedTime: issueUpdatedTime,
        Comments:    3,
    }
    return issue
}

func Test_issueByteToObject(t *testing.T) {
    type args struct {
        issueNumber int
        body        []byte
    }
    tests := []struct {
        name      string
        args      args
        wantIssue cache.Issue
        wantErr   bool
    }{
        {
            name:      "",
            args:      args{issueNumber: 32, body: issueTestData},
            wantIssue:  wantedIssueHelper(),
            wantErr:  false },
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            gotIssue, err := issueByteToObject(tt.args.issueNumber, tt.args.body)
            if (err != nil) != tt.wantErr {
                t.Errorf("issueByteToObject() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if !reflect.DeepEqual(gotIssue, tt.wantIssue) {
                t.Errorf("issueByteToObject() gotIssue = %v, want %v", gotIssue, tt.wantIssue)
            }
        })
    }
}
