#include "allhead.h"

int main()
{
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	delay_init();
	LED_Init();
	RX_Init();
	TIM1_Init(2000-1,720-1);
	TIM3_Init(2000-1,720-1);
	GPIO_ResetBits(GPIOB,GPIO_Pin_3);
	GPIO_ResetBits(GPIOB,GPIO_Pin_5);
	GPIO_ResetBits(GPIOB,GPIO_Pin_11);
	GPIO_ResetBits(GPIOB,GPIO_Pin_10);
	GPIO_ResetBits(GPIOB,GPIO_Pin_12);
	GPIO_ResetBits(GPIOB,GPIO_Pin_13);
	while(1)
	{
		long long int n=0;
		if(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_11))
		{
			delay_ms(100);
			if(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_11))
			{
				TIM3->CCR1=2000;
				TIM3->CCR2=0;  //down
				while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_4))
				{
					delay_ms(100);
					while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_4))
					{
						n++;
						if(n>3000000)
							break;
					}
					if(n>3000000)
					{
						break;
					}
				}
				if(n>3000000)
				{
					TIM3->CCR1=0;
					TIM3->CCR2=2000; //up
					while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_6))
					{
						delay_ms(100);
						while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_6));
					}
					GPIO_SetBits(GPIOB,GPIO_Pin_13);
					GPIO_SetBits(GPIOB,GPIO_Pin_12);
					delay_ms(300);
					GPIO_ResetBits(GPIOB,GPIO_Pin_13);
					GPIO_ResetBits(GPIOB,GPIO_Pin_12);
					continue;
				}
				TIM3->CCR1=0;
				TIM3->CCR2=00;
	//---------------------------------
				TIM1->CCR1=110;  //clamp ball
				delay_ms(300);
	//---------------------------------
				TIM3->CCR1=0;
				TIM3->CCR2=2000; //up
				while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_6))
				{
					delay_ms(100);
					while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_6));
				}	
				TIM3->CCR1=0;
				TIM3->CCR2=00;
				delay_ms(1000);

	//---------------------------------
	//		put first pin high
				GPIO_SetBits(GPIOB,GPIO_Pin_12);
				delay_ms(1000);
				GPIO_ResetBits(GPIOB,GPIO_Pin_12);
	//---------------------------------
			}
		}
		else if(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_10))
		{
			delay_ms(100);
			if(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_10))
			{
				TIM1->CCR1=70; //loosen
				delay_ms(500);
	//---------------------------------
	//			put second pin high 
				GPIO_SetBits(GPIOB,GPIO_Pin_13);
				delay_ms(1000);
				GPIO_ResetBits(GPIOB,GPIO_Pin_13);
	//---------------------------------
	    } 

		}
	}
		
}	
