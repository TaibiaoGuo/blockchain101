/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 14:14 GMT+8
*/
package tools

import (
    "archive/zip"
    "io"
    "os"
)

/*
压缩文件或文件夹
@files:文件数组，可以是不同dir下的文件或者文件夹
@dest:压缩文件存放地址
 */
func Compress(files []*os.File, dest string) error {
    d, _ := os.Create(dest)
    defer d.Close()
    w := zip.NewWriter(d)
    defer w.Close()
    for _, file := range files {
        err := compress(file, "", w)
        if err != nil {
            return err
        }
    }
    return nil
}

func compress(file *os.File, prefix string, zw *zip.Writer) error {
    info, err := file.Stat()
    if err != nil {
        return err
    }
    if info.IsDir() {
        prefix = prefix + "/" + info.Name()
        fileInfos, err := file.Readdir(-1)
        if err != nil {
            return err
        }
        for _, fi := range fileInfos {
            f, err := os.Open(file.Name() + "/" + fi.Name())
            if err != nil {
                return err
            }
            err = compress(f, prefix, zw)
            if err != nil {
                return err
            }
        }
    } else {
        header, err := zip.FileInfoHeader(info)
        header.Name = prefix + "/" + header.Name
        if err != nil {
            return err
        }
        writer, err := zw.CreateHeader(header)
        if err != nil {
            return err
        }
        _, err = io.Copy(writer, file)
        file.Close()
        if err != nil {
            return err
        }
    }
    return nil
}