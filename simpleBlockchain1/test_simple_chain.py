# jetbrains pytest docs
# https://www.jetbrains.com/help/pycharm/pytest.html
# pytest docs
# https://docs.pytest.org/en/stable/index.html

from . import simple_chain as sc

class TestMessageUnitTest:
    """
    Message类的单元测试
    """

    def test_init(self):
        case = [
            "1",
            "hello",
            "EOF",
            "你好"
        ]
        for i in case:
            message = sc.Message(i)
            assert message.data == i

    def test__hash_payload(self):
        """
        单元测试 _hash_payload 方法
        """
        case = [
            {'timestamp': 1602252778.7426066,
             'data': str(1),
             'hexdigest': '1fad31b7d2f429da09dd01a1b549e3baa6087d7b62c1c56a6f0dc5ab4376c1db'},
            {'timestamp': 1602252778.7426066,
             'data': str("hello"),
             'hexdigest': 'adfa45c763c427eab42db377e3371f4ddd460870dc45cf3b19705730ac49da5f'},
            {'timestamp': 1602252778.7426066,
             'data': str("你好"),
             'hexdigest': '35ec626cfa627bf4d63b8ac362f37698667fe0210c34f594ef05eb8bf88219a6'},
        ]
        for i in case:
            message = sc.Message(i["data"])
            message.timestamp = i['timestamp']
            assert message._hash_payload() == i['hexdigest']

    def test__hash_message(self):
        assert True

    def test_link(self):
        assert True

    def test_seal(self):
        assert True

    def test_validate(self):
        assert True