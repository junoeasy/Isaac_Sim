

Isaac Sim 설치하는 법 - Ubuntu 기준
https://docs.isaacsim.omniverse.nvidia.com/6.0.0/installation/download.html
링크에서 Linux Isaac Sim 설치
[Linux Isaac Sim](https://downloads.isaacsim.nvidia.com/isaac-sim-standalone-6.0.0-linux-x86_64.zip)
설치 이후 터미널에서
```
# 폴더 만들기
mkdir -p ~/isaacsim
# 다운로드 폴더 가서
cd ~/Downloads
#isaac sim zip 파일을 isaacsim폴더에 압축해제
unzip "isaac-sim-standalone-6.0.0-linux-x86_64.zip" -d ~/isaacsim
#isaac sim 폴더로 이동
cd ~/isaacsim
#post install 실행
./post_install.sh
#isaac sim 실행
./isaac-sim.sh
```

설치 이후 호환성 테스트
```
./isaac-sim.compatibility_check.sh
```

![[Pasted image 20260611163244.png]]


Isaac sim 실행 화면
![[Pasted image 20260611163403.png]]

바닥생성하기 
상단의 Create -> Physics -> Ground Plane
![[Pasted image 20260611163652.png]]

박스 생성하기

Create -> Mesh -> Cube
![[Pasted image 20260611163820.png]]

포커싱 이동 하는 법
포커스 잡고 싶은 물체 누른 후 F 클릭

![[Peek 2026-06-11 16-45.gif]]




----
## 우분투 Isaac sim 원격으로 확인하기
다른 공유기에서 원격으로 확인하기 위해서 일단 isaac sim streaming을 사용할 거임
이거를 하기 위해 glxinfo가 필요 이거 설치하기 위해서 

```
sudo apt update
sudo apt install mesa-utils
glxinfo -B
```


vulkan 확인
```
sudo apt install vulkan-tools  
vulkaninfo | less
```