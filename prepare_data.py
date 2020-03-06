from collections import defaultdict

from urllib.request import urlopen

URL = 'https://raw.githubusercontent.com/ondata/covid19italia/master/publication/provinceArchivio.csv'

f = urlopen(URL)
content = f.read().decode('utf-8')

data = {}

datetimes = set()

first_line = True
for line in content.splitlines():
	#line = str(line)
	#print(line)

	if first_line:
		first_line = False
		continue

	# TODO: logica per skippare una linea

	if 'verifica' in line.lower():
		continue
	if 'aggiorna' in line.lower():
		continue

	provincia, numero, regione, datetime = line.split(',')

	# TODO: logica per skippare una linea in base a qualche valore non valido

	datetimes.add(datetime)

	if provincia not in data:
		data[provincia] = {}
	
	data[provincia][datetime] = numero
	data[provincia]['regione'] = regione

datetimes = sorted(datetimes)

# HEADER
print("provincia,regione," + ",".join(datetimes))

datetime_history = defaultdict(int)
for provincia in data:
	line = provincia + ',' + data[provincia]['regione']

	for datetime in datetimes:
		if datetime in data[provincia]:
			line = line + ',' + str(data[provincia][datetime])
			datetime_history[provincia] = str(data[provincia][datetime])
		else:
			# se per caso mi manca il dato uso l'ultimo disponibile
			# se non c'è l'ultimo dato disponibile uso zero perché è defaultdict
			line = line + ',' + str(datetime_history[provincia])

	print(line)