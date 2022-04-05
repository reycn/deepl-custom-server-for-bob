# from pypt import trans
import sys
from loguru import logger
from sanic import Sanic, response
from sanic.response import json
from sentry_sdk import capture_message, init
from sys import path as syspath
from configparser import ConfigParser
# from api.api import translator
from api.pypt import translator

app = Sanic("DeepL")
path = syspath[0] + '/config/config.ini'

try:
    cfg = ConfigParser()
    cfg.read(path)
    sentry = cfg.get('sentry', 'sdk')
    init(sentry, traces_sample_rate=1.0)
except Exception as e:
    logger.exception("Init:" + str(e))
    capture_message('Init: ' + str(e))
    exit()


@app.route('/', methods=["GET"])
async def index(request):
    print('DeepL API sevice is running.')
    return response.html(
        '<!DOCTYPE html><html lang="en"><meta charset="UTF-8"><div>DeepL API service is running<br>More on <a href="https://github.com/reycn/deepl-custom-server-for-bob">GitHub</a></div>'
    )


@app.route('/v2/translate', methods=["GET"])
async def get_translate(request, lang_tgt='ZH', lang_src='EN'):
    if request.args.get('lang_tgt'):
        lang_tgt = request.args.get('lang_tgt')
    if request.args.get('lang_src'):
        lang_src = request.args.get('lang_src')
    if request.args.get('text'):
        text = request.args.get('text')
        logger.info(f'[>>] {text}')
        try:
            # result = await trans(text, lang_tgt=lang_tgt, lang_src=lang_src) # headless
            result = await translator(text, lang_tgt=lang_tgt)  # API Cracked
            logger.info(f'[<<] [{lang_tgt}] {result}')
        except Exception as e:
            logger.exception("Trans:" + str(e))
            capture_message('Trans: ' + str(e))
            result = "API Error"
    else:
        result = "API Error"
        logger.error("API Error")
    return json(text_to_dict(result, lang_src))


@app.route('/v2/translate', methods=["POST"])
async def post_translate(request, lang_tgt='ZH', lang_src='EN'):
    if request.form.get('lang_tgt'):
        lang_tgt = request.form.get('lang_tgt')
    if request.form.get('lang_src'):
        lang_src = request.form.get('lang_src')
    if request.body:
        text = request.form.get('text')
        logger.info(f'[>>] {text}')
        try:
            # result = await trans(text, lang_tgt=lang_tgt, lang_src=lang_src) # headless
            result = await translator(text, lang_tgt=lang_tgt)  # API Cracked
            logger.info(f'[<<] [{lang_tgt}] {result}')
        except Exception as e:
            logger.exception("Trans:" + str(e))
            capture_message('Trans: ' + str(e))
            result = "API Error"
    else:
        result = "API Error"
        logger.error("API Error")
    return json(text_to_dict(result, lang_src))


def text_to_dict(string, lang_src):
    dct = {
        "translations": [{
            "detected_source_language": lang_src,
            "text": string
        }]
    }
    return dct


def start(argv):
    host = '0.0.0.0'
    if len(argv) >= 2:
        port = int(sys.argv[1])
    else:
        port = 80
    logger.info(f'[Start] {host} {port}')
    app.run(host=host, port=port)


if __name__ == '__main__':
    start(sys.argv)