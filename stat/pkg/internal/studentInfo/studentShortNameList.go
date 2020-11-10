package studentInfo

import "errors"

func GetStudentShortNameList(semester int) ([]string,error) {
if semester == 202002{
	return studentShortNameList202002,nil
}else {
	return nil,errors.New("semester not found")
}
}

