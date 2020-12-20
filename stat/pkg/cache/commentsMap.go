package cache

import (
    "github.com/google/go-github/v33/github"
    "sync"
)

var issueCommentIdList []IssueCommentId
var allCommentsMapInstance *AllCommentsMap
var allCommentIssueMapInstance *map[IssueCommentId]IssueId
var allCommentsMapMu sync.RWMutex

type IssueCommentId *int64
type AllCommentsMap map[IssueCommentId]*github.IssueComment

func (c *AllCommentsMap) UpdateMapById(comment *github.IssueComment) {
    cacheOnce.Do(func() { lazyInitCache() })
    allCommentsMapMu.Lock()
    (*allCommentsMapInstance)[comment.ID] = comment
    allCommentsMapMu.Unlock()
}

// 用dirtyMap 替换 allCommentsMapInstance
func ReplaceCommentsMap(newMap *AllCommentsMap) {
    cacheOnce.Do(func() { lazyInitCache() })
    allCommentsMapMu.Lock()
    allCommentsMapInstance = newMap
    allCommentsMapMu.Unlock()
}

// 用dirtyList 替换 issueCommentIdList
func ReplaceCommentsList(newList []IssueCommentId) {
    cacheOnce.Do(func() { lazyInitCache() })
    allCommentsMapMu.Lock()
    issueCommentIdList = newList
    allCommentsMapMu.Unlock()
}

// 用dirtyMap 替换 allCommentIssueMapInstance
func ReplaceAllCommentIssueMap(newMap *map[IssueCommentId]IssueId) {
    cacheOnce.Do(func() { lazyInitCache() })
    allCommentsMapMu.Lock()
    allIssuesMapMu.Lock()
    allCommentIssueMapInstance = newMap
    allIssuesMapMu.Unlock()
    allCommentsMapMu.Unlock()
}

func GetCommentsMap() *AllCommentsMap {
    allCommentsMapMu.RLock()
    defer allCommentsMapMu.RUnlock()
    return allCommentsMapInstance

}

func GetCommentsList() *[]IssueCommentId {
    allCommentsMapMu.RLock()
    defer allCommentsMapMu.RUnlock()
    return &issueCommentIdList
}

func GetCommentById(id IssueCommentId) *github.IssueComment {
    cacheOnce.Do(func() { lazyInitCache() })
    allCommentsMapMu.RLock()
    defer allCommentsMapMu.RUnlock()
    return (*allCommentsMapInstance)[id]
}

func IsIssueOpenByCommentId(id IssueCommentId) bool  {
    cacheOnce.Do(func() { lazyInitCache() })
    allCommentsMapMu.RLock()
    // 根据commentId获取issuesId
    issueId := (*allCommentIssueMapInstance)[id]
    allCommentsMapMu.RUnlock()
    allIssuesMapMu.RLock()
    // 根据issuesId获取issue
    issue := GetIssueById(issueId)
    allIssuesMapMu.RUnlock()
    if *issue.State == "open" {
        return true
    } else {
        return false
    }
}
