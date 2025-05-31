import logging
import datetime
import requests
import config

logger = logging.getLogger(__name__)

def push_ntfy(token, body):
    url = f"{config.ntfy_host}/{token}"
    resp = requests.post(url, data=body)
    logger.debug(resp)

def notify(title, body, tag):
    if not config.tokens.get(tag, None):
        logger.debug("skip tag: %s", tag)
        return
    time_periods = config.dont_disturb_hours.get(tag, None)
    level = "timeSensitive"
    if time_periods:
        now = datetime.datetime.now()
        for period in time_periods:
            if period["begin"] <= now.hour < period["end"]:
                logger.debug("sleep time, slient: %s, %s, %s, %s", tag, period, title, body)
                level = "passive"
    # tag -> bark推送token
    logger.info("notify to bark, tag:%s, level:%s", tag, level)
    payload = {
            "title":title,
            "body":body,
            "url":"rocketchat://room",
            "level": level,
            "group":title,
            "isArchive":1,
            }
    url = f"{config.host}/{config.tokens[tag]}/"
    resp = requests.post(url, json=payload)
    logger.debug(resp)
    # ntfy
    push_ntfy(config.tokens[tag], body)

if __name__ == '__main__':
    # 设置日志级别
    logging.basicConfig(level=logging.DEBUG)
    
    # 测试push_ntfy功能
    test_token = "qPKzhYeHRTMidHxDMnRYEd"  # 替换为实际的token
    test_payload = "test"
    push_ntfy(test_token, test_payload) 