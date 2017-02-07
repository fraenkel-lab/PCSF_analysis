printUsage <- function() {
    print("This script will plot the average terminal/steiner degrees (in interactome) based on the network summary file created by Tobi's PCSF param sweep summarization python script.")
    print("Please provide the following arguments (in this order!):")
    print("  -1- Path to node sweep summary table (*_networkSummary.tsv).")
}

DegreeParamPlot <- function(x) {
    par(mar = c(12, 5, 2, 5), xpd = NA, lwd = 4)
    ylimits <- c(0, max(c(x$terminal.avg.degree.in.interactome, x$steiner.avg.degree.in.interactome, 
        x$avg.degree.in.interactome), na.rm = T))
    plot(1:nrow(x), x$terminal.avg.degree.in.interactome, type = "c", col = "blue", axes = F, 
        xlab = NA, ylab = NA, ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$terminal.avg.degree.in.interactome, pch = 2, col = "blue", axes = F, xlab = NA, 
        ylab = NA, ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$steiner.avg.degree.in.interactome, type = "c", col = "darkgreen", axes = F, 
        xlab = NA, ylab = NA, ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$steiner.avg.degree.in.interactome, pch = 1, col = "darkgreen", axes = F, 
        xlab = NA, ylab = NA, ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$avg.degree.in.interactome, type = "c", col = "gold", axes = F, xlab = NA, 
        ylab = NA, ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$avg.degree.in.interactome, pch = 0, col = "gold", axes = F, xlab = NA, 
        ylab = NA, ylim = ylimits)
    par(new = T)
    abline(h = c(50, 75, 25), col = "grey", lwd = 0.8)
    axis(2)
    mtext(side = 2, line = 3, "Average degree in Interactome")
    text(1:nrow(x), -14, labels = rownames(x), srt = 90, cex = 0.75, pos = 2)
    par(new = T)
    ylimits <- c(0, max(x$X..nodes, na.rm = T))
    plot(1:nrow(x), x$X..nodes, type = "c", col = "lightgoldenrod1", axes = F, xlab = NA, ylab = NA, 
        ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$X..nodes, pch = 15, col = "lightgoldenrod1", axes = F, xlab = NA, ylab = NA, 
        ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$X..Steiner, type = "c", col = "lightgreen", axes = F, xlab = NA, ylab = NA, 
        ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$X..Steiner, pch = 16, col = "lightgreen", axes = F, xlab = NA, ylab = NA, 
        ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$X..Terminal, type = "c", col = "lightblue", axes = F, xlab = NA, ylab = NA, 
        ylim = ylimits)
    par(new = T)
    plot(1:nrow(x), x$X..Terminal, pch = 17, col = "lightblue", axes = F, xlab = NA, ylab = NA, 
        ylim = ylimits)
    par(new = T)
    # plot(1:nrow(x), x$netw.coherency, pch=8, col='grey', axes=F, xlab=NA, ylab=NA,
    # ylim=ylimits); par(new=T)
    axis(4)
    mtext(side = 4, line = 3, "# of Nodes")
    legend("topleft", title = "Average Degree in Interactome", legend = c("Terminal", "Steiner", 
        "Combined"), col = c("blue", "darkgreen", "gold"), pch = c(2, 1, 0))
    legend("topright", title = "Number of Nodes", legend = c("# of Terminals", "# of Steiner Nodes", 
        "Network size"), col = c("lightblue", "lightgreen", "lightgoldenrod1"), pch = c(17, 16, 
        15))
    par(new = F)
}

params <- commandArgs(T)

if (length(params) > 0) {
    options(bitmapType = "cairo")
    filepath <- params[1]
    print(paste0("Reading file ", filepath))
    # x <-
    # read.table('/nfs/latdata/tobieh/medullo/MetabAndPhosphoprot/analyses/PCSF/paul.SNVs/terms.all.in.subgroup/1_sweep_analysis/promising.from.sweep/crossSubgroup_networkSummary.tsv',
    # sep='\t',comment.char='@', header=T)
    x <- read.table(filepath, sep = "\t", comment.char = "@", header = T)
    #################################### 
    x <- x[which(x$FILENAME != "__UNION__"), ]
    x$NAME <- sapply(x$FILENAME, function(s) strsplit(as.character(s), "_")[[1]][1])
    rownames(x) <- sapply(x$FILENAME, function(s) strsplit(as.character(s), "_optimal")[[1]][1])
    x <- x[order(x$NAME, x$mu, x$omega, x$beta, x$D), ]
    #################################### 
    png(paste0(filepath, "_degreeParamPlot.png"), width = 1600, height = 900)
    DegreeParamPlot(x)
    dev.off()
    #################################### 
    # png(paste0(filepath, "_degreeParamPlot_filtered.StAvgDegIntLt100.png"), width = 1600, height = 900)
    # x <- x[which(x$steiner.avg.degree.in.interactome < 100 & x$steiner.avg.degree.in.interactome < 
    #    x$terminal.avg.degree.in.interactome + 20 & x$X..nodes > 0), ]
    # DegreeParamPlot(x)
    #dev.off()
    #################################### 
} else {
    printUsage()
}

# ```{r, fig.width = 35, fig.height = 10 , include=FALSE} Gather connectivity data data<-x
# %>%
# gather(node_type,degree,c(terminal.avg.degree.in.interactome,steiner.avg.degree.in.interactome,avg.degree.in.interactome))
# ggplot(data=data,aes(x=index,y=degree, colour=node_type)) + geom_line()
# p<-ggplot(data=data,aes(x=index,y=degree, colour=node_type, shape=node_type)) + geom_line()
# +geom_point(size=2,fill='white') + scale_colour_brewer(palette='Set1')+ theme(axis.text.x =
# element_text(angle = 90, hjust = 1)) p<-p + scale_x_discrete(limits=data$names) ```
# ```{r,include=FALSE} Gather connectivity data data.number.nodes<-x %>%
# gather(node_type,node.number,c(X..nodes,X..Steiner,X..Terminal))
# p2<-ggplot(data=data.number.nodes,aes(x=index,y=node.number, colour=node_type,
# shape=node_type)) + geom_line() +geom_point(size=2,fill='white') +
# scale_colour_brewer(palette='Set2')+ theme(axis.text.x = element_text(angle = 90, hjust =
# 1)) p2<-p2 + scale_x_discrete(limits=data$names) ``` ```{r Connectivity, fig.width = 20,
# fig.height = 1 ,include=FALSE} gg <- ggplotly(p) gg ``` Number nodes ```{r NumberNodes,
# fig.width = 20, fig.height = 1 , include=FALSE} gg2 <- ggplotly(p2) gg2 ```
