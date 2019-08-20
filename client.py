import sys
import requests
import datetime
import json
import base64

def demo():
  _type = sys.argv[1]

  url = 'http://localhost:8888/{}'.format(_type)
  date = str(datetime.datetime.now())

  if _type == 'ImageHandler':
    files = {'uploadFile':open('./{}'.format('send.jpg'), 'rb')}
    r = requests.post(url, files=files, headers={'time':date}, timeout=5)
    j = json.loads(r.text)

    print('Recv: {}:{}'.format(j['type'], j['result']))
    with open('recv.jpg', 'wb') as f:
      f.write(base64.b64decode(j['data']))
    print('Save file ok, recv.jpg')
  
  if _type == 'TextHandler':
    r = requests.post(url,headers={'time':date}, data={'msg':"Hello World"}, timeout=5)
    j = json.loads(r.text)

    print('Recv: {}:{}'.format(j['type'], j['result']))
    print('Echo data: {}'.format(j['data']))

if __name__ == "__main__":
  demo()
