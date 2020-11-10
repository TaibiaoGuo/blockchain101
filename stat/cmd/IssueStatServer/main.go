package main

import (
	"fmt"
	"stat/pkg/githubapi"
)

func main() {
	fmt.Println("hello")

	s := "郭001"
	//s1 := "001"
	if githubapi.MustCompile("郭001",s) == true {
		fmt.Println("yes")
	}else {
		fmt.Println("no")
	}
	c := make(chan struct{})
	githubapi.GetAllIssues(c)
}
