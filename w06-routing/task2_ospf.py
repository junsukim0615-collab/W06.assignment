"""Measure real FRR OSPF routes after link down, restoration and cost change.

Requires Docker Desktop with Linux containers. Only this Compose project's
three routers are changed. No simulated timing values are generated.
"""
import argparse
import datetime
import json
import shutil
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "out"
ROUTERS = ("r1", "r2", "r3")
LOOPS = {r: f"10.255.6.{i}" for i, r in enumerate(ROUTERS, 1)}
DOCKER = shutil.which("docker") or str(Path("C:/Program Files/Docker/Docker/resources/bin/docker.exe"))
DC = [DOCKER, "compose", "-p", "network-w06", "-f", str(ROOT / "compose.yml"), "--profile", "routing"]


def run(args):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=180)
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return result.stdout


def command(router, *args):
    return run(DC + ["exec", "-T", router, *args])


def vty(router, *commands):
    args = ["vtysh"]
    for cmd in commands:
        args += ["-c", cmd]
    output = command(router, *args)
    if "% Unknown command" in output or "% Ambiguous" in output:
        raise RuntimeError(output)
    return output


def discover():
    networks, interfaces = {}, {}
    for router in ROUTERS:
        cid = run(DC + ["ps", "-q", router]).strip()
        if not cid:
            raise RuntimeError(f"{router} is not running")
        data = json.loads(run([DOCKER, "inspect", cid]))[0]
        networks[router] = {n: v["IPAddress"] for n, v in data["NetworkSettings"]["Networks"].items()}
        addresses = json.loads(command(router, "ip", "-j", "-4", "address", "show"))
        interfaces[router] = {a["local"]: item["ifname"] for item in addresses for a in item.get("addr_info", [])}
    edges = {}
    for a in ROUTERS:
        for b in ROUTERS:
            if a == b:
                continue
            common = set(networks[a]) & set(networks[b])
            if len(common) != 1:
                raise RuntimeError(f"Expected one shared network: {a}, {b}")
            network = common.pop()
            edges[a, b] = (interfaces[a][networks[a][network]], networks[b][network])
    return edges


def capture(name):
    blocks = []
    for router in ROUTERS:
        blocks.append(f"===== {router} =====\n" + vty(router, "show ip route ospf", "show ip ospf neighbor"))
    (OUT / name).write_text("\n".join(blocks), encoding="utf-8")


def expected(edges, phase):
    result = {}
    for a in ROUTERS:
        for b in ROUTERS:
            if a == b:
                continue
            hop = b
            if phase == "cut" and {a, b} == {"r1", "r2"}:
                hop = "r3"
            if phase == "cost" and a == "r1" and b == "r3":
                hop = "r2"
            result[a, b] = edges[a, hop][1]
    return result


def correct(wanted):
    for a in ROUTERS:
        table = json.loads(vty(a, "show ip route ospf json"))
        for b in ROUTERS:
            if a == b:
                continue
            entries = table.get(LOOPS[b] + "/32", [])
            hops = {n.get("ip") for entry in entries for n in entry.get("nexthops", [])}
            if hops != {wanted[a, b]}:
                return False
    return True


def wait_routes(wanted, start, timeout=150):
    consecutive = 0
    first_match = None
    while time.perf_counter() - start < timeout:
        if correct(wanted):
            if consecutive == 0:
                first_match = time.perf_counter() - start
            consecutive += 1
            if consecutive >= 2:
                return first_match
        else:
            consecutive = 0
        time.sleep(0.5)
    raise TimeoutError("Expected next hops did not converge on all three routers")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("up", "measure", "down"))
    action = parser.parse_args().action
    OUT.mkdir(exist_ok=True)
    if action == "up":
        print(run(DC + ["up", "-d", "r1", "r2", "r3"]))
        return
    if action == "down":
        print(run(DC + ["down"]))
        return
    edges = discover()
    (OUT / "interface-map.json").write_text(json.dumps({f"{a}->{b}": value for (a, b), value in edges.items()}, indent=2), encoding="utf-8")
    for router in ROUTERS:
        command(router, "ip", "address", "replace", LOOPS[router] + "/32", "dev", "lo")
        for interface in sorted({value[0] for (a, _), value in edges.items() if a == router}):
            vty(router, "configure terminal", f"interface {interface}",
                "ip ospf cost 10", "ip ospf hello-interval 10", "ip ospf dead-interval 40")
    print("Waiting for initial OSPF convergence...", flush=True)
    wait_routes(expected(edges, "normal"), time.perf_counter())
    capture("route-before.txt")
    (OUT / "ospf-interfaces.txt").write_text("\n".join(f"===== {r} =====\n" + vty(r, "show ip ospf interface") for r in ROUTERS), encoding="utf-8")
    cut_interface = edges["r1", "r2"][0]
    cost_interface = edges["r1", "r3"][0]
    timings = {}
    try:
        start = time.perf_counter()
        command("r1", "ip", "link", "set", cut_interface, "down")
        timings["link_down_seconds"] = wait_routes(expected(edges, "cut"), start)
        capture("route-after.txt")
        print("Link down:", timings["link_down_seconds"], "seconds", flush=True)
        start = time.perf_counter()
        command("r1", "ip", "link", "set", cut_interface, "up")
        timings["restore_seconds"] = wait_routes(expected(edges, "normal"), start)
        capture("route-restored.txt")
        capture("route-cost-before.txt")
        print("Restored:", timings["restore_seconds"], "seconds", flush=True)
        start = time.perf_counter()
        vty("r1", "configure terminal", f"interface {cost_interface}", "ip ospf cost 100")
        timings["cost_change_seconds"] = wait_routes(expected(edges, "cost"), start)
        capture("route-cost-after.txt")
        print("Cost change:", timings["cost_change_seconds"], "seconds", flush=True)
        timings["measured_at"] = datetime.datetime.now().astimezone().isoformat()
        timings["method"] = "All six remote loopback routes must have the expected next hop in two consecutive polls; time records completion of first matching poll, including command and polling overhead."
        timings["failure_mode"] = "Local administrative link down: the local router can detect this immediately rather than waiting for its dead timer."
        timings["hello_seconds"] = 10
        timings["dead_seconds"] = 40
        (OUT / "reconverge.txt").write_text(json.dumps(timings, indent=2), encoding="utf-8")
        print("PASS: all three routers have the expected routes after every phase.")
    finally:
        command("r1", "ip", "link", "set", cut_interface, "up")
        vty("r1", "configure terminal", f"interface {cost_interface}", "ip ospf cost 10")


if __name__ == "__main__":
    main()
