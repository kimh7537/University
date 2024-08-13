#include<unistd.h>
#include<stdio.h>

#define my_queue_enqueue 335
#define my_queue_dequeue 336

int main(){
	int a = 0;
	
	a = syscall(my_queue_enqueue, 1);     // enqueue함수를 시스템콜 호출, queue에 숫자 1 넣음
	printf("Enqueue : ");			
	printf("%d\n", a);
	
	a = syscall(my_queue_enqueue, 2);     // enqueue함수를 시스템콜 호출, queue에 숫자 2 넣음
	printf("Enqueue : ");			
	printf("%d\n", a);
	
	a = syscall(my_queue_enqueue, 3);     // enqueue함수를 시스템콜 호출, queue에 숫자 3 넣음
	printf("Enqueue : ");			
	printf("%d\n", a);
	
	a = syscall(my_queue_enqueue, 3);     //  enqueue함수를 시스템콜 호출, 기존 queue에 있던 3과 새로 넣으려고 하는 element가 겹침
	printf("Enqueue : ");		
	printf("%d\n", a);
	
	a = syscall(my_queue_dequeue);        // dequeue함수를 시스템콜 호출, queue에서 가장 앞에 있는 element dequeue
	printf("Dequeue : ");		
	printf("%d\n", a);
	
	a = syscall(my_queue_dequeue);        // dequeue함수를 시스템콜 호출, queue에서 가장 앞에 있는 element dequeu
	printf("Dequeue : ");		
	printf("%d\n", a);
	
	a = syscall(my_queue_dequeue);        // dequeue함수를 시스템콜 호출, queue에서 가장 앞에 있는 element dequeu
	printf("Dequeue : ");		
	printf("%d\n", a);
	
	return 0;
}
