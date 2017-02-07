library(stringr)

# Script that generates parameters for running a parameter search

# Get parameters
args <- commandArgs(trailingOnly = TRUE)

W_input <-args[1]
B_input <-args[2]
D_input <-args[3]
mu_input <-args[4]
resultPath <-args[5]

#Function to process parameters
process_parameters<-function(input){
  #First parameter will be W, then B, then D and then mu
  #param<-str_split(input,"_",simplify = TRUE)
  #param<-as.numeric(param)

  param<-str_split(input,"_")
  param<-as.numeric(unlist(param))

  output<-seq(param[1],param[2],param[3])
  return(output)
}

W_vector<-process_parameters(W_input)
B_vector<-process_parameters(B_input)
#B_vector<-c(B_vector[1], 1 ,B_vector[2:length(B_vector)])
D_vector<-process_parameters(D_input)
mu_vector<-process_parameters(mu_input)

#Create all combinations of supplied vectors or factor
all_combinations<-expand.grid(W_vector,B_vector,D_vector,mu_vector)
colnames(all_combinations)<-c("w","b","D","mu")

for(i in 1:nrow(all_combinations)){
  #print(i)
  tmp<-all_combinations[i,]
  print(tmp)
  tmp1<-colnames(tmp[1])
  tmp2<-colnames(tmp[2])
  tmp3<-colnames(tmp[3])
  tmp4<-colnames(tmp[4])

  #filename<-str_c(tmp1,tmp[1],tmp2,tmp[2],tmp3,tmp[3],tmp4,tmp[4],sep = "_")
  filename<-str_c("W",tmp[1],"BETA",tmp[2],"D",tmp[3],"mu",tmp[4],sep = "_")
  filename<-str_c(resultPath,filename,".params")

  out1<-str_c(tmp1,"=",tmp[1],sep=" ")
  out2<-str_c(tmp2,"=",tmp[2],sep = " ")
  out3<-str_c(tmp3,"=",tmp[3],sep = " ")
  out4<-str_c(tmp4,"=",tmp[4],sep = " ")

  out<-t(data.frame(out1,out2,out3,out4))

  write.table(out,file=filename,quote = FALSE,row.names = FALSE,col.names = FALSE)
}
