/**
@program: blockchain101
@auther: TaibiaoGuo
@github: https://github.com/taibiaoGuo/
@create: 2020/03/14 12:15 GMT+8
*/
package boot
var singleRedemptionCode *Config

type Config struct {
    RedemptionCode string
}
func NewConfig(r string) *Config {
    if singleRedemptionCode == nil {
        singleRedemptionCode = &Config{RedemptionCode:r}
    }
    return singleRedemptionCode
}

func (c *Config) IsSameRedemptionCode(redemptionCode string)  bool {
    if c.RedemptionCode == redemptionCode{
        return true
    } else {
        return false
    }
}

