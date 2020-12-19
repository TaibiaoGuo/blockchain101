package githubapi

import (
    "log"
    "time"
)

var timeBegin = "2020-09-01T00:00:00+08:00" // issue、comment起始提交时间
var timeEnd = "2020-12-20T00:00:00+08:00"   // issue、comment终止提交时间

// 根据更新时间判断当前版本是否为最新版本
func isLatestVersion(lastTime, thisTime string) bool {
    t, err := time.Parse(time.RFC3339Nano, lastTime) // example:"2013-06-05T14:10:43.678Z"
    if err != nil {
        panic(err)
    }
    t2, err := time.Parse(time.RFC3339Nano, thisTime)
    if err != nil {
        panic(err)
    }
    if t2.After(t) {
        return false
    } else {
        return true
    }
}

// 判断创建时间是否是在要求的时间区间内
func isCreatedInDuration(thisTime string) bool {
    t1, err := time.Parse(time.RFC3339, timeBegin) // example:"2020-09-01T00:00:00+08:00"
    t2, err := time.Parse(time.RFC3339, timeEnd)   // example:"2020-09-01T00:00:00+08:00"
    if err != nil {
        log.Printf(err.Error())
    }
    t3, err := time.Parse(time.RFC3339Nano, thisTime)
    if err != nil {
        panic(err)
    }
    if t3.Before(t1) || t3.After(t2) {
        return false
    } else {
        return true
    }
}

func rfc3339NanoTimeParse(thisTime string) (time.Time ,error){
t1, err := time.Parse(time.RFC3339, timeBegin) // example:"2020-09-01T00:00:00+08:00"
return t1,err
}
