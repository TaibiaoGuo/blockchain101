/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 19:34 GMT+8
*/
package tools

import (
    "io/ioutil"
    "net/http"
    "errors"
)

func GetPublicIP() (string, error) {
    publicIP := ""

    for i := 0; i < 3; i++ {
        resp, err := http.Get("http://myexternalip.com/raw")
        if err != nil {
            return "", err
        }
        defer resp.Body.Close()
        content, _ := ioutil.ReadAll(resp.Body)
        publicIP = string(content)
        if publicIP != "" {
            break
        }
    }

    if publicIP == "" {
        return "", errors.New("[ERROR] network can't connecting")
    }

    return publicIP, nil
}
