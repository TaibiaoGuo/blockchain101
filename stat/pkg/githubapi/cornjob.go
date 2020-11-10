package githubapi

import (
	"context"
	"fmt"
	"io/ioutil"
	"net/http"
	"regexp"
	"strconv"
	"time"
)

var ISSUESURL = `https://api.github.com/repos/TaibiaoGuo/blockchain101/issues`

func getIssuesList(ctx context.Context ,cancelSig chan<- struct{},page int) string {
	url := ISSUESURL + `?per_page=20&page=` + strconv.Itoa(page)
	method := "GET"

	client := &http.Client{
	}
	req, err := http.NewRequest(method, url, nil)

	if err != nil {
		fmt.Println(err)
		return ""
	}
	res, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return ""
	}
	defer res.Body.Close()

	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Println(err)
		return ""
	}
	// 只包含[<空白符号>]，表示已经全部遍历
	if ok,_ := regexp.MatchString(`\[[\s]*\]`,string(body));ok{
		fmt.Println("只包含[<空白符号>]，表示已经全部遍历")
		cancelSig <- struct{}{}
	}
	// 包含"API rate limit"，表示已经超过API使用限制 v3
	// {"message":"API rate limit exceeded for
	//(But here's the good news: Authenticated requests get a higher rate limit.
	//Check out the documentation for more details.)",
	//"documentation_url":"https://developer.github.com/v3/#rate-limiting"}
	if ok,_ := regexp.MatchString(`API rate limit`,string(body));ok{
		fmt.Println("API rate limit")
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
				fmt.Println("ctx.Done")
				return
			default:
				go getIssuesList(ctx,cancelSig,pageNumber)
				pageNumber++
				time.Sleep(1 * time.Second)
			}
		}
	}(ctx)
	for  {
		select {
		case <-cancelSig:
			cancel()
			return
		default:
			time.Sleep(1 * time.Second)
		}
	}
}
