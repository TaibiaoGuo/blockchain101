package cache

import (
    "github.com/google/go-github/v33/github"
    "sync"
)

var issueCommentIdList []string
var allCommentsMapInstance *AllCommentsMap
var allCommentsMapMu sync.RWMutex

type IssueCommentId *int64
type AllCommentsMap map[IssueCommentId]*github.IssueComment

func (c *AllCommentsMap) UpdateMapById(comment *github.IssueComment){
    cacheOnce.Do(func() { lazyInitCache() })
    allCommentsMapMu.Lock()
    (*allCommentsMapInstance)[comment.ID]=comment
    allCommentsMapMu.Unlock()
}

func (c *AllCommentsMap) GetCommentById(id IssueCommentId) *github.IssueComment{
    cacheOnce.Do(func() { lazyInitCache() })
    allCommentsMapMu.RLock()
    defer allCommentsMapMu.RUnlock()
    return (*allCommentsMapInstance)[id]
}