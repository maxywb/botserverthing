#ifndef _BOTSERVERTHING_SERIALCOM_HPP_
#define _BOTSERVERTHING_SERIALCOM_HPP_

#ifndef BST_NOT_AVR
#define uint8_T unsigned char
#define uint32_T unsigned long
#else
#include <cstdlib>
#define uint8_T uint8_t
#define uint32_T uint32_t
#endif

typedef union{
  uint8_T raw[4];
  float   as_float;
  uint32_T as_int;
} cmd_contents;
struct packet{
  uint8_T      cmd;
  cmd_contents data;
} __attribute__((packed));


#endif
