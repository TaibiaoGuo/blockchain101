package githubapi

import (
    "log"
    "sync"
    "time"
)

var StudentsMapCreatedSignal = make(chan bool, 1)

/*
每当issuesMap建库完成
遍历一遍issues，修改studentsMap的数据
 */
func Run() {
    cj := newCornJob()
    cj.onceWait(StudentsMapCreatedSignal)
    for {
        err := cj.run()
        if err != nil {
            log.Println("cornJob failed")
            time.Sleep(time.Hour)
        }else {
            log.Println("cornJob succeed")
            time.Sleep(time.Hour*24)
        }
    }
}

type cornJob struct {
    count int
    status string // enum: running,sleep
    lastRun string // enum: success,failed,unknown
    lastRunTime time.Time
    waitStart bool
    mu sync.RWMutex
}

func  newCornJob() *cornJob {
    cj := &cornJob{
        count:       0,
        status:      "sleep",
        lastRun:     "unknown",
        lastRunTime: time.Time{},
        waitStart:   true,
        mu : sync.RWMutex{},
    }
    return cj
}

// 运行一次
func(c *cornJob) run() error {
    // 更新状态
    c.setCornJobAsRunning()
    // 当函数终止时更新状态
    defer c.setCornJobAsSleeping()
    // 执行issuesMap建库
    maxIssuesNumber,err := GetMaxIssuesNumber()
    if err != nil {
        c.setCornJobAsFailed()
        return err
    }
    for i := 1; i <= maxIssuesNumber; i++ {
        func(issueId int){
            // 拉取issue
            // 判断issue状态
            // 拉取对应comments
            // 存储comments至对应issues
            // 存储issue至issuesMap
        }(i)
    }
return nil
}

// 阻塞直到收到studentsMap建库完成的通知
func(c *cornJob) onceWait(start chan bool) {
    <- start // 阻塞直到收到通知
    // 函数执行完成前关闭通道
    defer close(start)
}

func(c *cornJob) setCornJobAsRunning()  {
    c.mu.Lock()
    c.waitStart = false
    c.lastRunTime = time.Now()
    c.status = "running"
    c.mu.Unlock()
}

func(c *cornJob) setCornJobAsSleeping()  {
    c.mu.Lock()
    c.status = "sleep"
    c.waitStart= true
    c.mu.Unlock()
}

func(c *cornJob) setCornJobAsFailed()  {
    c.mu.Lock()
    c.lastRun="failed"
    c.mu.Unlock()
}