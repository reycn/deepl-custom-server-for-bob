import asyncio
import time
from pyppeteer import launch

PARMS = {
    "headless":
    True,
    "args": [
        '--disable-infobars',  # 关闭自动化提示框
        '--log-level=30',  # 日志保存等级， 建议设置越好越好，要不然生成的日志占用的空间会很大 30为warning级别
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',  # UA
        # '--single-process',
        '--disable-gpu',
        '--no-sandbox',  # 关闭沙盒模式
        '--start-maximized',  # 窗口最大化模式
        # '--proxy-server=127.0.0.1:1080'
        # '--window-size=1920,1080',  # 窗口大小
        # '--proxy-server=http://localhost:1080'  # 代理
        # '--enable-automation'
    ],
}

JS_TEXT = """
    () =>{
        Object.defineProperties(navigator, { webdriver:{ get: () => false } });
        window.navigator.chrome = { runtime: {},  };
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        Object.defineProperty(navigator, 'plugins',   { get: () => [1, 2, 3, 4, 5,6], });
    }
    """

SELECTOR = "button.lmt__translations_as_text__text_btn"

BROWSER = None

text = '我喜欢在一起'


async def translator(text: str,
                     lang_tgt: str = 'ZH',
                     lang_src: str = 'EN',
                     detect: bool = False) -> tuple:
    time_start = time.time()
    global BROWSER
    BROWSER = await launch(args=PARMS['args'],
                           handleSIGINT=False,
                           handleSIGTERM=False,
                           handleSIGHUP=False)
    page = await BROWSER.newPage()
    await page.evaluateOnNewDocument(JS_TEXT)  # 本页刷新后值不变，自动执行js
    await page.goto(
        f'https://www.deepl.com/en/translator#{lang_src.upper()}/{lang_tgt.upper()}/{text}'
    )
    # await page.waitForSelector(SELECTOR, {'visible':True})
    # await page.waitForFunction(
    #     'document.querySelector("#dl_translator > div.lmt__text > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--target > div.lmt__textarea_container.halfViewHeight > div.lmt__translations_as_text > p.lmt__translations_as_text__item.lmt__translations_as_text__main_translation > button.lmt__translations_as_text__text_btn").innerText.length > 0'
    #     );
    await page.waitForFunction(
        'document.querySelector("button.lmt__translations_as_text__text_btn").textContent.length >0'
    )
    element = await page.querySelector(SELECTOR)
    result = await page.evaluate('(element) => element.textContent', element)
    time_end = time.time()
    # await page.screenshot({'path': './deepl.png','x':0,'y':0,'width':300,'height':300})
    await BROWSER.close()
    print(result, time_end - time_start)
    return result


def trans_auto(text):
    return translator(text, 'zh')


if __name__ == '__main__':
    text = '测试'
    try:
        print('Start running...')
        asyncio.get_event_loop().run_until_complete(translator(text))
    except KeyboardInterrupt as k:
        print('\nKey pressed to interrupt...')
