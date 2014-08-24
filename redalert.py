#!/usr/bin/python3

import datetime
import json
import os
import re
import time
import urllib.request

from socket import timeout
from urllib.error import URLError


def main():

    url = 'http://www.oref.org.il/WarningMessages/alerts.json'
    last_data = ''
    affected_areas = []
    interested_areas = [287, 288, 289, 291, 292, 297]

    while True:
        current_time = datetime.datetime.now().strftime('%H:%M:%S') + ' '
        try:
            response = urllib.request.urlopen(url, timeout=1).read()

            # 65279 is the zero-width no-break space, also used
            # as and more commonly known as the BOM!
            response_decoded = re.sub(chr(65279), '', response.decode('utf-16le'))

            predata = json.loads(response_decoded)
            data = predata['data']

            if len(data)==0:
                last_data = ''
                continue

            affected_areas[:] = []
            for d in data:
                affected_area = int(d.split()[-1:][0])
                affected_areas.append(affected_area)
                #print(current_time + 'Affected area: ' + str(type(affected_area)) + str(affected_area))

            for ia in interested_areas:
                if ia in affected_areas:
                    os.system('beep')
                    if data!=last_data:
                        last_data = data
                        print(current_time + str(data))
                    continue

            if data!=last_data:
                last_data = data
                print( current_time + 'Different area: ' + str(data))

        except URLError as e:
            print( current_time + 'Timeout A, probably not a big deal.')
        except timeout as e:
            print( current_time + 'Timeout B, probably not a big deal.')
        except Exception as e:
            print( current_time + 'Exception: ' + str(e))

        time.sleep(1)

    return True



if __name__ == '__main__':
    main()
