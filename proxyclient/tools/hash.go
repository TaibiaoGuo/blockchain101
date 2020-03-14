/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 19:36 GMT+8
*/
package tools

import (
    "crypto/md5"
    "encoding/hex"
)

func CreateClientHash(r,i string) string{
    s := r + i
    md5Inst := md5.New()
    md5Inst.Write([]byte(s))
    md5Result := hex.EncodeToString(md5Inst.Sum(nil))
    result := md5Result[:8]
    return result
}
