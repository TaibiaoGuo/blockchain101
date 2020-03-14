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
    "io"
    "net/http"
    "os"
    "./api"
    "time"
    "./tools"
)

var cmdConfig boot.Config

func main() {
    //传入参数解析
    flag.StringVar(&cmdConfig.RedemptionCode, "r", "", "-r [兑换码] 例子: -r ACGG5PDCPIKGPQU")
    flag.Parse()
    if cmdConfig.RedemptionCode == "" || len(cmdConfig.RedemptionCode) != 15 {
        fmt.Printf("[错误] 请输入正确的兑换码，兑换码和ECS服务器兑换码相同！")
        flag.Usage()
        os.Exit(1)
    }
    // Config的单一模式初始化写入
    boot.NewConfig(cmdConfig.RedemptionCode)

    // 启动API服务
    go func() {
        http.HandleFunc("v1/download", api.Downloadhandle)
        http.HandleFunc("/v1/health", api.Healthhandle)
        http.ListenAndServe(":7001", nil)
    }()

    // TODO 判断服务端状态
    for {
       time.Sleep(60 * time.Second)
       func() {
           client := &http.Client{}
           url := "http://47.113.88.216:170001/v1/login"
           req, err := http.NewRequest("GET", url, nil)
           if err != nil {
               fmt.Println(err)
           } else {
               conf := boot.NewConfig("")
               q := req.URL.Query()
               publicIP,_ := tools.GetPublicIP()
               q.Add("ip", publicIP)
               q.Add("port", "7001")
               q.Add("hash", tools.CreateClientHash(conf.RedemptionCode,publicIP))
               q.Add("redemptionCode",conf.RedemptionCode )
               req.URL.RawQuery = q.Encode()

               response, _ := client.Do(req)
               stdout := os.Stdout
               _, err = io.Copy(stdout, response.Body)
               status := response.StatusCode
               fmt.Println(status)
           }
       }()
    }

// TOOD 版本升级

}
