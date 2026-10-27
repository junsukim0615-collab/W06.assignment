"""Capture real traceroutes on Windows and run the supplied Task 2 checks."""
import argparse
import concurrent.futures
import datetime
import locale
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
TARGETS = ("www.korea.ac.kr", "www.stanford.edu", "1.1.1.1")


def trace(target):
    command = ["tracert", "-4", "-h", "30", "-w", "1000", target]
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=240)
    output = result.stdout.decode(locale.getpreferredencoding(False), errors="replace")
    return target, result.returncode, output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("trace", "verify"))
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.action == "trace":
        if sys.platform != "win32":
            parser.error("This capture command uses Windows tracert.")
        print("Measuring three real network paths (up to 30 hops)...", flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(trace, TARGETS))
        sections = ["Measured: " + datetime.datetime.now().astimezone().isoformat()]
        for target, code, output in results:
            section = f"\n===== {target} (exit {code}) =====\n{output}"
            sections.append(section)
            print(section, flush=True)
        (OUT / "traceroute.txt").write_text("\n".join(sections), encoding="utf-8")
        print("Saved out/traceroute.txt. Timeouts are recorded, not treated as replies.")
        return 0
    result = subprocess.run([sys.executable, str(HERE / "test_tasks.py"), "--task", "2"],
                            cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode(locale.getpreferredencoding(False), errors="replace")
    print(output)
    (OUT / "task2-tests.txt").write_text(output, encoding="utf-8")
    print("This checks file format only. OSPF timings and observations require real measurements.")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
