/*********************************************************************
 * @file          util.c
 * @version
 * @brief

 * @date          Wed Nov 20 22:24:14 2013
 * Modified at:   Tue Jan 14 14:30:23 2020
 * Modified by:   badnack <n.redini@gmail.com>
 ********************************************************************/
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include "util.h"

extern Message send_login(int);
extern Message send_registration(int);
extern Message send_pag_help(int);
extern Message send_exit(int);
extern Message show_my_diamonds(int);
extern Message add_diamond(int);

/** tremendous hack */
Message
dummy_foo()
{
  /* We're
     happy */
  return OK;
}

void
init_system()
{
  f_array[0] = dummy_foo;
  f_array[1] = send_login;
  f_array[2] = send_registration;
  f_array[3] = send_pag_help;
  f_array[4] = send_exit;
  f_array[5] = show_my_diamonds;
  f_array[6] = add_diamond;
}

int
get_code_opt(char c)
{
  switch(c) {
  case 'l':
  case 'L':
    return 1;
  case 'r':
  case 'R':
    return 2;
  case 'h':
  case 'H':
    return 3;
  case 'e':
  case 'E':
    return 4;
  case 'g':
  case 'G':
    return 5;
  case 'a':
  case 'A':
    return 6;
  case 'y':
  case 'Y':
    return 7;
  case 'n':
  case 'N':
    return 8;
  case 't':
  case 'T':
    return 9;
  default:
    return UNKNOWN;
  }
}

Message
send_msg(const char* msg)
{
  unsigned int len, count;
  int ret;

  len = strlen(msg);
  if (send(clientsd, &len, sizeof(unsigned int), MSG_NOSIGNAL) <= 0) {
    return FATAL_ERROR;
  }
  count = 0;
  while (count < len) {
    if((ret = send(clientsd, &msg[count], len - count, MSG_NOSIGNAL)) < 0) {
      return FATAL_ERROR;
    }
    count += ret;
  }
  return OK;
}

int
recv_cmd()
{
  unsigned int size;
  char cmd;

  if (recv(clientsd, &size, sizeof(unsigned int), 0) <= 0) {
    return FATAL_ERROR;
  }
  if (size != 1) {
    return TOO_LONG;
  }
  if (recv(clientsd, &cmd, size, 0) <= 0) {
    return FATAL_ERROR;
  }
  return get_code_opt(cmd);
}

Message
recv_msg(char *msg, int msg_size)
{
  unsigned int len, count;
  int ret;

  if (recv(clientsd, &len, sizeof(unsigned int), 0) <= 0) {
    return FATAL_ERROR;
  }
  if (len > (msg_size - 1)) {
    return TOO_LONG;
  }

  count = 0;
  while (count < len) {
    if ((ret = recv(clientsd, &msg[count], len - count, 0)) < 0) {
      return FATAL_ERROR;
    }
    count += ret;
  }
  msg[len] = 0;
  return OK;
}
