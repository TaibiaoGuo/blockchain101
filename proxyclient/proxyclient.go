/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 14:49 GMT+8
*/
package main

import (
    "./core/boot"
    "flag"
    "fmt"
    "net/http"
    "os"
    "./api"
    "time"
)

var cmdRedemptionCOde string

func main() {
    //传入参数解析
    flag.StringVar(&cmdRedemptionCOde, "r", "", "-r [兑换码] 例子: -r ACGG5PDCPIKGPQU")
    flag.Parse()
    if cmdRedemptionCOde == "" || len(cmdRedemptionCOde) != 15 {
        fmt.Printf("[错误] 请输入正确的兑换码，兑换码和ECS服务器兑换码相同！")
        flag.Usage()
        os.Exit(1)
    }
    // Config的单一模式初始化写入兑换码
    boot.NewConfig(cmdRedemptionCOde)

    // 启动API服务
    go func() {
        http.HandleFunc("/v1/download", api.Downloadhandle)
        http.HandleFunc("/v1/health", api.Healthhandle)
        http.ListenAndServe("0.0.0.0:7001", nil)
    }()

    // TODO 判断服务端状态
    go func(){
        for {
            time.Sleep(2 * time.Second)
            func() {
                //请求服务端判断服务端状态
                _,e :=api.ServerStatusCheck()
                if e != nil {
                    return
                }
                time.Sleep(58 * time.Second)
                return
            }()

        }
    }()

    // TOOD 版本升级功能实现

    // 阻塞防止退出
    for {
        time.Sleep(time.Minute)
    }

}
