# W06.assignment

컴퓨터네트워크 6주차 Task 1·2·3 실험 및 구현 보고서.

## 보고서

- [관찰 요약](w06-routing/out/observation.md): 과제별 2–3줄
- [통합 상세 보고서](w06-routing/out/answers-detailed.md): 모든 요구사항의 답변, 측정 환경, 근거와 해석

Task 2는 최초 교외 측정과 추가 학교망 측정을 구분했다. 캠퍼스의 정확한 출구 홉과 대양 횡단 케이블은 관측 자료로 확정하지 못했으며, 보고서에 근거와 한계를 설명했다.

## 결과 자료

| 항목 | 자료 |
|---|---|
| Task 1 | [검증 결과](w06-routing/out/task1-verify.txt) |
| Task 2 경로 추적 | [최초 교외](w06-routing/out/traceroute.txt), [학교망](w06-routing/out/traceroute-campus.txt), [학교 국내 초기 추적](w06-routing/out/traceroute-campus-domestic-initial.txt), [교외 추가](w06-routing/out/traceroute-supplement.txt) |
| OSPF 장애·복구 | [장애 전](w06-routing/out/route-before.txt), [장애 후](w06-routing/out/route-after.txt), [복구 후](w06-routing/out/route-restored.txt), [시간](w06-routing/out/reconverge.txt) |
| OSPF 비용 변경 | [변경 전](w06-routing/out/route-cost-before.txt), [변경 후](w06-routing/out/route-cost-after.txt), [Hello/Dead](w06-routing/out/ospf-interfaces.txt) |
| Task 3 | [벤치마크](w06-routing/out/bench.txt), [추가 검사](w06-routing/out/task3-extra-checks.txt) |
| 전체 검증 | [9 passed, 0 failed, 1 skipped](w06-routing/out/all-tests.txt), [제출 형식 검사](w06-routing/out/submission-check.txt) |

Task 3는 1,000개 이벤트 오답 0회, SPF 1,001→363회(63.74% 감소, good)다. skipped는 사람이 평가하는 실행 시간 설명 항목이며 보고서에 작성했다.

## 실행

Python 3가 필요하며 OSPF 재측정에는 Linux 컨테이너 모드의 Docker Desktop이 필요하다.

```powershell
cd w06-routing
python task1_linkstate.py --verify
python bench.py --yours
python test_tasks.py
python ../check.py w06
```

OSPF 재측정은 [TASK2-RUN.md](w06-routing/TASK2-RUN.md)를 따른다. 학교망에서 경로를 다시 수집하려면 `python task2_supplement.py --campus`를 실행한다. 재측정은 해당 출력 파일을 갱신한다.

VS Code에서 저장소 루트를 열고 Run and Debug의 Task 1 검증, Task 2 검증 또는 Task 3 벤치마크 구성을 선택해 F5로 실행한다.

[과제 원본](https://github.com/codingchild2424/2026-lecture-network-practice/tree/main/w06-routing)
