# -*- coding: utf-8 -*-
"""
自制装备制作器 —— 后端（Python 标准库，零依赖）。

启动:
    python crafter/backend/server.py [--port 8765]

接口:
    GET  /api/meta       物品种类、词条列表、星级默认值
    POST /api/search     组合搜索
    POST /api/evaluate   计算一个指定的 6 原料配方
"""
from __future__ import print_function

import argparse
import json
import mimetypes
import os
import posixpath
import sys
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                 # crafter/
FRONTEND = os.path.join(ROOT, 'frontend')

sys.path.insert(0, HERE)
import engine as E  # noqa: E402

DS = E.Dataset()
LOCK = threading.Lock()

CONTENT_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.ico': 'image/x-icon',
}


def meta_payload():
    counts = {}
    for ing in DS.items:
        for k in ing['ids']:
            counts[k] = counts.get(k, 0) + 1
    ids = [{'key': k, 'label': DS.id_labels.get(k, k), 'count': counts.get(k, 0)}
           for k in DS.id_keys]
    ids.sort(key=lambda x: (-x['count'], x['key']))
    types = []
    for t in E.ITEM_TYPES:
        types.append({
            'id': t[0], 'cn': t[1], 'en': t[2], 'kind': t[3],
            'professions': t[4],
        })
    return {
        'types': types,
        'baseTiers': E.BASE_TIERS,
        'defaultBaseTable': list(E.DEFAULT_BASE_TABLE),
        'defaultCharges': E.DEFAULT_BASE_CHARGES,
        'tierNames': E.TIER_NAMES,
        'tierColors': E.TIER_COLORS,
        'skills': [{'key': k, 'cn': z, 'en': e} for k, z, e in E.SKILLS],
        'professions': {k: {'zh': E.PROF_CN.get(k, k), 'en': E.PROF_EN.get(k, k)}
                        for k in E.PROF_CN},
        'ids': ids,
        'ingredientCount': len(DS.items),
        'ingredients': [{'id': i['id'], 'name': i['name'], 'tier': i['tier'],
                         'professions': i['professions'], 'durability': i['durability']}
                        for i in DS.items],
        'grid': {'rows': E.ROWS, 'cols': E.COLS},
    }


class Handler(BaseHTTPRequestHandler):
    server_version = 'wynnbd-crafter/1.0'

    # -- 工具
    def _send(self, code, body, ctype='application/json; charset=utf-8'):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode('utf-8')
        elif isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json_body(self):
        length = int(self.headers.get('Content-Length') or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode('utf-8'))

    def log_message(self, fmt, *args):
        sys.stdout.write('%s - %s\n' % (self.address_string(), fmt % args))

    # -- 路由
    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        try:
            if path == '/api/meta':
                return self._send(200, meta_payload())
            if path == '/api/health':
                return self._send(200, {'ok': True, 'ingredients': len(DS.items)})
            return self._serve_static(path)
        except Exception:
            traceback.print_exc()
            self._send(500, {'error': 'internal', 'detail': traceback.format_exc(limit=2)})

    def do_POST(self):
        path = unquote(urlparse(self.path).path)
        try:
            body = self._json_body()
            if path == '/api/search':
                with LOCK:
                    res = E.Searcher(DS, body).run()
                return self._send(200, res)
            if path == '/api/evaluate':
                ids = body.get('ingredients') or []
                if len(ids) != 6:
                    return self._send(400, {'error': '需要 6 个原料'})
                missing = [x for x in ids if x not in DS.by_id]
                if missing:
                    return self._send(400, {'error': '未知原料: %s' % ', '.join(missing)})
                return self._send(200, E.evaluate(DS, body, ids))
            return self._send(404, {'error': 'not found'})
        except Exception:
            traceback.print_exc()
            self._send(500, {'error': 'internal', 'detail': traceback.format_exc(limit=2)})

    def _serve_static(self, path):
        if path in ('/', ''):
            path = '/index.html'
        rel = posixpath.normpath(path).lstrip('/')
        if rel.startswith('..') or os.path.isabs(rel):
            return self._send(403, {'error': 'forbidden'})
        full = os.path.join(FRONTEND, *rel.split('/'))
        if not os.path.isfile(full):
            return self._send(404, 'Not Found', 'text/plain; charset=utf-8')
        ext = os.path.splitext(full)[1].lower()
        with open(full, 'rb') as f:
            data = f.read()
        self._send(200, data, CONTENT_TYPES.get(ext, 'application/octet-stream'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=8765)
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--open', action='store_true', help='启动后自动打开浏览器')
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    url = 'http://%s:%d/' % (args.host, args.port)
    print('原料库: %d 个' % len(DS.items))
    print('服务已启动: %s' % url)
    if args.open:
        import threading
        import webbrowser
        threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\n已停止')


if __name__ == '__main__':
    main()
