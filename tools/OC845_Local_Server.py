"""Local-only OC845 viewer. Python standard library; no installation needed."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import ipaddress, json, re, urllib.request, urllib.error

ROOT=Path(__file__).resolve().parent
HTML=ROOT/'OC845_Pocket_Tool_v2.html'
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Avoid logging camera addresses, paths or credentials.
        pass
    def send(self, code, data, typ):
        self.send_response(code)
        self.send_header('Content-Type',typ)
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path not in ('/','/index.html'):
            return self.send(404,b'Not found','text/plain')
        self.send(200,HTML.read_bytes(),'text/html; charset=utf-8')
    def do_POST(self):
        if self.path!='/api/read':
            return self.send(404,b'Not found','text/plain')
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<1 or n>8192: raise ValueError('Invalid request size')
            obj=json.loads(self.rfile.read(n))
            ip=obj['ip']; addr=ipaddress.IPv4Address(ip)
            if not addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_multicast: raise ValueError('Only private LAN camera IPv4 addresses allowed')
            path=obj['path']
            if not re.fullmatch(r'adm/(?:get_group\.cgi(?:\?group=[A-Za-z0-9_]+)?|get_ui_group\.cgi)',path): raise ValueError('Only read-only group paths allowed')
            user=str(obj.get('username',''))[:128]; password=str(obj.get('password',''))[:256]
            url='http://'+ip+'/'+path
            handlers=[urllib.request.ProxyHandler({})]
            if user:
                mgr=urllib.request.HTTPPasswordMgrWithDefaultRealm();mgr.add_password(None,'http://'+ip+'/',user,password)
                handlers += [urllib.request.HTTPBasicAuthHandler(mgr),urllib.request.HTTPDigestAuthHandler(mgr)]
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self,req,fp,code,msg,headers,newurl):
                    raise urllib.error.HTTPError(req.full_url,code,'Redirect blocked',headers,fp)
            opener=urllib.request.build_opener(*handlers,NoRedirect())
            req=urllib.request.Request(url,headers={'User-Agent':'OC845-Local-Pocket-Viewer/2.0'})
            with opener.open(req,timeout=6) as response:
                body=response.read(131073)
                if len(body)>131072: raise ValueError('Response too large')
                result={'ok':True,'status':response.status,'body':body.decode('utf-8','replace')}
        except urllib.error.HTTPError as e:
            result={'ok':False,'status':e.code,'error':'Camera returned HTTP '+str(e.code)+' (check login and camera IP)'}
        except Exception as e:
            result={'ok':False,'error':str(e)}
        self.send(200,json.dumps(result).encode('utf-8'),'application/json; charset=utf-8')
if __name__=='__main__':
    print('OC845 Pocket Tool: http://127.0.0.1:8765')
    print('Keep this window open; Ctrl+C to stop. Camera credentials are not saved.')
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
