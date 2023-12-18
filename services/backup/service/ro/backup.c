#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

unsigned int num_files;
char name[100];
char password[100];

struct temp_files {
    char* contents;
    unsigned int size;
    struct temp_files* next;
};

struct temp_files* head = NULL;


int readline(char *buf, int size){
    int i;
    for(i=0; i < size; i++) {
        if(read(0,buf+i,1) <= 0) {
            exit(1);
        }
        if (buf[i] == '\n') {
            buf[i] = '\x00';
            return i;
        }
    }
    buf[size-1] = '\x00';
    return size-1;
}

void read_in_bytes(char* new_file, unsigned int the_size) {
    int i = 0;
    while(i < the_size)
    {
        if(read(0,new_file+i,1) !=1)
        {
            exit(0);
        }
        i += 1;
    }
}

void printmenu()
{
    printf("\nHello, welcome to the secure data storage system. \n");
    printf("(1) Securely start backup.\n");
    printf("(2) Retrieve secure backup.\n");
    printf("(3) Exit.\n");
    printf("> ");
    fflush(stdout);
}
void print_backup_menu() {
    printf("You currently have %d files ready to be stored for backup. \n", num_files);
    printf("(1) Add a file.\n");
    printf("(2) Remove all files.\n");
    printf("(3) Store files. \n");
    printf("(4) Return to menu without saving.\n");
    printf("> ");
    fflush(stdout);
}

void add_file()
{
    char size[20];
    unsigned int the_size;
    char* new_file;
    struct temp_files* tmp;
    printf("How big (in bytes) is your files ");
    fflush(stdout);
    readline(size,20);

    the_size = atoi(size)+1;
    new_file = malloc(the_size);

    printf("Go ahead, send you file\n");
    fflush(stdout);

    read_in_bytes(new_file, the_size);


    if (head == NULL)
    {
        head = (struct temp_files*) malloc(sizeof(struct temp_files));
        head->contents = NULL;
        head->next = NULL;
    }
    tmp = head;
    while(tmp->next != NULL) {
        tmp = tmp->next;
    }
    tmp->next = (struct temp_files*) malloc(sizeof(struct temp_files));
    tmp->next->next = NULL;
    tmp->next->contents = new_file;
    tmp->next->size = the_size;

}
void strip(char *s) {
    int pos = strlen(s) - 1;
    if (s[pos] == '\n')
        s[pos] = '\0';
}

void get_info() {

    if(name[0] == '\0' || password[0] == '\0') {
        puts("Select a name for your backup:");
        fgets(name, 100, stdin);
        strip(name);

        puts("Choose a secure password for your backup:");
        fgets(password, 100, stdin);
        strip(password);

    }

}

void store_files() {




    struct temp_files* tmp;
    tmp = head;
    if (tmp != NULL) {
        tmp = tmp->next;

        char file_path[200];
        snprintf(file_path, 200, "%s_%s.secure.bak", name, password);

        FILE* f = fopen(file_path, "w");
        fprintf(f, "%s", tmp->contents);
        fclose(f);

        printf("\nStored successly %d files\n", num_files);

        free(head);
        head = NULL;

    }
}


void cal_num() {


        struct temp_files* tmp1;
        tmp1 = head;
        num_files = 0;

        while(tmp1 != NULL) {
            num_files += 1;
            tmp1 = tmp1->next;
            if (tmp1->next == NULL ){
                break;
            }
        }

}

void start_backup() {

    get_info();
    while(1){

        cal_num();
        print_backup_menu();

        char input[20];
        readline(input,20);
        if (!strcmp(input,"1"))
        {

            add_file();
        }
        else if (!strcmp(input,"2"))
        {
            free(head);
            head = NULL;
        } else if (!strcmp(input,"3")) {
            store_files();
        } else  {
            break;
        }

    }

}

void retrieve_backup()
{
    char cmd[200];
    get_info();

    printf("Here is your backup data that was stored securely\n");
    fflush(stdout);
    snprintf(cmd,200,"cat %s_%s.secure.bak", name,password);
    system(cmd);
    printf("\n");
}

int main(int argc, char** argv)
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    char input[40];
    chdir("/home/chall/service/rw/");
    while(1)
    {
        printmenu();
        readline(input,40);
        if (!strcmp(input,"1"))
        {
            start_backup();
        }
        else if (!strcmp(input,"2"))
        {
            retrieve_backup();
        } else if (!strcmp(input,"3")){
            printf("Goodbye!\n");
            fflush(stdout);
            return 0;
        }

    }

 return 0;
}
