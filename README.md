# DeepL 翻译接口

将 DeepL 的网页功能转换为类似官方文档的 API 接口

# 典型用例
- 为 [Bob](https://github.com/ripperhe/Bob) 多接口翻译软件提供 [自定义的免费 DeepL 服务](https://github.com/reycn/bob-plugin-deepl-translate)
- 为其他应用提供通用的 DeepL 翻译接口
# Documentation
`EXAMPLE REQUEST`
```POST /v2/translate?> HTTP/1.0
Host: YOUR_HOST
User-Agent: YourApp
Accept: */*
Content-Length: 54
Content-Type: application/x-www-form-urlencoded

text=Hello, world&target_lang=DE```
```

`EXAMPLE RESPONSE`

```
{
 "translations": [{
  "detected_source_language":"EN",
  "text":"Hallo, Welt!"
 }]
}
```

\* *Language supports in progress*

## TODO
<!-- - Target language -->
<!-- - Language detection -->
<!-- - Speed optimization -->
- Translation for long strings (Len > 5000)

