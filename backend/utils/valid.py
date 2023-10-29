import re   

def checkEmail(email):
    if len(email) > 7:
        if re.match("^.+@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False

def checkIPV4(ip):
    if ip.count('.') == 3:
        ip = ip.split('.')
        for i in ip:
            if not i.isdigit():
                return False
            else:
                if not 0 <= int(i) <= 255:
                    return False
        return True
    return False