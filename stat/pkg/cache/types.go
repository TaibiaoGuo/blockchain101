package cache

type StudentIssues struct {
	StudentNickName      string
	StudentShortId       string
	TotalIssuesCount     int
	OpeningIssuesCount   int
	OpeningIssuesList    []Issue
	ClosedIssuesCount    int
	ClosedIssuesList     []Issue
	TotalCommentsCount   int
	OpeningCommentsCount int
	OpeningCommentsList  []Issue
	ClosedCommentsCount  int
	ClosedCommentsList   []Issue
}

type Issue struct {
	IssueId int
	state   string
	Title   string
	Body    string
}

type Comment struct {
	CommentId int
	Title     string
	Body      string
}
