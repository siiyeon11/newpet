"""
넥슨 메이플스토리 API 프록시 서버 (Python)
CORS 문제를 해결하기 위한 간단한 프록시 서버입니다.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import json
import os

class ProxyHandler(BaseHTTPRequestHandler):
    API_BASE_URL = 'https://open.api.nexon.com'
    
    def do_GET(self):
        # 헬스체크 엔드포인트
        if self.path == '/health' or self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'ok', 
                'message': '프록시 서버가 정상 작동 중입니다.',
                'path': self.path
            }).encode('utf-8'))
            return
        
        # API 프록시 요청 처리
        if self.path.startswith('/api/maplestory/'):
            self.handle_api_request()
        else:
            # 정적 파일 서비스 (index.html 등)
            self.serve_static_file()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-nxopen-api-key')
        self.send_header('Access-Control-Max-Age', '3600')
    
    def handle_api_request(self):
        try:
            # 경로에서 엔드포인트 추출
            # /api/maplestory/id?character_name=xxx -> id
            path_with_query = self.path.split('/api/maplestory/')[1]
            path_parts = path_with_query.split('?')
            endpoint = path_parts[0]
            query_string = path_parts[1] if len(path_parts) > 1 else ''
            
            # API Key 가져오기
            api_key = self.headers.get('x-nxopen-api-key') or self.headers.get('X-Nxopen-Api-Key')
            if not api_key or api_key.strip() == '':
                error_msg = {
                    'error': 'API Key가 필요합니다.',
                    'message': 'x-nxopen-api-key 헤더에 API Key를 포함해주세요.',
                    'status_code': 400
                }
                error_data = json.dumps(error_msg, ensure_ascii=False)
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(error_data.encode('utf-8'))
                print(f"[400 오류] API Key가 전달되지 않았습니다.")
                return
            
            # 넥슨 API URL 구성
            api_url = f"{self.API_BASE_URL}/maplestory/v1/{endpoint}"
            if query_string:
                api_url += f"?{query_string}"
            
            print(f"[프록시 요청] {api_url}")
            
            # 넥슨 API 호출
            req = urllib.request.Request(api_url)
            req.add_header('x-nxopen-api-key', api_key)
            
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = response.read().decode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(data.encode('utf-8'))
                    print(f"[응답 성공] {response.status}")
            except urllib.error.HTTPError as e:
                error_data = e.read().decode('utf-8')
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(error_data.encode('utf-8'))
                print(f"[응답 에러] {e.code}: {error_data[:100]}")
            except Exception as e:
                print(f"[오류] {str(e)}")
                self.send_error_response(500, f'서버 오류: {str(e)}')
                
        except Exception as e:
            print(f"[처리 오류] {str(e)}")
            import traceback
            traceback.print_exc()
            self.send_error_response(500, str(e))
    
    def serve_static_file(self):
        try:
            # 경로 정규화
            if self.path == '/' or self.path == '':
                file_path = 'index.html'
            else:
                file_path = self.path.lstrip('/').split('?')[0]  # 쿼리 제거
            
            # 보안: 상위 디렉토리 접근 방지
            if '..' in file_path:
                self.send_error_response(403, 'Forbidden')
                return
            
            # 파일 읽기
            if not os.path.exists(file_path):
                self.send_error_response(404, f'File not found: {file_path}')
                return
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Content-Type 설정
            content_type = 'text/html'
            if file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.json'):
                content_type = 'application/json'
            elif file_path.endswith('.png'):
                content_type = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(content)
            print(f"[파일 제공] {file_path} ({len(content)} bytes)")
            
        except FileNotFoundError:
            self.send_error_response(404, 'File not found')
        except Exception as e:
            print(f"[파일 오류] {str(e)}")
            self.send_error_response(500, str(e))
    
    def send_error_response(self, status_code, message):
        error_data = json.dumps({'error': message, 'status_code': status_code})
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(error_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        # 기본 로그 메시지는 print로만 출력
        pass

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProxyHandler)
    
    print("=" * 50)
    print(f"프록시 서버가 http://localhost:{port} 에서 실행 중입니다.")
    print(f"브라우저에서 http://localhost:{port} 을 열어주세요.")
    print("서버를 중지하려면 Ctrl+C를 누르세요.")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
        httpd.shutdown()

if __name__ == '__main__':
    run_server(8000)
