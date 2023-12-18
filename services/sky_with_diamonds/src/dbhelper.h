/*
 * TreasureCaveDb.h
 *
 *  Created on: Nov 24, 2013
 *      Author: webking
 */

#include "util.h"

#ifndef TREASURECAVEDB_H_
#define TREASURECAVEDB_H_
#define MAX_DIAMONDS_PER_USER 20

typedef enum {
  RESULT_OK=0,
  STRING_WRONG_FORMAT=-1,
  DB_ERROR=-2,
  DB_ERROR_USER_EXISTS=-3,
  DB_OPEN_ERROR=-4,
  DB_NO_RESULT=-5,
  DB_ERROR_DIAMOND_EXISTS=-6,
  DB_ERROR_TOO_MANY_DIAMONDS=-7,
  DB_ERROR_TOO_MANY_USERS=-8 // #n#
} DB_RES;

typedef struct DIAMOND_STRUCT{
  int (*insert)(int, double, double, char*);
  int timestamp; // #n#
  int id;
  int descriptionLen;
  int userId;
  double price;
  double size;
  char descr[MAX_USER_LEN];
}diamond;

typedef struct USER_STRUCT {
    unsigned int ts;
    int user_id;
    int uname_len;
    int pass_len;
    char username[MAX_USER_LEN];
    char pass[MAX_USER_LEN];
}USER;

static const char USER_DB_PATH [] = "user.dat";
static const char USER_DB_PATH_BAK [] = "user.dat.bak";
static const char DIAMONDS_DB_PATH [] ="diamonds.dat";
static const char DIAMONDS_DB_PATH_BAK [] ="diamonds.dat.bak";

int list_diamonds(int, diamond**);
int insert_diamond(int, double, double, char*);
int check_cred(int, char*, char**);
int add_user(char*, char*);
int db_clean();
int get_diamonds(diamond**, int*);

/**
 * The user.dat contains as many record-entries as the number of users.
 * Each record is composed as following:
 * Timestamp (4 bytes unsigned int) - UserId (4 bytes, integer) - UsernameLength (4 bytes, integer) - PasswordLength (4 bytes, integer) - UserName (MAX_USER_LEN bytes, string) - Password (MAX_USER_LEN bytes, string)
 *
**/


/**
 * The diamond.dat is a binary file which contains some records. Each record identifies
 * a single diamond and is composed as follows.
 * Timestamp (4 bytes unsigned int) - SpotId (4 bytes, integer) - DescriptionLength (4 bytes, integer) - UserId (4 bytes, integer) - Latitude (8 bytes, double) - Longitude (8 bytes, double) - Description(MAX_USER_LEN bytes, string)
**/
#endif /* TREASURECAVEDB_H_ */
