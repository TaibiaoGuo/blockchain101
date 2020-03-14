/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 12:10 GMT+8
*/
package version

import (
    "fmt"
    "strings"
)

type version struct {
    VersionTag string
    ImageRepository string
    ImageName string
}

func (v *version) CheckVersion() *version{
    switch v.getVersionImageRepository() {
    case "aliyun":
        v.aliyunCheckVersion()
    case "dockerhub":
        v.dockerhubCheckVersion()
    default:
        {
        fmt.Println("[ERROR] CheckVersion failure.\n")
        v.recoveryVersionImageRepository()
            fmt.Println("[INFO] ImageRepository has been recovery. ")}
    }
    return v
}

func (v *version) aliyunCheckVersion() *version{

    return v
}

func (v *version) dockerhubCheckVersion() *version{
    return v
}

func (v *version) getVersionImageRepository() string {
    if strings.Contains(v.ImageRepository,"aliyuncs.com"){
        return "aliyun"
    } else {
        return "dockerhub"
    }
}

func (v *version) recoveryVersionImageRepository() *version{
    v.ImageRepository="registry.cn-shenzhen.aliyuncs.com/"
    return v
}