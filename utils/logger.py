import logging
logging.basicConfig(filename='logs/api_automation.log',
                    filemode='a',
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()
def log_request_response(request, response):
    logger.info(f"Request URL: {request.url}")
    logger.info(f"Request body: {getattr(request, 'body', None)}")
    logger.info(f"Response ({response.status_code}): {response.text}")

