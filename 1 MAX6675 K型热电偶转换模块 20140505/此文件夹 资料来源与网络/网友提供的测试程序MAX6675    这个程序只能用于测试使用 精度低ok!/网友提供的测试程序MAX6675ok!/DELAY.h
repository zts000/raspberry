/************************************************************/
/*********         DELAY.H C51 driver           *************/
/**********  Written by WangBiao---20060308  ****************/
/************************************************************/
//-----------------------------------------------------------------------
//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
//-----------------------------------------------------------------------
sbit    LED =P3^4;
//-----------------------�ⲿ����----------------------------------------
void delay(unsigned int n);
void delay50ms(unsigned int n);
//-----------------------------------------------------------------------
//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
//-----------------------------------------------------------------------
//*********************************************//
//       delay nearly n*0.05s ;;n=20->1s      //
//********************************************//
void delay(unsigned int n)
{	unsigned int i;
	for(;n>0;n--)
	{	for(i=0;i<10000;) i++;  }
}
//********************************************//
//       delay50ms n*0.05s    ;;n=20->1s      //
//********************************************//
void delay50ms(unsigned int n) 
{	unsigned int i;
	for(i=0;i<n;i++)
 	{	TMOD=0x01;
		TH0=0x3c;TL0=0xaf;
		TR0=1;
		for(TF0=0;TF0==0;);//eaqual wait
	}
}
//-----------test LED-----------------------
void blink(unsigned char t,unsigned char n)
{	unsigned char i;
	for(i=0;i<n;i++)
	{	LED=0;delay(t);LED=1;delay(t);	}
}
//-------------------end DELAY.H-----------------------------------------
