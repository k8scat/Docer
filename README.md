# [Docer](https://www.docer.com/)
> 免责声明：本项目旨在学习，不可使用于商业和个人其他意图。若使用不当，均由个人承担。

[![License](https://img.shields.io/github/license/richardchien/nonebot.svg)](./LICENSE)

`iPhone` 手机上 `WPS` 有一周的免费 `VIP` 体验, 然后就...

## Support

* [x] [Word](https://www.docer.com/s/wps/?page=1)

## Todo

* [ ] [PPT](https://www.docer.com/s/wpp/?page=1)
* [ ] [Excel](https://www.docer.com/s/et/?page=1)

## Start

开发环境: Mac + Chrome78

chromedriver: https://sites.google.com/a/chromium.org/chromedriver/downloads

```
pip install --user pipenv
python -m pipenv install --python 3
# 扫码登录获取cookies
python -m pipenv run python login.py

# 修改爬取文件存放的位置, 例如word.py中设置save_path
save_path = '/Users/mac/Downloads/docer/word/'
# 爬取word
python -m pipenv run python crawler.py

```

## Mongo

使用 `mongodb` 只需去掉相应注释即可

## Blog

https://hsowan.me