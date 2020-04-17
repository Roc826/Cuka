from aip import AipOcr
import re
APP_ID = '********'
API_KEY = '***********'
SECRET_KEY ='**************'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
def get_code(image_name):
    image = get_file_content(image_name)
    options = {}
    options["language_type"] = "ENG"
    res = client.basicAccurate(image, options)
    code=re.sub("[^\w]", "", res['words_result'][0]['words'])
    return code
