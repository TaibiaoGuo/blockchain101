package main

import (
    "context"
    "fmt"
    "github.com/google/go-github/v33/github"
    "golang.org/x/oauth2"
    "log"
    "os"
)

func main() {
    ctx := context.Background()
    var client *github.Client

    if os.Getenv("BLOCKCHAIN101ACCESSTOEKN") != "" {
        ts := oauth2.StaticTokenSource(
            &oauth2.Token{AccessToken: os.Getenv("BLOCKCHAIN101ACCESSTOEKN")},
        )
        log.Println("auth client")
        tc := oauth2.NewClient(ctx, ts)
        client = github.NewClient(tc)
    } else {
        log.Println("not auth client")
        client = github.NewClient(nil)
    }
    // repos, _, _ := client.Repositories.List(ctx, "taibiaoguo", nil)
    issues, _, _ := client.Issues.ListByRepo(ctx, "taibiaoguo", "blockchain101", nil)
    fmt.Println(issues)
}
