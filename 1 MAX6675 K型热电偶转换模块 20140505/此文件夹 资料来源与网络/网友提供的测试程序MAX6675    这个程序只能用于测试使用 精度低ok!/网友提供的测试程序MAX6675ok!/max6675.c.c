#include <reg52.h>
#include "max6675.h"
#include "pccom.h"
#include "delay.h"
//-----------------------------------------------------------------------------------------
//--------------max6675 test---------------------------
void main(void)
{	unsigned int t;

	Init_Pccom();
	printf("hello,this is max6675 test!\n");
	for(;;)
	{	t=read_6675();
		printf("%d\n",t);
		blink(3,1);
		delay50ms(1);
	}
}
//--------------END-------------------------------------
