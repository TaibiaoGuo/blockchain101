package stat

import (
    "context"
    "log"
    "regexp"
    "stat/pkg/cache"
)

// 判定给定字符串中是否包含短名身份标识及其变形样式。ps:因为学生不按格式要求作答。
// <名字最后一位><0-3个空白符><学号后3位>
func MustCompile(s string, shortName string) bool {
    pattern := `[` + string([]rune(shortName)[0]) +
        `][\s]?[\s]?[\s]?` +
        string([]rune(shortName)[len([]rune(shortName))-3:])
    ok, err := regexp.MatchString(pattern, s)
    if err != nil {
        log.Println(err)
    }
    return ok
}

func UpdateStudentsMap(ctx context.Context) error {
    issuesList := cache.GetIssuesList()
    commentsList := cache.GetCommentsList()
    // 遍历 issue 写入 StudentsMap
    for _, issueId := range *issuesList {
        log.Println("为issueId",issueId,"更新用户Map")
        err := UpdateStudentIssue(ctx, issueId)
        if err != nil {
            return err
        }
    }
    // 遍历 comment 写入 StudentsMap
    for _, commentsId := range *commentsList {
        log.Println("为commentsId",commentsId,"更新用户Map")
        err := UpdateStudentComment(ctx, commentsId)
        if err != nil {
            return err
        }
    }
    return nil
}

// 更新学生Issues信息
func UpdateStudentIssue(ctx context.Context, issueId cache.IssueId) error {
    issue := cache.GetIssueById(issueId)
    ssn:= FindSSN(ctx, issue.Body)
    if ssn == "" {
        ssn = FindSSN(ctx, issue.Title)
    }
    // 如果找到了对应的ssn
    if ssn != "" {
    // 判断对应issue的类型
        if *issue.State == "open"{
            cache.UpdateStudentsMapByStudentShortId(ssn,cache.EffectiveIssue,issue)
        } else {
            cache.UpdateStudentsMapByStudentShortId(ssn,cache.InvalidIssue,issue)
        }
    } else {
        // 什么也不做，不更新信息
        return nil
    }
    return nil
}

// 更新学生Comment信息
func UpdateStudentComment(ctx context.Context, commentId cache.IssueCommentId) error {
    comment := cache.GetCommentById(commentId)
    ssn:= FindSSN(ctx, comment.Body)
    // 如果找到了对应的ssn
    if ssn != "" {
        // 判断comment对应issue的类型,如果issue不为open状态，则comment无效
        if cache.IsIssueOpenByCommentId(commentId){
            cache.UpdateStudentsMapByStudentShortId(ssn,cache.EffectiveComment, comment)
        } else {
            cache.UpdateStudentsMapByStudentShortId(ssn,cache.InvalidComment, comment)
        }
    } else {
        // 什么也不做，不更新信息
        return nil
    }
    return nil
}

// 从给定的信息中找到对应的ssn
func FindSSN(ctx context.Context, message *string) (ssn string) {
    for _, v := range cache.GetStudentShortNameList() {
        if MustCompile(*message, v) {
            return v
        }
    }
    return ""
}
