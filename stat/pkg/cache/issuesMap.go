package cache

import (
    "sync"
)

var issuesMapInstance *IssuesMap
var issuesMapOnce sync.Once  // issuesMap单例
var issuesMapMu sync.RWMutex // 偷懒，使用全局锁哈哈。单写多读。生产环境锁细粒度应该更小一些。

type IssuesMap map[int]*Issue

// 更新一个Issue
func UpdateIssue(issue Issue) {
    issuesMapOnce.Do(func() {
        issuesMapInstance = &IssuesMap{}
    })

    issueId := issue.IssueId
    issuesMapMu.Lock()
    *(*issuesMapInstance)[issueId] = issue
    issuesMapMu.Unlock()
}

// 更新一个Issue的一个Comment
func UpdateComment(issueId int, comment Comment) {
    updateTag := false // 更新标志位
    issuesMapOnce.Do(func() {
        issuesMapInstance = &IssuesMap{}
    })
    issuesMapMu.RLock()
    cs := (*issuesMapInstance)[issueId].CommentsDetails
    issuesMapMu.RUnlock()

    for k, v := range cs {
        // 如果CommentId存在，使用新comment进行替换旧comment
        if v.CommentId == comment.CommentId {
            issuesMapMu.Lock()
            (*issuesMapInstance)[issueId].CommentsDetails[k] = comment
            issuesMapMu.Unlock()
            updateTag = true //已更新，更新标志位设为true
            break
        }
    }
    // comment不存在情况，在CommentsDetails末尾添加comment
    if updateTag == false {
        var commentsDetails = (*(*issuesMapInstance)[issueId]).CommentsDetails
        var commentsComments = (*issuesMapInstance)[issueId].Comments
        issuesMapMu.Lock()
        commentsDetails = append(commentsDetails, comment)
        commentsComments++
        issuesMapMu.Unlock()
    }
}

func GetIssueById(issueId int) Issue {
    return *(*issuesMapInstance)[issueId]
}
