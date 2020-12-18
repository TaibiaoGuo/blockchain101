package githubapi

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "regexp"
    "stat/pkg/cache"
    "strconv"
)

// 获取某个issue的commnets
func GetIssueComments(number int) []cache.Comment {
    var jsonSlice []map[string]interface{}
    var comments []cache.Comment
    url := ISSUESURL + `/` + strconv.Itoa(number) + `/` + `/comments` // /repos/{owner}/{repo}/issues/{issue_number}/comments
    resp, err := http.Get(url)
    if err != nil {
        return nil
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)

    // 只包含[<空白符号>]
    if ok, _ := regexp.MatchString(`\[[\s*]\]`, string(body)); ok {
        return nil
    }
    // 包含"API rate limit"，表示已经超过API使用限制 v3
    // {"message":"API rate limit exceeded for
    //(But here'json the good news: Authenticated requests get a higher rate limit.
    //Check out the documentation for more details.)",
    //"documentation_url":"https://developer.github.com/v3/#rate-limiting"}
    if ok, _ := regexp.MatchString(`API rate limit`, string(body)); ok {
        log.Println("API rate limit")
    }

    json.Unmarshal(body, &jsonSlice)

    for _, v := range jsonSlice {
        commentId, _ := strconv.Atoi(fmt.Sprintf("%v", v["id"]))
        commentBody := fmt.Sprintf("%v", v["body"])
        comments = append(comments, cache.Comment{
            CommentId: commentId,
            Body:      commentBody,
        })
    }
    return comments
}
