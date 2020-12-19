package main

import (
    "stat/pkg/cache"
    "stat/pkg/githubapi"
    "time"
)

func main() {
    go githubapi.Run()
    cache.GetStudentsMap()
    // 通知StudentsMap初始化成功
    githubapi.StudentsMapCreatedSignal <- true
    for {
        time.Sleep(time.Second*60)
    }
}
