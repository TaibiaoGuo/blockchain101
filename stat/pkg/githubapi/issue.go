package githubapi

import (
	"fmt"
	"regexp"
)

// 判定给定字符串中是否包含短名身份标识及其变形样式。ps:因为学生不按格式要求作答。
// <名字最后一位><0-3个空白符><学号后3位>
func MustCompile(s string, shortName string) bool {
	pattern := `[` +string([]rune(shortName)[0]) +
		`][\s]?[\s]?[\s]?` +
		string([]rune(shortName)[len([]rune(shortName))-3:])
	ok, err := regexp.MatchString(pattern, s)
	if err != nil {
		fmt.Println(err)
	}
	return ok
}