 #include <sys/wait.h>
 #include <stdlib.h>
 #include <unistd.h>
 #include <readline/readline.h>
 #include <readline/history.h>
 
 char readline(char **line);
 
 void strstr_separa_tokens(char *line, char *arg0, char *arg1, char *arg2);
 
 int main(){
 	const char arg_shell_line[] = "gustavo**SHELL >> ";
 	char* line;
 	int pid_f;
 	char **args;
 
 	while(1){
 		char *buffer = (char*)malloc(sizeof(char) * 256);
         if (!buffer) {
             printf("Erro na aloca��o de mem�ria\n");
        }
        scanf("%s", &buffer);
       
        line = (char*)malloc(sizeof(char)*((strlen(buffer))+1));       /* Aloca espa�o para a entrada de dados do shell */
        strcpy(line, buffer);
        line[strlen(buffer)] = '\0';
        free(buffer);
        printf("%s\n", line);                                    /* Aloca espa�o para a entrada de dados do shell */                                 
		
		if(!strcmp(line, "sair")){
			break;
		}
		
		
		args = (char**)malloc(sizeof(char)*3);                  /* Aloca espa�o para os ponteiros dos argumentos que ser�o
                                                            recebidos de '"char" *line' */
		for(int i=0; i<3; i++){
             args[i] = (char*)malloc(sizeof(char)*20);           /* Aloca espa�o para os argumentos que ser�o recebidos */
 		}
 
 		strString(line, args[0], args[1], args[2]);             /* Separa os tokens recebidos por '"char" *line' em argumentos
                                                             no vetor '"char" **args', funciona como um strstr e strtok com
                                                             strcpy para armazenamento dos tokens */
 		int pid;
 		pid = fork();
 		if(pid == 0){
 			if (execvp(args[0], args) == -1) {                  /* Executa o primeiro argumento, recebe o vetor de tokens para a
                                                             execu��o dos comando seguintes na fun��o 'execvp' que retorna um
                                                             valor inteiro */
                 perror("Erro no comando \"%s\"", args[0]);      /* Imprime uma mensagem de erro caso o comando apresente alguma
                                                             anomalia */
             }
 			break;
 		}else{
 			int status;
 
 			pid_f = waitpid(-1, &status, 0);
 			printf("%d", pid_f);
 			putchar('\n');
 		}
 
 		free(line);                                             /* Libera o espa�o de entrada '"char" *line' alocado anteriomente */
 		i=3;
 		while(i>=0){                                            /* Libera os espa�os de tokens '"char" **args' que foram alocados
                                                             anteriomente */
             free(args[i]);
 		}
 		free(args);                                             /* Libera o espa�o de vetor de tokens '"char" **args' alocado
                                                             anteriomente */
 	}
 
 	return 0;
 }
 
 void strstr_separa_tokens(char *line, char *arg0, char *arg1, char *arg2){
 
     char *buffer = new char[strlen(line)+1];
     int j=0, chave=0, tam_buffer=0;
 
     tam_buffer = strlen(line);
     strcpy(buffer, line);
     buffer[tam_buffer] = '\0';
 
     for(int i=0; i<tam_buffer; i++){// terminar o codigo e compilar por partes
         if(buffer[i] == ' '){
             if(j>0){
                 if(chave==0){
                     chave = 1;
                     arg0[j] = '\0';
                 }else if(chave==1){
                     chave = 2;
                     arg1[j] = '\0';
                 }else if(chave==2){
                     i = tam_buffer;
                     arg2[j] = '\0';
                     chave = 0;
                 }
                 j = 0;
                 cout << chave << endl; /*/// retirar para nao imprimir o contador chave ///*/
             }
         }else{
             if(chave == 0){
                 arg0[j] = buffer[i];
             }else if(chave == 1){
                 arg1[j] = buffer[i];
             }else if(chave == 2){
                 arg2[j] = buffer[i];
             }
             j++;
         }
     }
     cout << arg0 << endl; /*/// retirar para nao imprimir a string final arg0 ///*/
 
     cout << arg1 << endl; /*/// retirar para nao imprimir a string final arg1 ///*/
 
     cout << arg2 << endl; /*/// retirar para nao imprimir a string final arg2 ///*/
 
     free(buffer);
 }
 
 char readline(char **line){
 
     char *buffer = malloc(sizeof(char) * 256);
     if (!buffer) {
         fprintf(stderr, "Erro na aloca��o de mem�ria\n");
         break;
     }
     scanf("%[^\n]s", &buffer);
 
     line = (char*)malloc(sizeof(char)*((strlen(buffer))+1));
 
     strcpy(line, buffer);
     line[strlen(buffer)] = '\0';
 
     free(buffer);
 }
