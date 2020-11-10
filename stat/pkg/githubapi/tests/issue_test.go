package tests

import (
	"stat/pkg/githubapi"
	"testing"
)

func TestMustCompile(t *testing.T) {
	type args struct {
		s         string
		shortName string
	}
	tests := []struct {
		name string
		args args
		want bool
	}{
		{"",args{s:"郭001", shortName: "郭001"},true},
		{"",args{s:"001", shortName: "郭001"},false},
		{"",args{s:"郭", shortName: "郭001"},false},
		{"",args{s:"郭 001", shortName: "郭001"},true},
		{"",args{s:"郭  001", shortName: "郭001"},true},
		{"",args{s:"郭   001", shortName: "郭001"},true},
		{"",args{s:"郭    001", shortName: "郭001"},false},
		{"",args{s:"郭     001", shortName: "郭001"},false},
		{"",args{s:"泰     001", shortName: "郭001"},false},
		{"",args{s:"", shortName: "郭001"},false},
		{"",args{s:"泰", shortName: "郭001"},false},
		{"",args{s:"中国在区块链技术中处于什么水平？唯038", shortName: "郭001"},false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := githubapi.MustCompile(tt.args.s, tt.args.shortName); got != tt.want {
				t.Errorf("MustCompile() = %v, want %v", got, tt.want)
			}
		})
	}
}