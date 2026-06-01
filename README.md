# Isaac Sim / 로봇 학습 스터디

이 워크스페이스는 Isaac Sim 기반 로봇 학습 업무를 1단계부터 순서대로 공부하기 위한 자료입니다.

최종 목표는 아래 작업들을 직접 설계하고 테스트할 수 있는 수준까지 가는 것입니다.

- Isaac Sim / MuJoCo 기반 모바일 매니퓰레이터 시뮬레이션 환경 구축
- 도메인 랜덤화
- 합성 데이터 자동 생성
- BC, ACT, Diffusion Policy 같은 모방학습
- PPO, SAC 기반 강화학습
- Sim-to-Real 전이
- VLA/RFM 스타일 정책 평가 벤치마크
- 대규모 합성 데이터 생성 및 학습 파이프라인

## 시작 순서

1. [전체 학습 로드맵](docs/isaac-sim-learning-roadmap.md)
2. [1단계: 기초](docs/stage-01-foundations.md)

## 1단계 실습 실행

```bash
python3 exercises/stage01_transforms_and_kinematics.py
```

실행하면 좌표 변환, 2-link 로봇팔의 순기구학/역기구학 결과가 출력되고, `outputs/stage01_2link_arm.png` 그림이 생성됩니다.
