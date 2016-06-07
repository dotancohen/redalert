#!/usr/bin/python3

import datetime
import json
import os
import re
import time
import urllib.request

from socket import timeout
from urllib.error import URLError



interesting_areas = [287, 288, 289, 291, 292, 297]
refresh_rate = 2



def main(interesting_areas, refresh_rate=1):

	url = 'http://www.oref.org.il/WarningMessages/alerts.json'
	last_data = ''
	affected_areas = []

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

			if len(interesting_areas)==0:
				os.system('beep')
				if data!=last_data:
					last_data = data
					print(current_time + str(data))
				continue

			affected_areas[:] = []
			for d in data:
				affected_area = d.split()[-1:][0]
				if affected_area.isdigit():
					affected_areas.append(int(affected_area))
				else:
					print('No number for this area: ' + str(d))
					continue

			for ia in interesting_areas:
				if ia in affected_areas:
					os.system('beep')
					if data!=last_data:
						last_data = data
						print(current_time + str(data))
					continue

			if data!=last_data:
				last_data = data

		except (URLError, timeout) as e:
			#print( current_time + 'Timeout, probably not a big deal.')
			pass
		except Exception as e:
			print( current_time + 'Exception: ' + str(e))

		time.sleep(refresh_rate)

	return True



if __name__ == '__main__':
	main(interesting_areas, refresh_rate)
