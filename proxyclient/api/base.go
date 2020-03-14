/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 15:22 GMT+8
*/
package api

import (
    "encoding/json"
    "fmt"
    "net/http"
)

type BaseJsonBean struct {
    Code    int         `json:"code"`
    Data    interface{} `json:"data"`
    Message string      `json:"message"`
}

func NewBaseJsonBean() *BaseJsonBean {
    return &BaseJsonBean{}
}

func HTTPResponse(w http.ResponseWriter,result *BaseJsonBean){
    bytes, _ := json.Marshal(result)
    fmt.Fprint(w,string(bytes))
}