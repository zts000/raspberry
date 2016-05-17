/********************************************************************
开发环境：Keil
单片机：AT89S52-24PU  晶振：12 MZ 
程序描述： K型热电偶+MAX6675，LCD1602 显示  
designed by YING 
2012-08-29 21:16   完成
注：1：本程序没有作断偶检测，请根据实际情况参考DATASHEET 编写
    2：本程序只供学习参考之用，请勿用于其它用途！！参考请自行验证程序正确性及可靠性！！！
**************************定义头文件*****************************************/
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
sbit LCD1602_RS=P2^0;   //设置RS 
sbit LCD1602_RW=P2^1;   //设置RW
sbit LCD1602_EN=P2^2;   //设置E
sbit MAX6675_SO=P2^4;    
sbit MAX6675_SCK=P2^5;    
sbit MAX6675_CS=P2^6; 
unsigned char data disdata[5];
unsigned int Value;
/********************************************************************/
void LCD_delay(void);//LCD延时函数
void LCD_en_command(unsigned char command);//LCD写指令
void LCD_en_dat(unsigned char temp);//LCD写数据
void LCD_set_xy( unsigned char x, unsigned char y );//设置LCD显示位置
void LCD_write_char( unsigned x,unsigned char y,unsigned char dat);//向LCD写入一个字符
void LCD_write_string(unsigned char X,unsigned char Y,unsigned char *s);//向LCD写入一串字符
void LCD_init(void);//LCD初始化函数
/********************************************************************/
void delay_nms(unsigned int n);//延时函数

/********************************************************************/
/***********************从MAX6675读取温度*********************************************/
unsigned int ReadMAX6675()   
{
 unsigned char count;
 MAX6675_CS=1; //关闭MAX6675
  //_nop_();
 //  _nop_();
 MAX6675_CS=0;//置低，使能MAX6675
 //_nop_();

 MAX6675_SCK=1;
 Value=0;
 //_nop_();
 //_nop_();
 for(count=16;count>0;count--) //获取16位MSB
 {
  MAX6675_SCK=0;  //sck置低
  Value=Value<<1;     //左移
    if(MAX6675_SO==1) //取当前值
   Value|=0x0001;
  else
   Value&=0xffff;
  MAX6675_SCK=1;
 //_nop_();
  //_nop_();
  //_nop_();
 //_nop_();
 }
 MAX6675_CS=1;  //关闭MAX6675
 return Value;
}
/***************************************************************************************/
/**************************温度值显示 **************************************************/
void tempdisp()  
{ 
  unsigned int temp;
  unsigned int TempValue;
 // unsigned int testD2;
  unsigned int xiaoshu;
  
   TempValue=ReadMAX6675();//读取MAX6675 转换后的温度数值；   
   TempValue=TempValue<<1;         //去掉第15位
   TempValue=TempValue>>4;//去掉第0~2位
   xiaoshu=TempValue*10;
   TempValue=TempValue/4;	     //MAX6675最大数值为1023。75，而AD精度为12位，即2的12次方为4096，转换对应数，故要除4；
   xiaoshu=xiaoshu/4;			//与上述同理
	if(TempValue>=1024)
	{TempValue=1024;}
	disdata[0]=(TempValue/1000)%10+0x30;//千位 +0x30是对应LCD里的ROM字符位置编码
    disdata[1]=(TempValue/100)%10+0x30;//百位  +0x30是对应LCD里的ROM字符位置编码
    disdata[2]=(TempValue/10)%10+0x30;//十位 +0x30是对应LCD里的ROM字符位置编码
    disdata[3]=(TempValue)%10+0x30;//个位  +0x30是对应LCD里的ROM字符位置编码
    disdata[4]=xiaoshu%10+0x30;//分位	 +0x30是对应LCD里的ROM字符位置编码  

	if(disdata[0]==0x30)
	{
	  LCD_write_char(4,LINE2,0x20);	//显示千位	
	  if(disdata[1]==0x30)
	    { LCD_write_char(5,LINE2,0x20);  
		  if(disdata[2]==0x30)
	       LCD_write_char(6,LINE2,0x20); 
		   else  LCD_write_char(6,LINE2,disdata[2]);	 //显示十位
	    }
	   else  
	  {    LCD_write_char(5,LINE2,disdata[1]); //显示百位
	       LCD_write_char(6,LINE2,disdata[2]);	 //显示十位
	  }
	 }	   
	 else  
	 {
	 LCD_write_char(4,LINE2,disdata[0]);	//显示千位
	 LCD_write_char(5,LINE2,disdata[1]);   //显示百位
	 LCD_write_char(6,LINE2,disdata[2]);	//显示十位
	 }
	 // LCD_write_char(6,LINE2,disdata[2]);	 //显示十位
	 LCD_write_char(7,LINE2,disdata[3]);	//显示个位
	 LCD_write_char( 8,LINE2,0X2e);//显示"点"
 	 LCD_write_char(9,LINE2,disdata[4]);	//显示分位
	  LCD_write_char( 10,LINE2,0XDF);//显示"度"		 
     LCD_write_char( 11,LINE2,0X43);//显示"C"

 
}  
/****************************主 程 序********************************************************/
void main(void)
{
 delay_nms(10);
 LCD_init();   //LCD初始化
 delay_nms(50);
 CLEARSCREEN;	//清屏
 delay_nms(10);
 LCD_write_string(0,LINE1,"temperature TEST");

 while(TRUE )    
 {
     
	tempdisp();  
	delay_nms(220);              
 }
}
/********************************************************************/
/******************** LCD 函数部份 ***********************************/
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
    LCD_set_xy( X, Y );//设置显示XY地址 
    while (*s)  // 写字符
    {
     LCDIO=*s;
        LCD_en_dat(*s);   
 s ++;
    }
}
/********************************************************************/
void LCD_init(void)
{  CLEARSCREEN;//clear screen 
 LCD_en_command(DATA_MODE);//8位模式
  LCD_en_command(DATA_MODE);
  LCD_en_command(DATA_MODE);
  LCD_en_command(DATA_MODE);
 LCD_en_command(OPEN_SCREEN);//开显示
 LCD_en_command(DISPLAY_ADDRESS);//设定显示起始位 
 CLEARSCREEN;//清屏
}
/********************************************************************/
/***********************  延时 *********************************/
void delay_nms(unsigned int n)      
{
    unsigned int i=0,j=0;
    for (i=n;i>0;i--)
     for (j=0;j<1140;j++);  
}
/********************************************************************/