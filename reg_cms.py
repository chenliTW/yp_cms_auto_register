import requests


def reg_cms(name,username,password):
    con=requests.Session()
    res=con.get("https://judge.le37.tw/admin/login?next=/users/add").text
    xsrf=res.split("name=\"_xsrf\" value=\"")[1].split("\"/>")[0]
    data={
        "_xsrf":xsrf,
        "next":"/users/add",
        "username":"bot",
        "password":"C5MsCBbk2YRE"
    }
    res=con.post("https://judge.le37.tw/admin/login",data=data).text
    xsrf=res.split("name=\"_xsrf\" value=\"")[2].split("\"/>")[0]
    files={
        "_xsrf":(None,xsrf),
        "first_name":(None,name[:1]),
        "last_name":(None,name[1:]),
        "username":(None,username),
        "password":(None,password),
        "method":(None,"bcrypt"),
        "email":(None,""),
        "timezone":(None,""),
        "preferred_languages":(None,"")
    }
    res=con.post("https://judge.le37.tw/admin/users/add",files=files)
    user_url=res.url
    xsrf=res.text.split("name=\"_xsrf\" value=\"")[2].split("\"/>")[0]
    data={
        "_xsrf":xsrf,
        "contest_id":"1"
    }
    res=con.post(user_url+"/add_participation",data=data).text
    return res.status_code


if __name__=="__main__":
    reg_cms("陳","107","password")
