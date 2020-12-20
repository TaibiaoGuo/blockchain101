package stat

type Rule interface {
    Pass() bool
}

// 防作弊规则集
type CheatRule struct {
    opts *map[string]interface{}
}

func (c *CheatRule) Pass() bool {
    return true
}

// 单条消息中包含多个用户标识，判定为作弊
// 对于任意一条issue或者comment，判断其中是否含有多个用户标示，如果有，则该条消息作弊
// 判定作弊的消息要被记录为无效（不在该函数处理）
// 建议在存入缓存前进行处理
func (c *CheatRule) multiUserInOneMessageCheat(message interface{}) bool {
    return true
}

// 单账户使用了多个用户标示，判定为作弊
// 对于某账户所有的issue和comment，如果其包含两个用户标示，则判定该账户作弊
// 判定作弊的账户所有的参与的issue和comment应该要记录为无效（不在该函数处理）
// 必须在完成
func (c *CheatRule) multiSSNInOneUserCheat(message interface{}) bool {
    return true
}

// 防垃圾信息规则
type SpanRule struct {
    opts *map[string]interface{}
}

func (c *SpanRule) Pass() bool {
    return true
}

// 消息太短，判定为垃圾信息
// 如果某条消息太短，则该消息被判定为垃圾消息，消息应该被记录为无效（不在该函数处理）
func (c *CheatRule) tooShortSpan(message interface{}) bool {
    return true
}
