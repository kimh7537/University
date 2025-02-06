#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/wait.h>
#include<time.h>
#include<sched.h>
#include<stdint.h>
#include<string.h>
#include<sys/syscall.h>

#define ROW (100)
#define COL ROW

struct sched_attr {
   uint32_t size;  
   uint32_t sched_policy;    
   uint64_t sched_flags;      
   int32_t  sched_nice;       
   uint32_t sched_priority;
   uint64_t sched_runtime;
   uint64_t sched_deadline;
   uint64_t sched_period;
};

static int sched_setattr(pid_t pid, const struct sched_attr *attr, unsigned int flags)
{
    return syscall(SYS_sched_setattr, pid, attr, flags);
}

int calc(int cpu, int time, unsigned long tv_nsec){

	int matrixA[ROW][COL];
	int matrixB[ROW][COL];
	int matrixC[ROW][COL];
	int i, j, k;
	
	int cpuid;
	int count = 0;

	cpuid = cpu;

	struct timespec begin, end;
	long long temp;
	long long time_nano;
	long long time_milli, time_second;

	const long long NANOS = 1000000000LL;

	unsigned long tv_millis;
	tv_millis = tv_nsec / 1000000; //time quantum

	while(1) {
		clock_gettime(CLOCK_MONOTONIC, &begin);
		for(i = 0 ; i < ROW ; i++) {
			for(j = 0 ; j < COL ; j++) {
				for(k = 0 ; k < COL ; k++){
					matrixC[i][j] += matrixA[i][k] * matrixB[k][j];
				} 
			}		
		}
		count++;

		clock_gettime(CLOCK_MONOTONIC, &end);

		time_nano = NANOS*(end.tv_sec - begin.tv_sec) + (end.tv_nsec - begin.tv_nsec);
		temp += time_nano;

		time_milli = temp/1000000;
		time_second = temp/1000000000;
		
		if(time_milli % tv_millis==0) {  //time quantum간격마다 프로세스 진행 상황 모니터링링
			printf("PROCESS #%02d count = %02d %lu\n", cpuid, count, tv_millis);
		}

		if(time_second >= time) {
			printf("DONE!! PROCESS #%02d : %06d %lld\n", cpuid, count, time_milli);
			break;
		}
		
	}

	return 0;
}

int main(int argc, char **argv){
	

	struct sched_attr attr;

	memset(&attr, 0, sizeof(attr));
    	attr.sched_priority = 10;
    	attr.sched_policy = SCHED_RR; //Round Robin 스케줄링

	int forknum = atoi(argv[1]); //fork할 process 갯수(ex. 2개)
	int time = atoi(argv[2]);    //프로그램 실행 시간(초 단위, ex. 30초)

	pid_t pid[forknum];
	int i;
	
	struct timespec ts;
	int interval;

	for(i=0 ; i<forknum ; i++){
		pid[i] = fork();  //부모 프로세스-> 자식PID return, 자식 프로세스-> return 0
		int calc_result = 0;
		int setattr_result = 0;
		if(pid[i] == 0){ //부모, 자식 프로세스 모두 조건문 실행, 자식만 true로 진입가능
			printf("Creating Process: #%d\n", i);
			setattr_result = sched_setattr(getpid(), &attr, 0);
			// 현재 프로세스(getpid())에 Round Robin 스케줄링 속성(&attr) 설정
			// 0은 flags로, 특별한 옵션 없음을 의미
			
			interval = sched_rr_get_interval(0, &ts); 
			//time quantum가져오기
			//(0:현재 프로세스, &ts: time quantum값을 저장할 timespec구조체 포인터)
			//반환값은 실제 ts.tv_nsec에 저장된 나노초 단위의 time quantum
			
			calc_result = calc(i, time, ts.tv_nsec); //(i:프로세스 번호, time: 실행시간, ts.tv_nsec: time quantum)

			exit(0);		
		}
	}
	
	int status;
	while(wait(&status) != -1); // 모든 자식 프로세스가 종료될 때까지 부모 프로세스가 대기
	//자식 프로세스가 종료되면 status가 -1이됨
	
	return 0;
}
