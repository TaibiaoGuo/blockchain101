package githubapi

import (
    "context"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "regexp"
    "strconv"
    "time"
)

// 判定给定字符串中是否包含短名身份标识及其变形样式。ps:因为学生不按格式要求作答。
// <名字最后一位><0-3个空白符><学号后3位>
func MustCompile(s string, shortName string) bool {
    pattern := `[` + string([]rune(shortName)[0]) +
        `][\s]?[\s]?[\s]?` +
        string([]rune(shortName)[len([]rune(shortName))-3:])
    ok, err := regexp.MatchString(pattern, s)
    if err != nil {
        fmt.Println(err)
    }
    return ok
}

var ISSUESURL = `https://api.github.com/repos/TaibiaoGuo/blockchain101/issues`

func getIssuesList(cancelSig chan<- struct{}, page int) string {
    url := ISSUESURL + `?per_page=20&page=` + strconv.Itoa(page)
    resp, err := http.Get(url)
    if err != nil {
        return ""
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    // 只包含[<空白符号>]，表示已经全部遍历
    if ok, _ := regexp.MatchString(`\[[\s*]\]`, string(body)); ok {
        log.Println("遍历完成")
        cancelSig <- struct{}{}
    }
    // 包含"API rate limit"，表示已经超过API使用限制 v3
    // {"message":"API rate limit exceeded for
    //(But here's the good news: Authenticated requests get a higher rate limit.
    //Check out the documentation for more details.)",
    //"documentation_url":"https://developer.github.com/v3/#rate-limiting"}
    if ok, _ := regexp.MatchString(`API rate limit`, string(body)); ok {
        log.Println("API rate limit")
        cancelSig <- struct{}{}
    }
    return string(body)
}

func GetAllIssues(cancelSig chan struct{}) {
    ctx, cancel := context.WithCancel(context.Background())
    pageNumber := 1
    go func(ctx context.Context) {
        for {
            select {
            // 遍历完全部请求，发出Done的指令,不再继续发起新的协程
            case <-ctx.Done():
                log.Println("ctx.Done")
                return
            default:
                go getIssuesList(cancelSig, pageNumber)
                pageNumber++
                time.Sleep(1 * time.Second)
            }
        }
    }(ctx)
    for {
        select {
        case <-cancelSig:
            cancel()
            return
        default:
            time.Sleep(1 * time.Second)
        }
    }
}

// 获取issues的总数
func GetMaxIssuesNumber() (maxNumber int) {
    url := ISSUESURL + `?per_page=1`
    resp, err := http.Get(url)
    if err != nil {
        return 0
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)

    // 只包含[<空白符号>]，表示已经全部遍历
    if ok, _ := regexp.MatchString(`\[[\s*]\]`, string(body)); ok {
        log.Println("遍历完成")
    }
    // 包含"API rate limit"，表示已经超过API使用限制 v3
    // {"message":"API rate limit exceeded for
    //(But here'json the good news: Authenticated requests get a higher rate limit.
    //Check out the documentation for more details.)",
    //"documentation_url":"https://developer.github.com/v3/#rate-limiting"}
    if ok, _ := regexp.MatchString(`API rate limit`, string(body)); ok {
        log.Println("API rate limit")
    }

    var jsonSlice []map[string]interface{}
    json.Unmarshal(body, &jsonSlice)
    maxNumber, err = strconv.Atoi(fmt.Sprintf("%v", jsonSlice[0]["number"]))
    return maxNumber
}
