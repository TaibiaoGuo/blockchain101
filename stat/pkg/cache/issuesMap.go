package cache

import (
    "github.com/google/go-github/v33/github"
    "sync"
)

var issueIdList []string
var allIssuesMapInstance *AllIssuesMap
var allIssuesMapMu sync.RWMutex

type IssueId *int64
type AllIssuesMap map[IssueId]*github.Issue

func (c *AllIssuesMap) UpdateMapById(issue *github.Issue){
    cacheOnce.Do(func() { lazyInitCache() })
    allIssuesMapMu.Lock()
    (*allIssuesMapInstance)[issue.ID]= issue
    allIssuesMapMu.Unlock()
}

func (c *AllIssuesMap) GetIssueById(id IssueCommentId) *github.IssueComment{
    cacheOnce.Do(func() { lazyInitCache() })
    allIssuesMapMu.RLock()
    defer allIssuesMapMu.RUnlock()
    return (*allCommentsMapInstance)[id]
}