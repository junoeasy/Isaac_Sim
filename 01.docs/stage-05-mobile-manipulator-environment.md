# 5단계: 모바일 매니퓰레이터 환경 구축

## 목적

모바일 베이스와 로봇팔이 결합된 환경을 만들고, navigation과 manipulation이 연결된 task를 구성하는 단계입니다. 최종 목표는 scripted controller로 pick-and-place를 끝까지 수행하는 것입니다.

## 공부할 내용

### 1. 모바일 베이스

공부할 내용:

- differential drive
- holonomic base
- base frame
- odometry
- local/global pose

테스트:

- base를 목표 위치로 이동
- yaw 방향 제어
- 속도 제한 적용
- 장애물과 충돌 여부 확인

### 2. 로봇팔과 Gripper

공부할 내용:

- arm joint control
- end-effector pose
- gripper open/close
- pre-grasp pose
- grasp pose
- lift pose

테스트:

- end-effector를 목표점으로 이동
- gripper 열기/닫기
- 물체 위 pre-grasp pose로 이동
- 물체를 집고 들어 올리기

### 3. Base와 Arm의 결합

공부할 내용:

- base frame과 arm base frame 관계
- mobile manipulation workspace
- 접근 가능 영역
- task state machine

테스트:

- base를 물체 근처로 이동
- arm이 닿는 거리인지 확인
- base 이동 후 arm pick 수행
- 실패 조건 기록

### 4. Scripted Expert Policy

공부할 내용:

- rule-based controller
- finite state machine
- waypoint trajectory
- retry logic

테스트:

- approach
- pre-grasp
- grasp
- lift
- place
- release

## 실습 목표

```text
모바일 베이스가 물체 근처로 이동하고,
로봇팔이 물체를 집어 지정 위치에 놓는 scripted task를 만든다.
```

## 완료 체크리스트

- [ ] base pose와 arm end-effector pose를 구분할 수 있다.
- [ ] base 이동과 arm 조작을 순서대로 연결할 수 있다.
- [ ] scripted pick-and-place state machine을 만들 수 있다.
- [ ] 성공/실패 조건을 로그로 남길 수 있다.
- [ ] 실패 case를 보고 원인을 분류할 수 있다.

## 다음 단계와 연결

scripted expert가 있어야 이후 합성 데이터 생성과 모방학습을 할 수 있습니다. 먼저 사람이 만든 규칙 기반 정책으로 task를 안정적으로 수행하게 만든 뒤, 그 trajectory를 학습 데이터로 사용합니다.
