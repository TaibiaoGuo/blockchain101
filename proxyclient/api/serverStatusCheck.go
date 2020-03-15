/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/15 15:23 GMT+8
*/
package api

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "net/url"
    "../tools"
    "../core/boot"
)

type serverStatus struct {
    Code           uint64 `json:"code"`
    Message       string `json:"message"`
}

func ServerStatusCheck() (string,error)  {
    //构造URL
    params := url.Values{}
    Url, errParse := url.Parse("http://47.113.88.216:170001/v1/login")
    if errParse != nil {
        return "",errParse
    }
    publicIP,_ := tools.GetPublicIP()
    conf := boot.NewConfig("")
    params.Set("ip",publicIP)
    params.Set("port","7001")
    params.Set("hash",tools.CreateClientHash(conf.RedemptionCode,publicIP))
    params.Set("redemptionCode",conf.RedemptionCode)
    //如果参数中有中文参数,这个方法会进行URLEncode
    Url.RawQuery = params.Encode()
    urlPath := Url.String()

    //发起请求，得到返回resp
    //这里必须要判断错误，否则请求失败时会造成内存泄漏
    resp,errGet:= http.Get(urlPath)
    if errGet != nil{
        fmt.Println("服务端不在线，稍后重试")
        return "",nil
    }
    defer resp.Body.Close()
    body, errioutil := ioutil.ReadAll(resp.Body)
    if errioutil != nil {
        return "",nil
    } else {
        bodyPtr := &serverStatus{}
        errJson := json.Unmarshal(body, bodyPtr)
        if errJson != nil{
            return "",nil
        }
        return bodyPtr.Message,nil
    }
}