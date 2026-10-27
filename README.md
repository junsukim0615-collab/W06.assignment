# W06.assignment

컴퓨터네트워크 6주차 Task 1·2 제출물. Task 3은 아직 수행하지 않았다.

## Task 1

Dijkstra 최단 비용 및 다음 홉 계산을 구현했다. 제공 검사 2개 통과, 도달 불가능한 노드·고립 노드·링크 단절 추가 확인 완료.

```powershell
cd w06-routing
python task1_linkstate.py --verify
python test_tasks.py --task 1
```

## Task 2

Windows 실제 traceroute(2026-10-24)와 Docker FRR 9.1.0 라우터 3대의 OSPF 실험(2026-10-27)을 수행했다.

| 요구사항 | 제출 자료 |
|---|---|
| A1: 국내·해외·애니캐스트 경로 | [traceroute.txt](w06-routing/out/traceroute.txt) |
| A2–A5: 경계 홉·대양 횡단·애니캐스트·별표 분석 | [observation.md](w06-routing/out/observation.md) |
| B1/B2: 세 라우터의 학습 경로 | [route-before.txt](w06-routing/out/route-before.txt) |
| B3: 장애 후 테이블 | [route-after.txt](w06-routing/out/route-after.txt) |
| B4/B5: 장애·복구 수렴 시간 | [reconverge.txt](w06-routing/out/reconverge.txt), [복구 테이블](w06-routing/out/route-restored.txt) |
| Hello/Dead 확인 | [ospf-interfaces.txt](w06-routing/out/ospf-interfaces.txt) |
| C1/C2: 비용 변경 전후 | [변경 전](w06-routing/out/route-cost-before.txt), [변경 후](w06-routing/out/route-cost-after.txt) |
| B2/B4/B5/C3 설명 | [observation.md](w06-routing/out/observation.md) |
| 제공 검사 | [task2-tests.txt](w06-routing/out/task2-tests.txt): 5 passed, 0 failed |

장애 재수렴 2.804초, 복구 13.546초, 비용 변경 2.716초. 각 단계에서 원격 루프백 6개의 예상 다음 홉을 두 번 연속 확인했다. 시간에는 명령 실행과 폴링 지연이 포함된다. 로컬 인터페이스 down 실험이므로 Dead 타이머 40초를 기다리는 Hello 소실 장애와 구별한다.

국내 대상은 목적지 도달에 실패했고, 해외 도메인은 CDN으로 연결되어 대양 횡단 구간·해저 케이블을 확인하지 못했다. 관측 한계는 답변에 명시했다. 제공 검사의 통과는 파일 검사 결과이며 모든 경로의 도달이나 지리적 위치를 입증하지 않는다.

## Task 2 재실행

Python 3와 Linux 컨테이너 모드의 Docker Desktop이 필요하다. 저장소 루트에서:

```powershell
cd w06-routing
python task2_measure.py trace
python task2_ospf.py up
python task2_ospf.py measure
python task2_measure.py verify
```

상세 안내: [TASK2-RUN.md](w06-routing/TASK2-RUN.md). Windows에서 사용한 Python 측정 도구는 원본 `scenario.sh`를 대신해 인터페이스를 자동 식별하고 세 라우터를 모두 검증한다. 재실행하면 기존 실측 파일이 갱신된다.

VS Code에서 저장소 루트를 열고 Run and Debug의 `Week 6 - Verify Task 2`를 선택해 F5를 누른다. 원본 과제: [w06-routing](https://github.com/codingchild2424/2026-lecture-network-practice/tree/main/w06-routing).
