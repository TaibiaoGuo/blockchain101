package tests

import (
	"stat/pkg/githubapi"
	"testing"
)

func TestGetIssuesList(t *testing.T) {
	tests := []struct {
		name string
		want string
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := githubapi.GetIssuesList(); got != tt.want {
				t.Errorf("GetIssuesList() = %v, want %v", got, tt.want)
			}
		})
	}
}
