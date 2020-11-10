package tests

import (
	"reflect"
	"stat/pkg/cache"
	"testing"
)

func TestGetStudentsMap(t *testing.T) {
	tests := []struct {
		name string
		want *cache.StudentsMap
	}{
		{name: "",want: &cache.StudentsMap{"彪234": cache.StudentIssues{},"是513": cache.StudentIssues{},"定314": cache.StudentIssues{}}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := cache.GetStudentsMap(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("GetStudentsMap() = %v, want %v", got, tt.want)
			}
		})
	}
}
