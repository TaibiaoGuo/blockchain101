package studentInfo

import (
    "fmt"
    "github.com/360EntSecGroup-Skylar/excelize/v2"
)

var studentShortNameList []string

func GetStudentShortNameList(semester int) []string {
    return studentShortNameList
}

func readStudentShortNameListFromExcel(fileName string, sheetName string) ([]string, error) {
    f, err := excelize.OpenFile(fileName)
    if err != nil {
        fmt.Println(err)
        return nil, err
    }

    rows, err := f.GetRows(sheetName)
    for _, row := range rows {
        for _, colCell := range row {
            fmt.Print(colCell, "\t")
        }
        fmt.Print()
    }
    return nil, nil
}
