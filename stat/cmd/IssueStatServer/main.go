package main

import (
    "log"
    "stat/pkg/githubapi"
)

func main() {
    n := githubapi.GetMaxIssuesNumber()
    log.Println("total issues:", n)
}
