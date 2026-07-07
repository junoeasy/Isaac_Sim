# Isaac Sim 6DOF Arm 작업 대화 정리

이 폴더는 `6 dof arm 3D.STEP`를 Isaac Sim에서 구동 가능한 로봇 USD로 만들기 위해 Codex와 진행한 대화 내용을 정리한 기록이다.

## 원본 파일

- STEP 원본: `/home/junho/isaac/6 dof arm 3D.STEP`
- STEP 변환 USD 원본: `/home/junho/isaac/6 dof arm 3D.usd`
- 편집 가능한 flat USD: `/home/junho/isaac/6 dof arm_editable_flat.usd`

## 현재 기준 파일

현재 링크 분류와 joint 테스트의 기준은 아래 파일들이다.

- 링크 색상/분류 기준: `/home/junho/isaac/6 dof arm_link_grouped_parent_to_base_v3.usd`
- joint2 테스트 최신 파일: `/home/junho/isaac/6 dof arm_joint2_test_parent_to_base_v6_fixed_base.usd`

## 핵심 결론

STEP에서 바로 가져온 USD는 CAD visual 모델이다. 이 상태에는 로봇 구동에 필요한 link, joint, mass, collider, drive가 없다.

따라서 Isaac Sim에서 구동하려면 다음 구조를 직접 만들어야 한다.

```text
base_link -- joint1 -- link1 -- joint2 -- link2 -- joint3 -- ...
```

서보모터 자체가 토크를 내는 것이 아니라, USD/PhysX에서는 `RevoluteJoint`의 `Drive`가 서보 역할을 한다.

## 현재까지 성공한 것

- STEP을 USD로 변환했다.
- CAD USD의 instance/prototype 구조 때문에 이동이 막혔고, `editable_flat` 파일로 풀었다.
- 링크별 색상 분류 파일을 만들었다.
- `tn___1_XF5i1JPa1g4X18n0`를 `base_link`로 옮긴 버전이 잘 동작했다.
- `tn__U_n9Bm0n0Z4m0`를 `link2`에서 `link1`으로 옮겼다.
- joint1 단독 테스트가 성공했다.
- joint2 테스트 파일을 만들었다.
- base가 떨어지는 문제를 `world_fixed_base` Fixed Joint로 해결했다.

## 남은 일

- joint2 축과 위치를 더 정확히 조정한다.
- joint3, joint4, joint5, joint6을 하나씩 추가 테스트한다.
- 전체 6DOF articulation 파일을 만든다.
- 실제 서보 스펙에 맞춰 drive stiffness, damping, max force를 조정한다.
- 볼트/너트류를 필요한 경우 visual용으로 각 링크에 분류한다.
