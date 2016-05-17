/************************************************************/
/*********          PCCOM.H C51 driver            *************/
/**********  Written by WangBiao---20060311  ****************/
/************************************************************/
//#include <stdio.h>
//-----------------------------------------------------------
//P3_0->RXD  ;;  P3_1->TXD
//-----------------------------------------------------------------------
//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
//-----------------------------------------------------------------------
//-----------------------Íâ²¿º¯Êý----------------------------------------
void Init_Pccom(void);
	//---------------------------------------------------
extern char _getkey (void);
extern char getchar (void);
extern char ungetchar (char);
extern char putchar (char);
extern int printf   (const char *, ...);
	//---------------------------------------------------
extern int sprintf  (char *, const char *, ...);
extern int vprintf  (const char *, char *);
extern int vsprintf (char *, const char *, char *);
extern char *gets (char *, int n);
extern int scanf (const char *, ...);
extern int sscanf (char *, const char *, ...);
extern int puts (const char *);
//-----------------------------------------------------------------------
//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
//-----------------------------------------------------------------------
//------------------------------------------------------------
void Init_Pccom(void) 
{	SCON  = 0x50;		    /* SCON: mode 1, 8-bit UART, enable rcvr            */
	TMOD |= 0x20;           /* TMOD: timer 1, mode 2, 8-bit reload              */
	TH1   = 0xfd; 		    /* TH1221:  reload value for 9600 baud @ 11.0592MHz */
	TL1   = 0xfd;           /* TH1221:  reload value for 1200 baud @ 16MHz      */
	TR1   = 1;              /* TR1:  timer 1 run                                */
	TI    = 1;              /* TI:   set TI to send first char of UART          */
}
//----------pccom end-----------------------------------------
