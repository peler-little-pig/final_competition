//
//  ASR.ino
//  智能用纸管理系统
//
//  Created by peler on 2022/8、16.
//  Copyright © 2022 peler. All rights reserved.
//

#include "ASR.h"  //语音识别
#include <LiquidCrystal.h>  //LCD显示

//#define DEBUG   //DEBUG模式

//初始化硬件对象
LiquidCrystal lcd(7, 8, 9, 10, 11, 2);

bool isAnswer = 0;
int item = 4;
int score = 0;

int num = 0;

int index = 0;
int list[50];

void setup() {
  /*
   * 以下为语音识别初始化代码，语音识别模块官方提供
   */
  unsigned char cleck = 0xff;
  unsigned char asr_version = 0;
  Wire.begin();
  Wire.setClock(100000);
  Serial.begin(115200);  // 串口波特率设置


  WireReadData(FIRMWARE_VERSION, &asr_version, 1);
  Serial.print("asr_version is ");
  Serial.println(asr_version);
#if 1
  I2CWrite(ASR_CLEAR_ADDR, 0x40); // 清除掉电保存区,录入前需要清除掉电保存区
  BusyWait();
  Serial.println("clear flash is ok");
  I2CWrite(ASR_MODE_ADDR, 1); // 设置检测模式
  BusyWait();
  Serial.println("mode set is ok");
  AsrAddWords(0, "kai shi");
  BusyWait();
  AsrAddWords(1, "hong deng");
  BusyWait();
  AsrAddWords(2, "lv deng");
  BusyWait();
  AsrAddWords(3, "lan deng");
  BusyWait();

  AsrAddWords(4, "qie fan");
  BusyWait();
  AsrAddWords(5, "shui gao");
  BusyWait();
  AsrAddWords(6, "xia xian");
  BusyWait();
  AsrAddWords(7, "xie za ye");
  BusyWait();
  while (cleck != 8)
  {
    WireReadData(ASR_NUM_CLECK, &cleck, 1);
    Serial.println(cleck);
    delay(100);
  }
  Serial.println("cleck is ok");
#endif

  I2CWrite(ASR_REC_GAIN, 0x40); //识别的灵敏度
  I2CWrite(ASR_VOICE_FLAG, 1); //识别结果提示音开关设置
  I2CWrite(ASR_BUZZER, 1); //开启蜂鸣器
  RGB_Set(255, 255, 255); //设置模块的RGB灯为白色
  delay(500);
  I2CWrite(ASR_BUZZER, 0); //关闭蜂鸣器
  RGB_Set(0, 0, 0); //关闭RGB灯

  //初始化硬件组件
  lcd.begin(16, 2);
}

void loop() {
  unsigned char result;
  WireReadData(ASR_RESULT, &result, 1); //读取识别序号值，并赋值给result，默认是0xff
  delay(100);
//  Serial.println(result);
  
  if (result==0) {
//    Serial.println("bbbbbbbbbbbbbbbbb");
    isAnswer = 1;
    item++;
  }
  if (isAnswer == 1)
  {
    num++;
//    Serial.println(num);
    lcd.setCursor(10,1);
    lcd.print(50-num);
    if (num==50) {
      isAnswer=0;
      num = 0;
    }

    if (result==item-1) {
      score++;
      isAnswer=0;
      num = 0;
    }
  }
  if (item == 9) {
    list[index] = score;
    index++;
    
    isAnswer = 0;
    item = 4;
    score = 0;
    num = 0;
  }

  lcd.setCursor(0,0);
  lcd.print("score:");
  lcd.print(score);

  lcd.setCursor(0,1);
  lcd.print("item:");
  lcd.print(item-4);

  if (Serial.available()) {
    if (Serial.read() == 'd') {
      for (int i=0;i<index;i++) {
        Serial.print(list[i]);
        Serial.print(',');
      }
      Serial.println();
    }
  }
}
