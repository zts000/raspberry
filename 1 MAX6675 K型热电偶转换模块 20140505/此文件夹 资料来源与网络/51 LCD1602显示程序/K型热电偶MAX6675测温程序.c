/********************************************************************
����������Keil
��Ƭ����AT89S52-24PU  ����12 MZ 
���������� K���ȵ�ż+MAX6675��LCD1602 ��ʾ  
designed by YING 
2012-08-29 21:16   ���
ע��1��������û������ż��⣬�����ʵ������ο�DATASHEET ��д
    2��������ֻ��ѧϰ�ο�֮�ã���������������;�����ο���������֤������ȷ�Լ��ɿ��ԣ�����
**************************����ͷ�ļ�*****************************************/
#include <reg51.h>
#include<intrins.h>
/*******************************************************************/
//lcd part
#define  LINE1     0
#define  LINE2     1
#define  LINE1_HEAD    0x80
#define  LINE2_HEAD    0xC0
#define  LCD_DELAY_TIME   40
#define  DATA_MODE    0x38
#define  OPEN_SCREEN    0x0C
#define  DISPLAY_ADDRESS   0x80
#define  CLEARSCREEN    LCD_en_command(0x01)
#define  HIGH   1
#define  LOW    0
#define  TRUE    1
#define  FALSE    0
#define  ZERO    0 
#define  MSB    0x80
#define  LSB    0x01
/*******************************************************************/
#define  LCDIO     P1
sbit LCD1602_RS=P2^0;   //����RS 
sbit LCD1602_RW=P2^1;   //����RW
sbit LCD1602_EN=P2^2;   //����E
sbit MAX6675_SO=P2^4;    
sbit MAX6675_SCK=P2^5;    
sbit MAX6675_CS=P2^6; 
unsigned char data disdata[5];
unsigned int Value;
/********************************************************************/
void LCD_delay(void);//LCD��ʱ����
void LCD_en_command(unsigned char command);//LCDдָ��
void LCD_en_dat(unsigned char temp);//LCDд����
void LCD_set_xy( unsigned char x, unsigned char y );//����LCD��ʾλ��
void LCD_write_char( unsigned x,unsigned char y,unsigned char dat);//��LCDд��һ���ַ�
void LCD_write_string(unsigned char X,unsigned char Y,unsigned char *s);//��LCDд��һ���ַ�
void LCD_init(void);//LCD��ʼ������
/********************************************************************/
void delay_nms(unsigned int n);//��ʱ����

