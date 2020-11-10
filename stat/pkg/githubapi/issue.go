package githubapi

import (
	"fmt"
	"regexp"
	"strconv"
)
// 判定给定字符串中是否包含短名身份标识及其变形样式。ps:因为学生不按格式要求作答。
// <名字最后一位><0-3个空白符><学号后3位>
func mustCompile(s string,shortName string) bool{
	pattern := `[` + chartToUTF8Code(string([]rune(shortName)[0:1])) + `][\s]？[\s]？[\s]？` + string([]rune(shortName)[:3])
	ok,err := regexp.Match(s, []byte(pattern))
	if err != nil {
		fmt.Println(err)
	}
	return ok
}

// 将单个字符转换成utf8的16进制样式，例如\u4e00
func chartToUTF8Code(s string) string{
	 return strconv.QuoteToASCII(s)
}