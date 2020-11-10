package cache

import (
	"fmt"
	"github.com/360EntSecGroup-Skylar/excelize/v2"
	"os"
	"sync"
)

var studentShortNameList []string
var instance *StudentsMap
var once sync.Once

type StudentsMap map[string]StudentIssues

// 单例模式的studentsMap
// 只在程序启动时执行一次，从excel文件`NameAndId.xlsx`中读取学生的姓名和学号生成短标识符号，如`仪001`，建立内存数据库
func GetStudentsMap() *StudentsMap {
	once.Do(func() {
		instance = &StudentsMap{}
		studentShortNameList = readStudentShortNameListFromExcel("NameAndId.xlsx", "Sheet1")
		for _, ssn := range GetStudentShortNameList() {
			(*instance)[ssn] = StudentIssues{}
		}
	})
	return instance
}

func GetStudentShortNameList() []string {
	return studentShortNameList
}

func readStudentShortNameListFromExcel(fileName string, sheetName string) []string {
	var localList []string
	f, err := excelize.OpenFile(fileName)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	rows, err := f.Rows(sheetName)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	for rows.Next() {
		row, err := rows.Columns()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
		// row[0] is name, row[1] is id
		localList = append(localList, generateShortName(row[0], row[1]))
	}
	return localList
}

func generateShortName(name string, id string) string {
	return string([]rune(name)[len([]rune(name))-1]) + string([]rune(id)[len([]rune(id))-3:])
}
