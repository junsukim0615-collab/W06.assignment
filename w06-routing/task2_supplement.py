"""Capture additional real paths; destination names do not prove server location."""
import concurrent.futures
import datetime
import locale
from pathlib import Path
import subprocess
import argparse


def trace(target):
    command = ['tracert', '-4', '-h', '30', '-w', '1000', target]
    try:
        result = subprocess.run(command, capture_output=True, timeout=240)
        raw = result.stdout + result.stderr
        status = str(result.returncode)
    except subprocess.TimeoutExpired as exc:
        raw = (exc.stdout or b'') + (exc.stderr or b'')
        status = 'timeout; partial output'
    return f'===== {target} (exit {status}) =====\n' + raw.decode(locale.getpreferredencoding(False), errors='replace')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campus', action='store_true', help='Use only when physically connected to the campus network')
    args = parser.parse_args()
    targets = ['www.korea.ac.kr', 'www.stanford.edu', '1.1.1.1'] if args.campus else ['www.stanford.edu', 'www.mit.edu', 'www.berkeley.edu']
    lines = ['Measured: ' + datetime.datetime.now().astimezone().isoformat(),
             'Network: campus connection confirmed by user' if args.campus else 'Network: home/external, confirmed by user; not campus']
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(trace, targets):
            lines.append(result)
            print(result, flush=True)
    out = Path(__file__).resolve().parent / 'out'
    out.mkdir(exist_ok=True)
    path = out / ('traceroute-campus.txt' if args.campus else 'traceroute-supplement.txt')
    path.write_text('\n\n'.join(lines), encoding='utf-8')
    print('Saved:', path)
