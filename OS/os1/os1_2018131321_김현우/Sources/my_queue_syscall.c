#include<linux/syscalls.h>
#include<linux/kernel.h>
#include<linux/linkage.h>

#define MAXSIZE 500

int queue[MAXSIZE];
int front = 0;        // queue에 있는 element중 처음을 가리키는 index
int rear = 0;         // queue에 있는 element중 마지막을 가리키는 index
int i, j, res = 0;


SYSCALL_DEFINE1(oslab_enqueue, int, a ){
	
	if (rear > MAXSIZE - 1) { // if queue is full 
		printk(KERN_INFO "[Error] - QUEUE IS FULL------------------\n");
		return -2;
	}
	
	for ( i = front; i<rear ;i++) {      // a가 queue에 있는 element중 a와 겹치는 것이 있는지 확인
		if (queue[i] == a)
		{	
			printk(KERN_INFO "[Error] - Already existing value \n");
			return a;
		}
	}
	
	queue[rear] = a ;       // queue에 a 삽입
	
	printk(KERN_INFO "[System call] oslab_enqueue(); ------\n");
	printk("Queue Front--------------------\n");
	for (i = front; i <= rear ; i ++)     // queue에 있는 element들 출력
		printk("%d\n", queue[i]); 
	printk("Queue Rear--------------------\n");
	
	rear = rear + 1;      //  rear를 다음 element 삽입 할 index로 옮김

	return a;
}

SYSCALL_DEFINE0(oslab_dequeue){
	
	if (rear == front) { // if queue is empty
		printk(KERN_INFO "[Error] - EMPTY QUEUE------------------\n");
		return -2;
	}
	res = queue[front]; // queue에 처음 들어온 값을 변수 res에 할당
	front = front + 1;  // queue에 들어온 다음 값의 index로 front 이동
	
	printk(KERN_INFO "[System call] oslab_dequeue(); ------\n");
	printk("Queue Front--------------------\n");
	
	for (j = front; j < rear ; j ++)       // queue에 있는 element들 출력
		printk("%d\n", queue[j]);
	
	printk("Queue Rear--------------------\n");

	return res;
}

