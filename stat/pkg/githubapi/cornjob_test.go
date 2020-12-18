package githubapi

import (
    "testing"
)

func Test_GetMaxIssuesNumber(t *testing.T) {
    type args struct {
    }

    tests := []struct {
        name          string
        args          args
        wantMaxNumber int
    }{
        {"", args{}, 1},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if gotMaxNumber := GetMaxIssuesNumber(); gotMaxNumber == 0 {
                t.Errorf("GetMaxIssuesNumber() = %v, want %v", gotMaxNumber, ">0")
            }
        })
    }
}
