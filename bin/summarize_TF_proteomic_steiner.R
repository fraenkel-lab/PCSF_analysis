library(data.table)
library(stringr)
# library(tidyr)
library(dplyr)

# Input arguments
args <- commandArgs(trailingOnly = TRUE)
projectPath <- args[1]

# List all directories in the path
all.directories <- list.dirs(projectPath)

# Remove all out_data and randomizations
all.directories <- all.directories[is.na(str_match(all.directories, "out_data"))]
all.directories <- all.directories[is.na(str_match(all.directories, "randomizations"))]

# List all node attributes file
all.files <- list.files(path = all.directories, pattern = "*_nodeattributes.tsv", full.names = TRUE)

# Remove results from out_data all.files<-all.files[(is.na(str_match(all.files,'out_data')))]
tmp <- as.data.frame(all.files)

out.df <- data.frame(matrix(ncol = 1, nrow = 3))
colnames(out.df) <- c("node_type")

for (index in 1:length(all.files)) {
    # for(index in 1:2){
    current.file <- all.files[index]
    # print(current.file)
    table <- fread(current.file, sep = "\t")
    # print(table)

    # Replace empty nodes
    table$TerminalType[table$TerminalType == ""] = "Steiner"

    summary <- table %>% dplyr::group_by(TerminalType) %>% dplyr::tally() %>% as.data.frame()
    # rownames(summary)<-summary$TerminalType
    colnames(summary) <- c("node_type", str_replace(basename(current.file), "_nodeattributes.tsv",
        ""))
    # summary<-summary$n
    if (index == 1) {
        out.df <- summary
    } else {
        out.df <- dplyr::full_join(out.df, summary, by = "node_type")
    }

}

# Transpose data
out.table <- t(out.df)
colnames(out.table) <- out.table[1, ]

# Remove first row of the data frame because we don't need it
out.table <- out.table[2:nrow(out.table), ]
parameters <- rownames(out.table)

out.table <- as.data.frame(out.table)
out.table$file <- parameters

out.table$file <- str_replace(out.table$file, ".x", "")
out.table$file <- str_replace(out.table$file, ".y", "")

# ensure that TF column is here
out.table$TF <- NA

# Divide into separate columns
# out.table <- tidyr::separate(out.table, file, into = c("W", "w.val", "BETA", "BETA.val", "D",
#    "D.val", "mu", "mu.val"), sep = "_", remove = "FALSE")
s<-data.frame(do.call('rbind', strsplit(rownames(out.table), '_')))
out.table$mu.val<-as.numeric(s[,dim(s)[2]])
out.table$D.val<-as.numeric(s[,dim(s)[2]-2])
out.table$BETA.val<-as.numeric(s[,dim(s)[2]-4])
out.table$w.val<-as.numeric(s[,dim(s)[2]-6])

out.table$Proteomic <- as.numeric(as.character(out.table$Proteomic))
out.table$TF <- as.numeric(as.character(out.table$TF))
out.table$Steiner <- as.numeric(as.character(out.table$Steiner))

# We can replace this to complete cases
out.table$Proteomic[is.na(out.table$Proteomic)] <- 0
out.table$TF[is.na(out.table$TF)] <- 0
out.table$Steiner[is.na(out.table$Steiner)] <- 0

out.table.file <- str_c(projectPath, "out_data/summary/summary_TF_proteomic_steiner.tsv")
write.table(out.table, file = out.table.file, quote = FALSE, col.names = TRUE, row.names = FALSE,
    sep = "\t")
