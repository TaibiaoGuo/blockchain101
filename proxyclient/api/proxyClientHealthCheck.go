/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 12:03 GMT+8
*/
package api

import (
    "net/http"
)

type ApiHealth struct {

}
// proxyclient 健康状态检查
func  Healthhandle(w http.ResponseWriter,req *http.Request){
    result := NewBaseJsonBean()
if healthCheck()=="ok"{
    result.Code = 200
    result.Message =  "ok"
    statusServer ,errServerStatus := ServerStatusCheck()
    if errServerStatus != nil{
        result.Data= errServerStatus.Error() + "，客户端健康"
    } else {
        result.Data= "服务器"+ statusServer + "客户端健康"
    }

} else {
    return
}
HTTPResponse(w,result)
}


/*
 服务端发起私钥签名的信息，客户端验证数字签名，执行升级指令
 升级成功后启动新的服务
 TODO：接收服务端的主动升级指令并启动软件的升级
*/
func VersionUpdate(w http.ResponseWriter,req *http.Request){

}

// proxyclient 健康状态检查,简单返回ok
func healthCheck() string {
return "ok"
}




