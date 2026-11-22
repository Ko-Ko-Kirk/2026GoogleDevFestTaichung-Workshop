"""台中場的本機防護練習與歷次雲端實測回放。"""
import argparse
import hashlib
import hmac
import json
from pathlib import Path

from devfest_security.common import Blocked
from devfest_security.policy import EXPENSES, authorize

EXAMPLES = Path(__file__).resolve().parent / 'examples'

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def manifest_digest(value):
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode()).hexdigest()

def verify_tools(discovered, approved):
    if not hmac.compare_digest(manifest_digest(discovered), manifest_digest(approved)):
        raise Blocked('工具清單與核准版本不同，停止使用這份清單。')

def local_expense(expense_id):
    # 固定用 Alice 示範。身分由程式提供，使用者僅能選擇要查的單號。
    authorize('alice', 'get_expense', {'expense_id': expense_id})
    return EXPENSES[expense_id]

def main():
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest='command', required=True)
    check = commands.add_parser('check', help='本機檢查 Alice 的讀取權限')
    check.add_argument('expense_id', choices=['EXP-ALICE', 'EXP-BOB'])
    manifest = commands.add_parser('manifest', help='比對輸入工具清單和教材核准版本')
    manifest.add_argument('candidate', type=Path)
    replay = commands.add_parser('replay', help='讀取歷次實測存檔')
    replay.add_argument('case', choices=['alice', 'bob', 'cloud'])
    args = cli.parse_args()
    try:
        if args.command == 'check':
            print(json.dumps(local_expense(args.expense_id), ensure_ascii=False, indent=2))
        elif args.command == 'manifest':
            verify_tools(read_json(args.candidate), read_json(EXAMPLES / 'approved-tools.json'))
            print('工具清單符合核准版本。')
        elif args.case == 'cloud':
            print(json.dumps(read_json(EXAMPLES / 'cloud-summary.json'), ensure_ascii=False, indent=2))
        else:
            run = read_json(EXAMPLES / 'hydrogen-stage.json')['runs'][args.case]
            print(json.dumps(run, ensure_ascii=False, indent=2))
    except Blocked as exc:
        print(f'拒絕：{exc}')
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
