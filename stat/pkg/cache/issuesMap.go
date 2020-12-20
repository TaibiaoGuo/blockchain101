package cache

import (
    "github.com/google/go-github/v33/github"
    "sync"
)

var issueIdList []IssueId
var allIssuesMapInstance *AllIssuesMap
var allIssuesMapMu sync.RWMutex

type IssueId *int64
type AllIssuesMap map[IssueId]*github.Issue

func (c *AllIssuesMap) UpdateMapById(issue *github.Issue) {
    cacheOnce.Do(func() { lazyInitCache() })
    allIssuesMapMu.Lock()
    (*allIssuesMapInstance)[issue.ID] = issue
    allIssuesMapMu.Unlock()
}

// 用dirtyMap替换allIssuesMapInstance
func ReplaceIssuesMap(newMap *AllIssuesMap) {
    cacheOnce.Do(func() { lazyInitCache() })
    allIssuesMapMu.Lock()
    allIssuesMapInstance = newMap
    allIssuesMapMu.Unlock()
}

// 用dirtyList 替换 issueIdList
func ReplaceIssuesList(newList []IssueId) {
    cacheOnce.Do(func() { lazyInitCache() })
    allIssuesMapMu.Lock()
    issueIdList = newList
    allIssuesMapMu.Unlock()
}

func GetIssuesMap() *AllIssuesMap {
    allIssuesMapMu.RLock()
    defer allIssuesMapMu.RUnlock()
    return allIssuesMapInstance
}

func GetIssuesList() *[]IssueId {
    allIssuesMapMu.RLock()
    defer allIssuesMapMu.RUnlock()
    return &issueIdList
}

func GetIssueById(id IssueId) *github.Issue {
    cacheOnce.Do(func() { lazyInitCache() })
    allIssuesMapMu.RLock()
    defer allIssuesMapMu.RUnlock()
    return (*allIssuesMapInstance)[id]
}
