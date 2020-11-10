package cache

type StudentIssues struct {
	StudentNickName      string `json:"student_nick_name"`
	StudentShortId       string `json:"student_short_id"`
	TotalIssuesCount     int `json:"total_issues_count"`
	OpeningIssuesCount   int `json:"opening_issues_count"`
	OpeningIssuesList    []Issue `json:"opening_issues_list"`
	ClosedIssuesCount    int `json:"closed_issues_count"`
	ClosedIssuesList     []Issue `json:"closed_issues_list"`
	TotalCommentsCount   int `json:"total_comments_count"`
	OpeningCommentsCount int `json:"opening_comments_count"`
	OpeningCommentsList  []Issue `json:"opening_comments_list"`
	ClosedCommentsCount  int `json:"closed_comments_count"`
	ClosedCommentsList   []Issue `json:"closed_comments_list"`
}

type Issue struct {
	IssueId int `json:"issue_id"`
	state   string `json:"state"`
	Title   string `json:"title"`
	Body    string `json:"body"`
}

type Comment struct {
	CommentId int `json:"comment_id"`
	Title     string `json:"title"`
	Body      string `json:"body"`
}
