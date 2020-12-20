package cache

import (
    "fmt"
    "github.com/360EntSecGroup-Skylar/excelize/v2"
    "github.com/google/go-github/v33/github"
    "log"
    "os"
    "sync"
    "time"
)

const EffectiveIssue = 1
const InvalidIssue = 2
const EffectiveComment = 3
const InvalidComment = 4

var studentShortNameList []string
var studentsMapInstance *StudentsMap
var studentsMapMu sync.RWMutex

// 键：短标识符号 值：对应学生issues信息
type StudentsMap map[string]*StudentIssues

type StudentIssues struct {
    UserId                 int
    StudentShortName       string
    TotalIssuesCount       int
    AllIssuesList          []*github.Issue
    EffectiveIssuesCount   int
    EffectiveIssuesList    []*github.Issue
    InvalidIssuesCount     int
    InvalidIssuesList      []*github.Issue
    TotalCommentsCount     int
    TotalCommentsList      []*github.IssueComment
    EffectiveCommentsCount int
    EffectiveCommentsList  []*github.IssueComment
    InvalidCommentsCount   int
    InvalidCommentsList    []*github.IssueComment
    UpdatedTime            time.Time // StudentIssues更新时间
}

// 单例模式的studentsMap
// 只在程序启动时执行一次，从excel文件`NameAndId.xlsx`中读取学生的姓名和学号生成短标识符号，如`仪001`，建立内存数据库
func GetStudentsMap() *StudentsMap {
    cacheOnce.Do(func() { lazyInitCache() })
    log.Printf("studentsMap created")
    return studentsMapInstance
}

func GetStudentShortNameList() []string {
    return studentShortNameList
}

func ReplacestudentShortNameList(newList []string) {
    studentsMapMu.Lock()
    studentShortNameList = newList
    studentsMapMu.Unlock()
}

func readStudentShortNameListFromExcel(fileName string, sheetName string) []string {
    var localList []string
    f, err := excelize.OpenFile(fileName)
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    rows, err := f.Rows(sheetName)
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    for rows.Next() {
        row, err := rows.Columns()
        if err != nil {
            fmt.Println(err)
            os.Exit(1)
        }
        // row[0] is name, row[1] is id
        localList = append(localList, generateShortName(row[0], row[1]))
    }
    return localList
}

func generateShortName(name string, id string) string {
    return string([]rune(name)[len([]rune(name))-1]) + string([]rune(id)[len([]rune(id))-3:])
}

// 使用StudentShortId做索引更新学生issues信息
// message是引用类型，否则视为错误
func UpdateStudentsMapByStudentShortId(ssn string, updatePlace int, message interface{}) error {
    cacheOnce.Do(func() { lazyInitCache() })
    // 该ssn不在成绩册中，跳过
    if _, ok := (*studentsMapInstance)[ssn]; !ok {
        return nil
    }
    if updatePlace == EffectiveIssue {
        if val, ok := message.(*github.Issue); ok {
            studentsMapMu.Lock()
            (*studentsMapInstance)[ssn].TotalIssuesCount++
            (*studentsMapInstance)[ssn].EffectiveIssuesCount++
            (*studentsMapInstance)[ssn].EffectiveIssuesList = append((*studentsMapInstance)[ssn].EffectiveIssuesList, val)
            studentsMapMu.Unlock()
        } else {
            log.Println("update failed")
            return fmt.Errorf("update failed")
        }
    } else if updatePlace == InvalidIssue {
        if val, ok := message.(*github.Issue); ok {
            studentsMapMu.Lock()
            (*studentsMapInstance)[ssn].TotalIssuesCount++
            (*studentsMapInstance)[ssn].InvalidIssuesCount++
            (*studentsMapInstance)[ssn].InvalidIssuesList = append((*studentsMapInstance)[ssn].InvalidIssuesList, val)
            studentsMapMu.Unlock()
        } else {
            log.Println("update failed")
            return fmt.Errorf("update failed")
        }
    } else if updatePlace == EffectiveComment {
        if val, ok := message.(*github.IssueComment); ok {
            studentsMapMu.Lock()
            (*studentsMapInstance)[ssn].TotalCommentsCount++
            (*studentsMapInstance)[ssn].EffectiveCommentsCount++
            (*studentsMapInstance)[ssn].EffectiveCommentsList = append((*studentsMapInstance)[ssn].EffectiveCommentsList, val)
            studentsMapMu.Unlock()
        } else {
            log.Println("update failed")
            return fmt.Errorf("update failed")
        }
    } else if updatePlace == InvalidComment {
        if val, ok := message.(*github.IssueComment); ok {
            studentsMapMu.Lock()
            (*studentsMapInstance)[ssn].TotalCommentsCount++
            (*studentsMapInstance)[ssn].InvalidCommentsCount++
            (*studentsMapInstance)[ssn].InvalidCommentsList = append((*studentsMapInstance)[ssn].InvalidCommentsList, val)
            studentsMapMu.Unlock()
        } else {
            log.Println("update failed")
            return fmt.Errorf("update failed")
        }
    } else {
        return fmt.Errorf("unknown format")
    }

    return nil
}

func GetStudentIssueBySSN(ssn string) *StudentIssues  {
    return (*GetStudentsMap())[ssn]
}
