from alerter import Alerter


if __name__ == '__main__':
    app = Alerter()

    app.add("https://open.feishu.cn/open-apis/bot/v2/hook/4c34e75a-d436-41b3-8160-3b43f2f0b6cc")
    ret = app.notify(
        body='what a great notification service!',
        title='my notification title',
    )
    print(ret)
