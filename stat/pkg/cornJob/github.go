package cornJob

import (
    "context"
    "github.com/google/go-github/v33/github"
    "go.uber.org/ratelimit"
    "golang.org/x/oauth2"
    "log"
    "net/http"
    "os"
    "stat/pkg/cache"
    "sync"
    "time"
)

const EnvKey = "BLOCKCHAIN101ACCESSTOEKN"
const owner = "taibiaoguo"
const repo = "blockchain101"

var ISSUESURL = `https://api.github.com/repos/TaibiaoGuo/blockchain101/issues`

func NewGithubClient(ctx context.Context) *github.Client {
    if os.Getenv(EnvKey) != "" {
        ts := oauth2.StaticTokenSource(
            &oauth2.Token{AccessToken: os.Getenv(EnvKey)},
        )
        log.Println("auth client")
        tc := oauth2.NewClient(ctx, ts)
        return github.NewClient(tc)
    } else {
        log.Println("not auth client")
        return github.NewClient(nil)
    }
}

func GetAllIssues(ctx context.Context) (*cache.AllIssuesMap, *[]cache.IssueId) {

    client := NewGithubClient(ctx)
    page := 1
    count := 0
    dirtyAllIssuesMap := &cache.AllIssuesMap{}
    dirtyIssuesIdList := &[]cache.IssueId{}
    for {
        opts := &github.IssueListByRepoOptions{State: "all", ListOptions: github.ListOptions{Page: page}}
        issues, _, err := client.Issues.ListByRepo(ctx, owner, repo, opts)
        if err != nil {
            log.Println("API Rate Limit")
            time.Sleep(time.Minute)
        } else if len(issues) == 0 {
            log.Println("issues count:", count)
            return dirtyAllIssuesMap, dirtyIssuesIdList
        } else {
            page++
            count = count + len(issues)
            for i, v := range issues {
                *dirtyIssuesIdList = append(*dirtyIssuesIdList, issues[i].ID)
                (*dirtyAllIssuesMap)[issues[i].ID] = v
            }
        }
    }
}

func GetALlComments(ctx context.Context, allIssuesMap *cache.AllIssuesMap) (*cache.AllCommentsMap, *[]cache.IssueCommentId) {
    client := NewGithubClient(ctx)
    page := 1
    count := 0
    dirtyAllCommentsMap := &cache.AllCommentsMap{}
    dirtyIssueCommentsIdList := &[]cache.IssueCommentId{}
    for {
        opts := &github.IssueListCommentsOptions{ListOptions: github.ListOptions{Page: page}}
        comments, _, err := client.Issues.ListComments(ctx, owner, repo, 0, opts)
        if err != nil {
            if _,ok := err.(*github.RateLimitError);ok{
                log.Println("API Rate Limit")
                time.Sleep(time.Minute)
            }
        } else if len(comments) == 0 {
            log.Println("comments count:", count)
            return dirtyAllCommentsMap, dirtyIssueCommentsIdList
        } else {
            page++
            count = count + len(comments)
            for i, v := range comments {
                *dirtyIssueCommentsIdList = append(*dirtyIssueCommentsIdList, comments[i].ID)
                (*dirtyAllCommentsMap)[comments[i].ID] = v
            }
        }
    }
}

// 通过 ListComments 建立 Comments-Issue 索引
func GetCommentsIssueMap(ctx context.Context) *map[cache.IssueCommentId]cache.IssueId {
    client := NewGithubClient(ctx)
    // 获取maxNumber
    maxNumber := len(*cache.GetIssuesList())
    count := 0
    dirtyAllCommentIssueMapInstance := &map[cache.IssueCommentId]cache.IssueId{}
    // 遍历所有issues
    // 协程组
    var wg sync.WaitGroup
    // 限制，每秒令牌
    rl := ratelimit.New(10)
    for number := 1; number <= maxNumber; number++ {
        // todo： 1、添加速率限制检查，降低执行时长；
        // todo: 2、避免通过API获取 Comments-Issue 索引，而是通过已有Comments、Issues信息创建索引

        //  阻塞，直到拿到执行令牌
        rl.Take()
     go func(ctx context.Context) {
         wg.Add(1)
         page := 1
         log.Println("为",number,"建立 Comments-Issue 索引")
            for {
                // 获取
                opts := &github.IssueListCommentsOptions{ListOptions: github.ListOptions{Page: page}}
                // 发起API请求
                comments, resp, err := client.Issues.ListComments(ctx, owner, repo, number, opts)
                if err != nil {
                    if _,ok := err.(*github.RateLimitError);ok{
                        log.Println("API Rate Limit")
                        time.Sleep(time.Minute)
                    } else if resp == nil {
                        log.Println("issue",number,"resp is nil")
                        time.Sleep(time.Minute)
                    } else if resp.Response.StatusCode == http.StatusNotFound {
                        log.Println("issue",number,"not found,break")
                        break
                    }
                    log.Println(err)
                }
                // 发起API请求
                issue, _, err := client.Issues.Get(ctx, owner, repo, number)
                if err != nil {
                    if _,ok := err.(*github.RateLimitError);ok{
                        time.Sleep(time.Minute)
                        log.Println("API Rate Limit")
                    }
                } else if len(comments) == 0 {
                    log.Println("issue",number,"comments=0,break")
                    break
                } else {
                    for j, _ := range comments {
                        (*dirtyAllCommentIssueMapInstance)[comments[j].ID] = issue.ID
                    }
                    page++
                    count = count + len(comments)
                }
            }
            wg.Done()
        }(ctx)
    }
    // 等待所有协程结束
    wg.Wait()

    log.Println("Comments-Issue 索引 建立完成，索引到", maxNumber, "issues", "和", count, "comments")
    return dirtyAllCommentIssueMapInstance
}
