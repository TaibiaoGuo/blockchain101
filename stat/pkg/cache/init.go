package cache

import "sync"

var cacheOnce sync.Once

// 第一次调用cache时，调用一次该函数，初始化cache
func lazyInitCache() {
    studentsMapinstance = &StudentsMap{}
    allIssuesMapInstance = &AllIssuesMap{}
    allCommentsMapInstance = &AllCommentsMap{}
    studentShortNameList = readStudentShortNameListFromExcel("NameAndId.xlsx", "Sheet1")
    for _, ssn := range GetStudentShortNameList() {
        (*studentsMapinstance)[ssn] = &StudentIssues{StudentShortName: ssn}
    }
}
