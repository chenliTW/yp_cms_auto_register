from flask import Flask,render_template,request,session,url_for,redirect

import os,requests
from datetime import timedelta
from bs4 import BeautifulSoup

import reg_cms

app=Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)


def check_login(sid,cid,bir):
    res = requests.get('http://www.yphs.tp.edu.tw/tea/tu2.aspx')
    soup = BeautifulSoup(res.text, "lxml")
    VIEWSTATE=soup.find(id="__VIEWSTATE")
    VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")
    EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")
    res=requests.post('http://www.yphs.tp.edu.tw/tea/tu2.aspx', allow_redirects=False, data = {'__VIEWSTATE':VIEWSTATE.get('value'),'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR.get('value'),'__EVENTVALIDATION':EVENTVALIDATION.get('value'),'chk_id':'學生／家長','tbx_sno':sid,'tbx_sid':cid,'tbx_sbir':bir,'but_login_stud':'登　　入'})
    cook=res.cookies['ASP.NET_SessionId']
    res=requests.get("http://www.yphs.tp.edu.tw/tea/hscore.aspx",cookies={"ASP.NET_SessionId":cook})
    name=res.text.split("登入者：")[1].split("</")[0]
    return name

@app.route('/',methods=["GET","POST"])
def reg():
	if request.method=="GET":
		return render_template("reg.html")
	else:
		sid=request.form.get('sid')
		cid=request.form.get('cid')
		bir=request.form.get('bir')
#		check_login(sid,cid,bir)
		try:
			name=check_login(sid,cid,bir)
			session.clear()
			session['sid']=request.form.get('sid')
			session['name']=name
			session.permanent = True
			return redirect("https://judge.le37.tw/register/2")
		except:
		        return '你輸入的登入資料有誤qq或是系統有問題<a href="./">重新登入</a>'

def regcms(name,user,passw):
	status=0
	try:
		status=reg_cms.reg_cms(name,user,passw)
	except:
		pass
	return status

@app.route('/2',methods=["GET","POST"])
def reg2():
	if 'sid' not in session:
		return redirect('https://judge.le37.tw/register/')
	if session['sid']=="None":
		return redirect('https://judge.le37.tw/register/')
	if request.method=="GET":
		return render_template("reg2.html",sid=session['sid'])
	else:
		status=regcms(session['name'],session['sid'],request.form.get("pass"))
		return "{}<br>帳:{}<br>密:{}<br><a href=\"https://judge.le37.tw\">去online judge</a>".format(status,session['sid'],request.form.get("pass"))
'''
@app.route('/s3cr3t',methods=["GET","POST"])
def s3cr3t():
	if request.method=="GET":
		return render_template("s3cr3t.html",sid="")
	else:
		if request.form.get("inv")=="qwertyyphsjudge":
                        status=regcms(request.form.get("name"),request.form.get("sid"),request.form.get("pass"))
                        return "{}<br>帳:{}<br>密:{}<br><a href=\"https://judge.le37.tw\">去online judge</a>".format(status,request.form.get("sid"),request.form.get("pass"))
		else:
			return "inv code not correct"
'''
if __name__=="__main__":
	app.config['SECRET_KEY']=os.urandom(24)
	app.run(port=5000)
