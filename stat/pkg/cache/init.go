package cache

import (
    "log"
    "sync"
)

var cacheOnce sync.Once

// 第一次调用cache时，调用一次该函数，初始化cache
func lazyInitCache() {
    studentsMapInstance = &StudentsMap{}
    allIssuesMapInstance = &AllIssuesMap{}
    allCommentsMapInstance = &AllCommentsMap{}
    allCommentIssueMapInstance = &map[IssueCommentId]*IssueId{}
    studentShortNameList = readStudentShortNameListFromExcel("NameAndId.xlsx", "Sheet1")
    for _, ssn := range GetStudentShortNameList() {
        (*studentsMapInstance)[ssn] = &StudentIssues{StudentShortName: ssn}
    }
    log.Println("学生总数: ", len(studentShortNameList))
}

func InitCache() {
    cacheOnce.Do(func() { lazyInitCache() })
}
