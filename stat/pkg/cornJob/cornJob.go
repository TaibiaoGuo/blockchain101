package cornJob

import (
    "context"
    "fmt"
    "log"
    "stat/pkg/cache"
    "stat/pkg/stat"
    "sync"
    "time"
)

// 每天执行一次数据更新
const cornTime = time.Hour * 24
const running = "running"
const sleep = "sleep"
const success = "success"
const failed = "failed"
const unknown = "unknown"

type CornJob struct {
    count       int
    status      string // enum: running,sleep
    lastRun     string // enum: success,failed,unknown
    lastRunTime time.Time
    waitStart   bool
    mu          sync.RWMutex
}

// 每隔一天执行一次更新
func Run() {
    cj := CornJob{}
    //for {
    //    go cj.run(context.Background())
    //    time.Sleep(time.Second*2)
    //}
    cj.run(context.Background())
}

// 执行一次job
func (c *CornJob) run(ctx context.Context) error {
    ctx2, cancel := context.WithTimeout(ctx, cornTime)
    defer cancel()
    c.setCornJobAsUnknown()
    c.setCornJobAsRunning()
    // 当函数终止时更新状态
    defer c.setCornJobAsSleeping()
    // 初始化cache
    cache.InitCache()
    log.Println("before cache")

    // 拉取并存储所有issues
    newIssuesMap, newIssuesIdList := GetAllIssues(ctx2)
    cache.ReplaceIssuesMap(newIssuesMap)
    cache.ReplaceIssuesList(*newIssuesIdList)
    // 拉取并存储所有Comments
    newCommentsMap, newCommentsIdList := GetALlComments(ctx2, cache.GetIssuesMap())
    cache.ReplaceCommentsMap(newCommentsMap)
    cache.ReplaceCommentsList(*newCommentsIdList)
    // 建立comment-issues 索引
    newCommentsIssueMap := GetCommentsIssueMap(ctx2)
    cache.ReplaceAllCommentIssueMap(newCommentsIssueMap)
    // 根据cache进行统计，生成studentsMap
    err := stat.UpdateStudentsMap(ctx2)
    if err != nil{
        return err
    }
    // 日志打印，显示每个学生的信息
    for _, ssn := range cache.GetStudentShortNameList(){
        fmt.Println(cache.GetStudentIssueBySSN(ssn).StudentShortName,cache.GetStudentIssueBySSN(ssn).TotalIssuesCount,cache.GetStudentIssueBySSN(ssn).TotalCommentsCount)
    }

    //
    c.lastRun = success

    select {
    case <-ctx2.Done():
        return fmt.Errorf("cornjob timeout")
    default:
        if c.lastRun == success {
            log.Println(success)
            return nil
        } else if c.lastRun == unknown {
            log.Println(unknown)
            return fmt.Errorf("unknown cornjob")
        } else {
            log.Println(failed)
            c.setCornJobAsFailed()
            return fmt.Errorf("cornjob failed")
        }
    }
}

// 阻塞直到收到studentsMap建库完成的通知
func (c *CornJob) onceWait(start chan bool) {
    <-start // 阻塞直到收到通知
    // 函数执行完成前关闭通道
    defer close(start)
}

func (c *CornJob) setCornJobAsRunning() {
    c.mu.Lock()
    c.waitStart = false
    c.lastRunTime = time.Now()
    c.status = running
    c.mu.Unlock()
}

func (c *CornJob) setCornJobAsSleeping() {
    c.mu.Lock()
    c.status = sleep
    c.waitStart = true
    c.mu.Unlock()
}

func (c *CornJob) setCornJobAsFailed() {
    c.mu.Lock()
    c.lastRun = failed
    c.mu.Unlock()
}

func (c *CornJob) setCornJobAsUnknown() {
    c.mu.Lock()
    c.lastRun = unknown
    c.mu.Unlock()
}
