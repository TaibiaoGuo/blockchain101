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
    "os"
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

    // 启动API服务

    // 初始化服务


}
