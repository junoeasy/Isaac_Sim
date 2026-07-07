# Joint, Drive, 회전축 설정

## USD에서 서보는 어떻게 구현되는가

CAD의 `Servo` mesh가 직접 토크를 내는 것이 아니다.

Isaac Sim/PhysX에서는 링크 사이의 `RevoluteJoint`에 `Drive`를 붙여 서보처럼 만든다.

```text
Servo mesh = 보기용
RevoluteJoint + Angular Drive = 실제 회전/토크 구현
```

Drive 주요 값:

```text
Target Position = 목표 각도
Target Velocity = 목표 속도
Stiffness       = 목표 각도로 당기는 강도
Damping         = 움직임을 감쇠하는 정도
Max Force       = 최대 토크/힘
```

## 반동이 생기는 이유

Drive는 이상적인 위치 고정이 아니라 PD 제어기처럼 동작한다.

```text
Stiffness가 크고 Damping이 부족함
-> 목표 각도를 지나침
-> 되돌아옴
-> 반동/진동처럼 보임
```

서보처럼 덜 튀게 하려면:

```text
Stiffness 낮추기 또는 적당히 유지
Damping 크게 올리기
Max Force 충분히 크게
Target Velocity = 0
```

테스트한 smooth 값:

```text
Stiffness: 800
Damping: 2500
Max Force: 100000
```

강하게 위치를 잡고 싶을 때 시작값:

```text
Stiffness: 10000
Damping: 3000
Max Force: 1000000
```

## 회전축 맞추는 법

Revolute Joint에서 중요한 값:

```text
Axis = 어느 방향 축으로 회전할지
Local Pos 0 / Local Pos 1 = 회전 중심 위치
```

축 색:

```text
X = 빨강
Y = 초록
Z = 파랑
```

서보 출력축이 바라보는 방향이 joint axis이다.

```text
출력축이 좌우 방향이면 X
출력축이 앞뒤 방향이면 Y
출력축이 위아래 방향이면 Z
```

검증 방법:

```text
1. joint 선택
2. Axis를 X/Y/Z 중 하나로 설정
3. Target Position을 20 또는 30으로 설정
4. Play
5. 서보 축 중심으로 자연스럽게 돌면 맞음
```

판단:

```text
회전축 중심은 맞고 방향만 반대
-> Target Position 부호를 반대로 사용한다. 예: 30 대신 -30

문짝처럼 엉뚱한 방향으로 회전
-> Axis가 틀림

부품이 축 중심이 아니라 떨어진 곳을 중심으로 돈다
-> Local Pos 0 / Local Pos 1 위치가 틀림
```

## 현재 joint2 상태

현재 `joint2_shoulder_test`는 아래 위치와 축으로 테스트 중이다.

```text
joint2 위치: (-17.5, -29.4, 275.0)
Axis: X
```

이 축이 이상하면 `Y` 또는 `Z`로 바꿔 테스트한다.
