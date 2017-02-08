# Compute specificity of nodes based on random terminals randomizations The summary file
# displays how often each node was found in each random network.  Usually we want nodes that
# rarely appear in random networks The specificity is then plotted as 1-total.scores$score
# VERSION 2016-10-20

# Script that summarizes all the scores across randomizations
library("data.table")
library("dplyr")
library("stringr")
library("yaml")

# load project path
x<-yaml.load_file("specification_sheet.yaml")
TF<-as.character(x["projectPath"])


######################
# compute specificity
######################

sources.files <- list.files(path = TF, recursive = T, pattern = "*_randomTerminals_nodeattributes.tsv", 
    full.names = T)

sources.files

final.mat <- data.frame()
for (i in 1:length(sources.files)) {
    current.file <- sources.files[i]
    # current.file<-sources.files[2]
    dat <- fread(current.file, data.table = F, header = T)
    if (i == 1) {
        final.mat <- dat
    } else {
        final.mat <- merge(final.mat, dat, by = "Protein", all=T)
    }
}

column_names <- colnames(final.mat)
nodes.scores <- final.mat[, !is.na(str_extract(column_names, "FractionOfOptimalForestsContaining"))]

# Replace NAs with 0
nodes.scores[is.na(nodes.scores)] = 0

# Total number of batches of randomizations B is the number of batches
B <- ncol(nodes.scores)
total.scores <- data.frame(nodes = matrix(NA, nrow = nrow(nodes.scores)), score = matrix(NA, 
    nrow = nrow(nodes.scores)))
total.scores$score <- rowSums(nodes.scores)/B

# Create new column with interactors
total.scores$nodes <- final.mat$Protein

# Export file with scores
dir.create(paste0(TF,"/summary/"), showWarnings=F)
filename <- str_c(TF, "/summary/summary_nodes_specificity.txt")
write.table(total.scores, file = filename, quote = F, sep = "\t", row.names = F, col.names = F)

######################
# compute robustness
######################
sources.files <- list.files(path = TF, recursive = T, pattern = "*_noisy_nodeattributes.tsv", 
    full.names = T)

final.mat <- data.frame()
for (i in 1:length(sources.files)) {
    current.file <- sources.files[i]
    # current.file<-sources.files[2]
    dat <- fread(current.file, data.table = F, header = T)
    if (i == 1) {
        final.mat <- dat
    } else {
        try(final.mat <- merge(final.mat, dat, by = "Protein", all=T))
    }
}

column_names <- colnames(final.mat)
nodes.scores <- final.mat[, !is.na(str_extract(column_names, "FractionOfOptimalForestsContaining"))]

# Replace NAs with 0
nodes.scores[is.na(nodes.scores)] = 0

# Total number of batches of randomizations B is the number of batches
B <- ncol(nodes.scores)
total.scores <- data.frame(nodes = matrix(NA, nrow = nrow(nodes.scores)), score = matrix(NA, 
    nrow = nrow(nodes.scores)))
total.scores$score <- rowSums(nodes.scores)/B

# Create new column with interactors
total.scores$nodes <- final.mat$Protein

# Export file with scores
filename <- str_c(TF, "/summary/summary_nodes_robustness.txt")
write.table(total.scores, file = filename, quote = F, sep = "\t", row.names = F, col.names = F)


######################
# compute randomization scores
######################
sources.files <- list.files(path = TF, recursive = T, pattern = "*_noisy_edgeattributes.tsv", 
    full.names = T)

final.mat <- data.frame()
for (i in 1:length(sources.files)) { 
    current.file <- sources.files[i]
    # current.file<-sources.files[2]
    dat <- fread(current.file, data.table = F, header = T)
    if (i == 1) {
        final.mat <- dat
    } else {
        final.mat <- merge(final.mat, dat, by = "Edge", all=T)
    }
}

column_names <- colnames(final.mat)
edge.scores <- final.mat[, !is.na(str_extract(column_names, "FractionOfOptimalForestsContaining"))]

# Replace NAs with 0
edge.scores[is.na(edge.scores)] = 0

# Total number of batches of randomizations (usually 10, sometimes 50)
B <- ncol(edge.scores)
total.scores <- data.frame(A = matrix(NA, nrow = nrow(edge.scores)), B = matrix(NA, nrow = nrow(edge.scores)), score = matrix(NA, nrow = nrow(edge.scores)))
total.scores$score <- rowSums(edge.scores)/B

# Create new column with interactors
# final.mat <- tidyr::separate(final.mat, Edge, into = c("A", "pp", "B"), sep = " ")
s<-data.frame(do.call('rbind', strsplit(final.mat$Edge,"(pp)", fixed=T)))
total.scores$A<-s[,1]
total.scores$B<-s[,2]



# Export file with scores
filename <- str_c(TF, "/summary/summary_scores_noisy_edges.txt")
write.table(total.scores, file = filename, quote = F, sep = "\t", row.names = F, col.names = F)

print("3 files written to summary/ ... ignore warnings")
