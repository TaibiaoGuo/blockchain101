/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 15:22 GMT+8
*/
package api

import (
    "../core/boot"
    "io"
    "net/http"
    "os"
)
/*
存储了userclient，如果redemptioncode正确则会提供下载，包含windows、安卓、Mac版本。
 */
const BASEFILEPATH = "/usr/local/blockchain101/bin"
const USERCLIENT = "client.zip"

type ApiDownload struct {
}
/*
GET /download?redemptioncode=xxxxxxxxxxxxxxx
 */
func (d ApiDownload) Downloadhandle(w http.ResponseWriter, request *http.Request) {
    //文件上传只允许GET方法
    if request.Method != http.MethodGet {
        w.WriteHeader(http.StatusMethodNotAllowed)
        _, _ = w.Write([]byte("Method not allowed"))
        return
    }
    //检查兑换码是否正确
    redemptionCode := request.FormValue("redemptioncode")
    //Config 使用单例模式，这里会直接读取到初始化所生成的配置
    c := boot.NewConfig("")
    if c.IsSameRedemptionCode(redemptionCode) {
        w.WriteHeader(http.StatusBadRequest)
        _, _ = io.WriteString(w, "Bad request")
        return
    }
    // log.Println("redemptioncode: " + redemptionCode)
    //打开文件
    file, err := os.Open(BASEFILEPATH + "/" + USERCLIENT)
    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        _, _ = io.WriteString(w, "Bad request")
        return
    }
    //结束后关闭文件
    defer file.Close()

    //设置响应的header头
    w.Header().Add("Content-type", "application/octet-stream")
    w.Header().Add("content-disposition", "attachment; filename=client.zip")
    //将文件写至responseBody
    _, err = io.Copy(w, file)
    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        _, _ = io.WriteString(w, "Bad request")
        return
    }
}
