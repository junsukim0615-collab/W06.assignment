# W06.assignment

컴퓨터네트워크 6주차 Task 1 — Link State Routing

## 완료 내용

- Dijkstra 최단 비용 계산과 포워딩 테이블 구현
- 동일 비용 경로 선택 규칙 및 u-x 단절 전후 분석
- VS Code에서 `--verify` 실행: `all ok`
- 제공 Task 1 검사: `2 passed, 0 failed, 0 skipped`
- 도달 불가능한 노드, 고립 노드, 링크 단절 후 거리·다음 홉 추가 확인

## 실행

```bash
cd w06-routing
python task1_linkstate.py --verify
python test_tasks.py --task 1
```

VS Code에서 저장소 폴더를 열고 Python 및 Python Debugger 확장이 설치된 환경에서 F5를 누르면 `Week 6 - Verify Task 1` 설정으로 검증한다.

## 답변과 결과

- [과제 답변](w06-routing/out/observation.md)
- [검증 출력](w06-routing/out/task1-verify.txt)
- [Task 1 테스트 출력](w06-routing/out/task1-tests.txt)
- [추가 확인 결과](w06-routing/out/task1-extra-checks.txt)

이 저장소는 Task 1 완료분이다. 제공 `test_tasks.py`는 전체 주차 검사 도구이므로 여기서는 `--task 1`로 실행한다.

과제 원본: [codingchild2424/2026-lecture-network-practice, w06-routing](https://github.com/codingchild2424/2026-lecture-network-practice/tree/main/w06-routing)
