# Task 2 실행 안내

## Part A: 실제 Windows 경로 추적

```powershell
python task2_measure.py trace
```

최대 30홉, 홉당 응답 대기 1초로 과제의 세 대상을 측정한다. 원본은 `out/traceroute.txt`에 저장된다. 명령 종료 코드가 0이어도 목적지 도달 여부는 출력으로 별도 판단해야 한다.

## Part B/C: Docker 기반 실제 OSPF 실험

Docker Desktop이 Linux 컨테이너 모드로 실행 중이어야 한다.

```powershell
python task2_ospf.py up
python task2_ospf.py measure
python task2_measure.py verify
```

- FRR 9.1.0 공식 이미지 주소 `quay.io/frrouting/frr:9.1.0`을 사용한다. 원본 Compose의 Docker Hub 태그를 공식 배포 위치로 수정했다.
- `network-w06` Compose 프로젝트의 라우터 3대만 기동한다.
- Docker에서 실제 IP와 인터페이스를 읽어 링크를 식별한다. eth0/eth1 순서를 가정하지 않는다.
- 각 라우터에 실험용 루프백 주소 10.255.6.1/32~10.255.6.3/32를 추가한다. 다른 두 라우터의 루프백 경로는 OSPF로 학습되어야 한다.
- 링크 비용은 10, Hello/Dead는 10/40초로 명시하여 실행 중 설정을 기록한다.
- 초기 수렴, r1-r2 단절, 복구, r1-r3 방향 비용 100 변경을 순서대로 수행한다.
- 각 단계마다 라우터 3대의 원격 루프백 경로 6개가 예상 다음 홉과 일치하는지 두 번 연속 확인한다. 첫 번째 일치 관측이 끝난 시간을 기록하며, 명령 실행·폴링 지연이 포함된다.
- 이 실험의 단절은 로컬 인터페이스를 내리는 방식이다. 로컬 라우터는 이를 즉시 감지할 수 있으므로 무조건 Dead 타이머만큼 기다린다고 해석하면 안 된다.
- 완료 또는 예외 발생 시 링크를 복구하고 변경한 비용을 10으로 되돌린다.

추가 산출물: `interface-map.json`, `ospf-interfaces.txt`, `route-restored.txt`, `route-cost-before.txt`, `route-cost-after.txt`.

실험 종료 후 컨테이너를 정리하려면 `python task2_ospf.py down`을 실행한다.

## 검증 화면

VS Code에서 상위 `network-practice-w06` 폴더를 열고 Run and Debug의 `Week 6 - Verify Task 2`를 선택해 F5로 실행한다. 결과 파일이 없으면 FAIL로 표시된다. 제공 검사는 파일 형식만 확인하며, 실제 경로 및 시간 측정은 `task2_ospf.py measure`가 수행한다.

참고: [FRR 9.1 공식 릴리스](https://frrouting.org/release/9.1/), [OSPF 동작 설명](https://docs.frrouting.org/en/latest/ospfd.html).