/********************************************************************/
/***********************��MAX6675��ȡ�¶�*********************************************/
unsigned int ReadMAX6675()   
{
 unsigned char count;
 MAX6675_CS=1; //�ر�MAX6675
  //_nop_();
 //  _nop_();
 MAX6675_CS=0;//�õͣ�ʹ��MAX6675
 //_nop_();

 MAX6675_SCK=1;
 Value=0;
 //_nop_();
 //_nop_();
 for(count=16;count>0;count--) //��ȡ16λMSB
 {
  MAX6675_SCK=0;  //sck�õ�
  Value=Value<<1;     //����
    if(MAX6675_SO==1) //ȡ��ǰֵ
   Value|=0x0001;
  else
   Value&=0xffff;
  MAX6675_SCK=1;
 //_nop_();
  //_nop_();
  //_nop_();
 //_nop_();
 }
 MAX6675_CS=1;  //�ر�MAX6675
 return Value;
}
/***************************************************************************************/
/**************************�¶�ֵ��ʾ **************************************************/
void tempdisp()  
{ 
  unsigned int temp;
  unsigned int TempValue;
 // unsigned int testD2;
  unsigned int xiaoshu;
  
   TempValue=ReadMAX6675();//��ȡMAX6675 ת������¶���ֵ��   
   TempValue=TempValue<<1;         //ȥ����15λ
   TempValue=TempValue>>4;//ȥ����0~2λ
   xiaoshu=TempValue*10;
   TempValue=TempValue/4;	     //MAX6675�����ֵΪ1023��75����AD����Ϊ12λ����2��12�η�Ϊ4096��ת����Ӧ������Ҫ��4��
   xiaoshu=xiaoshu/4;			//������ͬ��
	if(TempValue>=1024)
	{TempValue=1024;}
	disdata[0]=(TempValue/1000)%10+0x30;//ǧλ +0x30�Ƕ�ӦLCD���ROM�ַ�λ�ñ���
    disdata[1]=(TempValue/100)%10+0x30;//��λ  +0x30�Ƕ�ӦLCD���ROM�ַ�λ�ñ���
    disdata[2]=(TempValue/10)%10+0x30;//ʮλ +0x30�Ƕ�ӦLCD���ROM�ַ�λ�ñ���
    disdata[3]=(TempValue)%10+0x30;//��λ  +0x30�Ƕ�ӦLCD���ROM�ַ�λ�ñ���
    disdata[4]=xiaoshu%10+0x30;//��λ	 +0x30�Ƕ�ӦLCD���ROM�ַ�λ�ñ���  

	if(disdata[0]==0x30)
	{
	  LCD_write_char(4,LINE2,0x20);	//��ʾǧλ	
	  if(disdata[1]==0x30)
	    { LCD_write_char(5,LINE2,0x20);  
		  if(disdata[2]==0x30)
	       LCD_write_char(6,LINE2,0x20); 
		   else  LCD_write_char(6,LINE2,disdata[2]);	 //��ʾʮλ
	    }
	   else  
	  {    LCD_write_char(5,LINE2,disdata[1]); //��ʾ��λ
	       LCD_write_char(6,LINE2,disdata[2]);	 //��ʾʮλ
	  }
	 }	   
	 else  
	 {
	 LCD_write_char(4,LINE2,disdata[0]);	//��ʾǧλ
	 LCD_write_char(5,LINE2,disdata[1]);   //��ʾ��λ
	 LCD_write_char(6,LINE2,disdata[2]);	//��ʾʮλ
	 }
	 // LCD_write_char(6,LINE2,disdata[2]);	 //��ʾʮλ
	 LCD_write_char(7,LINE2,disdata[3]);	//��ʾ��λ
	 LCD_write_char( 8,LINE2,0X2e);//��ʾ"��"
 	 LCD_write_char(9,LINE2,disdata[4]);	//��ʾ��λ
	  LCD_write_char( 10,LINE2,0XDF);//��ʾ"��"		 
     LCD_write_char( 11,LINE2,0X43);//��ʾ"C"

 
}  
/****************************�� �� ��********************************************************/
void main(void)
{
 delay_nms(10);
 LCD_init();   //LCD��ʼ��
 delay_nms(50);
 CLEARSCREEN;	//����
 delay_nms(10);
 LCD_write_string(0,LINE1,"temperature TEST");

 while(TRUE )    
 {
     
	tempdisp();  
	delay_nms(220);              
 }
}
/********************************************************************/
/******************** LCD �������� ***********************************/
void LCD_delay(void)   
{
 unsigned char i;
 for(i=LCD_DELAY_TIME;i>ZERO;i--)
   ;
}
/********************************************************************/  
void LCD_en_command(unsigned char command)
{
 LCD_delay();
 LCD1602_RS=LOW;   
 LCD1602_RW=LOW;
 LCD1602_EN=HIGH;
 LCDIO=command;
 LCD1602_EN=LOW;
}
/********************************************************************/
void LCD_en_dat(unsigned char dat)
{
 LCD_delay();
 LCD1602_RS=HIGH;
 LCD1602_RW=LOW;
 LCD1602_EN=HIGH;
 LCDIO=dat;
 LCD1602_EN=LOW;
}
/********************************************************************/
void LCD_set_xy( unsigned char x, unsigned char y )
{
 unsigned char address;
 if (y == LINE1) 
  address = LINE1_HEAD + x;
 else 
     address = LINE2_HEAD + x;
 LCD_en_command(address); 
}
/********************************************************************/
void LCD_write_char( unsigned x,unsigned char y,unsigned char dat)
{
 LCD_set_xy( x, y ); 
 LCD_en_dat(dat);
}
/********************************************************************/
void LCD_write_string(unsigned char X,unsigned char Y,unsigned char *s)
{
    LCD_set_xy( X, Y );//������ʾXY��ַ 
    while (*s)  // д�ַ�
    {
     LCDIO=*s;
        LCD_en_dat(*s);   
 s ++;
    }
}
/********************************************************************/
void LCD_init(void)
{  CLEARSCREEN;//clear screen 
 LCD_en_command(DATA_MODE);//8λģʽ
  LCD_en_command(DATA_MODE);
  LCD_en_command(DATA_MODE);
  LCD_en_command(DATA_MODE);
 LCD_en_command(OPEN_SCREEN);//����ʾ
 LCD_en_command(DISPLAY_ADDRESS);//�趨��ʾ��ʼλ 
 CLEARSCREEN;//����
}
/********************************************************************/
/***********************  ��ʱ *********************************/
void delay_nms(unsigned int n)      
{
    unsigned int i=0,j=0;
    for (i=n;i>0;i--)
     for (j=0;j<1140;j++);  
}
/********************************************************************/