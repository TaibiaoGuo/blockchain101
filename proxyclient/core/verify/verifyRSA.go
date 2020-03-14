/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 13:32 GMT+8
*/
package verify

import (
    "crypto"
    "crypto/rsa"
    "crypto/sha512"
    "crypto/x509"
    "encoding/pem"
    "os"
)

func getRsaPubKeyFileName()  string{
    file,err := os.Open("./")
    if err != nil {
        panic(err)
    }
    fileInfo,err := file.Stat()
    if err != nil {
        panic(err)
    }
    buf := make([]byte,fileInfo.Size())
    file.Read(buf)
    file.Close()
}

// rsa签名认证
func VerifyRSA(plainText,signText []byte, rsaPubKeyFileName string) bool {
    // 1 打开公钥文件，将内容读出
    file,err := os.Open(rsaPubKeyFileName)
    if err != nil {
        panic(err)
    }
    fileInfo,err := file.Stat()
    if err != nil {
        panic(err)
    }
    buf := make([]byte,fileInfo.Size())
    file.Read(buf)
    file.Close()
    // 2 pem解码得到block
    block,_ := pem.Decode(buf)
    // 3 x509解析得到接口
    pubInterface,err := x509.ParsePKIXPublicKey(block.Bytes)
    if err != nil {
        panic(err)
    }
    // 4 接口进行类型断言得到公钥结构体
    publicKey := pubInterface.(*rsa.PublicKey)
    // 5 对原始明文进行hash运算得到散列值
    hashText := sha512.Sum512(plainText)
    // 6 签名认证
    err = rsa.VerifyPKCS1v15(publicKey,crypto.SHA512,hashText[:],signText)
    if err == nil {
        return true
    }
    return false
}

