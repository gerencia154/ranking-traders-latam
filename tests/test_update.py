import io
import json
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/update.py'
VALID = {'status':'ok','date_modified':'2026-11-16','total':1,'strategies':[{'position':1,'strategy_alias':'Public alias','broker':'Example','platform':'MT5','tl_score':70,'tl_rating':'B','report_url':'https://trading-latam.com/auditor/report.php?slug='+'a'*24}]}

class Response(io.BytesIO):
    headers = {'Content-Type':'application/json'}

class UpdateTests(unittest.TestCase):
    def run_script(self, payloads):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'scripts').mkdir();(root/'data/historico').mkdir(parents=True)
            script=root/'scripts/update.py';shutil.copyfile(SCRIPT,script)
            (root/'README.md').write_text('<!-- TOP:INICIO -->old<!-- TOP:FIN -->')
            for name in ['ranking.json','ranking.csv']:(root/'data'/name).write_bytes(b'previous verified snapshot')
            before={str(f.relative_to(root)):f.read_bytes() for f in root.rglob('*') if f.is_file()}
            responses=[Response(json.dumps(x).encode() if isinstance(x,dict) else x) for x in payloads]
            with patch('urllib.request.urlopen',side_effect=responses) as fetch,patch('time.sleep'):
                error=None
                try:runpy.run_path(str(script),run_name='__main__')
                except Exception as exc:error=exc
            after={str(f.relative_to(root)):f.read_bytes() for f in root.rglob('*') if f.is_file()}
            return error,fetch.call_count,before,after

    def test_retries_html_then_publishes_valid_snapshot(self):
        error,calls,_,after=self.run_script([b'<html>temporary upstream response</html>',VALID])
        self.assertIsNone(error);self.assertEqual(calls,2)
        self.assertEqual(json.loads(after['data/ranking.json'])['total'],1)
        self.assertIn('data/historico/2026-11-16.csv',after)

    def test_exhausted_html_keeps_all_previous_files(self):
        error,calls,before,after=self.run_script([b'<html>not JSON</html>']*3)
        self.assertIsNotNone(error);self.assertEqual(calls,3);self.assertEqual(before,after)

    def test_upstream_error_payload_cannot_erase_ranking(self):
        bad={'status':'temporarily_unavailable','date_modified':'2026-11-16','total':0,'strategies':[]}
        error,_,before,after=self.run_script([bad]*3)
        self.assertIsNotNone(error);self.assertEqual(before,after)

    def test_partial_payload_cannot_publish_inconsistent_total(self):
        error,_,before,after=self.run_script([dict(VALID,total=2)]*3)
        self.assertIsNotNone(error);self.assertEqual(before,after)

    def test_invalid_date_cannot_select_history_path(self):
        error,_,before,after=self.run_script([dict(VALID,date_modified='../bad')]*3)
        self.assertIsNotNone(error);self.assertEqual(before,after)

    def test_legitimate_empty_public_ranking_is_allowed(self):
        payload={'status':'ok','date_modified':'2026-11-16','total':0,'strategies':[]}
        error,_,_,after=self.run_script([payload]);self.assertIsNone(error)
        self.assertEqual(json.loads(after['data/ranking.json'])['strategies'],[])

if __name__=='__main__':unittest.main()
