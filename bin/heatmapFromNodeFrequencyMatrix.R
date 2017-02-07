printUsage <- function() {
    print("This script will create a heatmap from a node frequency matrix as created by Tobi's PCSF param sweep summarization python script.")
    print("Please provide the following arguments (in this order!):")
    print("  -1- Path to node freq matrix.")
}

params <- commandArgs(T)

DEFAULT_MARGIN_COL <- 16
DEFAULT_MARGIN_ROW <- 7
DEFAULT_PLOT_W <- 15
DEFAULT_PLOT_H <- 20

### DEBUG params <- c(
### '/nfs/latdata/tobieh/medullo/MetabAndPhosphoprot/analyses/PCSF/paul.SNVs/terms.all.in.subgroup/1_sweep_analysis/promising.from.sweep/promising.filtered/CrossSubgroupCrossTerm_networkNodeMatrix.tsv'
### ,'x' )
if (length(params) >= 1) {
    require(RColorBrewer)
    require(gplots)
    require(stringr)
    options(bitmapType = "cairo")
    options(stringsAsFactors = FALSE)
    
    matrPath <- params[1]
    # matrPath <-
    # '/nfs/latdata/tobieh/medullo/MetabAndPhosphoprot/analyses/PCSF/paul.SNVs/terms.by.subgroup/promising.from.sweep/crossSubgroupComparison_networkNodeMatrix.tsv'
    colorSubgroups <- length(params) > 1 && params[2] == "x"
    if (colorSubgroups) {
        print("Unlocking secret Subgroup Coloring Option...")
        subgroups <- c("WNT", "SHH", "Group3", "Group4")
        colors <- data.frame(Color = c("cornFlowerBlue", "fireBrick1", "goldenrod1", "darkoliveGreen4"), 
            stringsAsFactors = F)
        rownames(colors) <- subgroups
    }
    plotW <- DEFAULT_PLOT_W
    plotH <- DEFAULT_PLOT_H
    plotMargins <- c(DEFAULT_MARGIN_COL, DEFAULT_MARGIN_ROW)
    x <- read.table(matrPath, sep = "\t", header = T)
    rownames(x) <- x[, 1]
    x <- x[, -1]
    isTerm <- x$IS_TERMINAL == 1
    rownames(x) <- mapply(function(x, y) {
        if (y) 
            paste0(x, " *T*") else x
    }, rownames(x), isTerm)
    x <- x[, -c((ncol(x) - 1):ncol(x))]
    x <- as.matrix(x)
    colnames(x) <- sapply(colnames(x), function(x) {
        strsplit(x, "_optimalF")[[1]][1]
    })
    outPath <- paste(matrPath, "_heatmap.pdf", sep = "")
    pdf(outPath, width = plotW, height = plotH)
    clustfun <- function(sth) hclust(sth, method = "average")
    rsColors <- c("hotpink", "gray")[isTerm + 1]
    if (!colorSubgroups) {
        heatmap.2((x > 0) * 1, main = "All Nodes across Networks", hclustfun = clustfun, RowSideColors = rsColors, 
            trace = "none", scale = "none", col = c("white", "black"), margins = plotMargins, 
            key = F, sub = matrPath, srtCol = 40)
        legend("topright", legend = c("Steiner Node", "Terminal Node"), col = c("hotpink", "gray"), 
            lty = 1, lwd = 10, cex = 0.8)
        heatmap.2(x, main = "All Nodes across Networks (color is degree)", hclustfun = clustfun, 
            RowSideColors = rsColors, trace = "none", scale = "none", col = c("white", rev(heat.colors(max(x) + 
                2))), margins = plotMargins, key = T, sub = matrPath, srtCol = 40, keysize = 1)
        legend("topright", legend = c("Steiner Node", "Terminal Node"), col = c("hotpink", "gray"), 
            lty = 1, lwd = 10, cex = 0.8)
        
        heatmap.2((x[isTerm, ] > 0) * 1, main = "Terminal Nodes across Networks", hclustfun = clustfun, 
            trace = "none", scale = "none", col = c("white", "black"), margins = plotMargins, 
            key = F, sub = matrPath, srtCol = 40)
        heatmap.2(x[isTerm, ], main = "Terminal Nodes across Networks (color is degree)", hclustfun = clustfun, 
            trace = "none", scale = "none", col = c("white", rev(heat.colors(max(x[isTerm, ]) + 
                2))), margins = plotMargins, key = T, sub = matrPath, srtCol = 40, keysize = 1)
        
        heatmap.2((x[!isTerm, ] > 0) * 1, main = "Steiner Nodes across Networks", hclustfun = clustfun, 
            trace = "none", scale = "none", col = c("white", "black"), margins = plotMargins, 
            key = F, sub = matrPath, srtCol = 40)
        heatmap.2(x[!isTerm, ], main = "Steiner Nodes across Networks (color is degree)", hclustfun = clustfun, 
            trace = "none", scale = "none", col = c("white", rev(heat.colors(max(x[!isTerm, ]) + 
                2))), margins = plotMargins, key = T, sub = matrPath, srtCol = 40, keysize = 1)
    } else {
        # secret subgroup-coloring option!
        cols <- sapply(colnames(x), function(name) {
            if (!is.na(str_match(name, rownames(colors)[1]))) {
                colors$Color[1]
            } else if (!is.na(str_match(name, rownames(colors)[2]))) {
                colors$Color[2]
            } else if (!is.na(str_match(name, rownames(colors)[3]))) {
                colors$Color[3]
            } else if (!is.na(str_match(name, rownames(colors)[4]))) {
                colors$Color[4]
            } else {
                "white"
            }
        })
        heatmap.2((x > 0) * 1, main = "All Nodes across Networks", ColSideColors = cols, hclustfun = clustfun, 
            RowSideColors = rsColors, trace = "none", scale = "none", col = c("white", "black"), 
            margins = plotMargins, key = F, sub = matrPath, srtCol = 40, keysize = 0.9)
        legend("topright", legend = c(rownames(colors), "", "Steiner Node", "Terminal Node"), 
            col = c(colors$Color, "white", "hotpink", "gray"), lty = 1, lwd = 10, cex = 0.8)
        heatmap.2(x, main = "All Nodes across Networks (color is degree)", ColSideColors = cols, 
            hclustfun = clustfun, RowSideColors = rsColors, trace = "none", scale = "none", col = c("white", 
                rev(heat.colors(max(x) + 2))), margins = plotMargins, key = T, sub = matrPath, 
            srtCol = 40, keysize = 0.9)
        legend("topright", legend = c(rownames(colors), "", "Steiner Node", "Terminal Node"), 
            col = c(colors$Color, "white", "hotpink", "gray"), lty = 1, lwd = 10, cex = 0.8)
        
        heatmap.2((x[isTerm, ] > 0) * 1, main = "Terminal Nodes across Networks", ColSideColors = cols, 
            hclustfun = clustfun, trace = "none", scale = "none", col = c("white", "black"), 
            margins = plotMargins, key = F, sub = matrPath, srtCol = 40, keysize = 0.9)
        legend("topright", legend = rownames(colors), col = colors$Color, lty = 1, lwd = 10, 
            cex = 0.8)
        heatmap.2(x[isTerm, ], main = "Terminal Nodes across Networks (color is degree)", ColSideColors = cols, 
            hclustfun = clustfun, trace = "none", scale = "none", col = c("white", rev(heat.colors(max(x[isTerm, 
                ]) + 2))), margins = plotMargins, key = T, sub = matrPath, srtCol = 40, keysize = 1)
        legend("topright", legend = rownames(colors), col = colors$Color, lty = 1, lwd = 10, 
            cex = 0.8)
        
        heatmap.2((x[!isTerm, ] > 0) * 1, main = "Steiner Nodes across Networks", ColSideColors = cols, 
            hclustfun = clustfun, trace = "none", scale = "none", col = c("white", "black"), 
            margins = plotMargins, key = F, sub = matrPath, srtCol = 40, keysize = 0.9)
        legend("topright", legend = rownames(colors), col = colors$Color, lty = 1, lwd = 10, 
            cex = 0.8)
        heatmap.2(x[!isTerm, ], main = "Steiner Nodes across Networks (color is degree)", ColSideColors = cols, 
            hclustfun = clustfun, trace = "none", scale = "none", col = c("white", rev(heat.colors(max(x[!isTerm, 
                ]) + 2))), margins = plotMargins, key = T, sub = matrPath, srtCol = 40, keysize = 0.9)
        legend("topright", legend = rownames(colors), col = colors$Color, lty = 1, lwd = 10, 
            cex = 0.8)
        
        
        getWithinSubgroupFrequencies <- function(x, cols) {
            groups <- factor(cols)
            x.by.group <- sapply(levels(groups), function(gr) rowSums(x[, which(groups == gr)] > 
                0)/sum(groups == gr))
        }
        
        x.by.sg <- getWithinSubgroupFrequencies(x, cols)
        colors.x.sg <- colnames(x.by.sg)
        colnames(x.by.sg) <- rownames(colors)[match(colnames(x.by.sg), colors$Color)]
        heatmap.2(x.by.sg, main = "Frequency of Nodes in Networks within Subgroups", hclustfun = clustfun, 
            RowSideColors = rsColors, ColSideColors = colors.x.sg, trace = "none", scale = "none", 
            col = colorRampPalette(c("white", "blue", "red"))(n = 10), margins = plotMargins, 
            key = T, srtCol = 40, keysize = 0.9)
        legend("topright", legend = c(rownames(colors), "", "Steiner Node", "Terminal Node"), 
            col = c(colors$Color, "white", "hotpink", "gray"), lty = 1, lwd = 10, cex = 0.8)
        
        row.idxs.sg <- which(rowSums(x.by.sg == 0) == 3)
        heatmap.2(x.by.sg[row.idxs.sg, ], main = "Nodes that are exclusive to networks of a single subgroup", 
            hclustfun = clustfun, RowSideColors = rsColors[row.idxs.sg], ColSideColors = colors.x.sg, 
            trace = "none", scale = "none", col = colorRampPalette(c("white", "blue", "red"))(n = 50), 
            margins = plotMargins, key = T, srtCol = 40, keysize = 0.9)
        legend("topright", legend = c(rownames(colors), "", "Steiner Node", "Terminal Node"), 
            col = c(colors$Color, "white", "hotpink", "gray"), lty = 1, lwd = 10, cex = 0.8)
        
        row.idxs.sg <- which(rowSums(x.by.sg == 0) == 3 & rowSums(x.by.sg) >= 0.5)
        heatmap.2(x.by.sg[row.idxs.sg, ], main = "Nodes that are exclusive to a subgroup and appear in >=50% of networks of that subgroup", 
            hclustfun = clustfun, RowSideColors = rsColors[row.idxs.sg], ColSideColors = colors.x.sg, 
            trace = "none", scale = "none", col = colorRampPalette(c("white", "blue", "red"))(n = 10), 
            margins = plotMargins, key = T, srtCol = 40, keysize = 0.9)
        legend("topright", legend = c(rownames(colors), "", "Steiner Node", "Terminal Node"), 
            col = c(colors$Color, "white", "hotpink", "gray"), lty = 1, lwd = 10, cex = 0.8)
        
        row.idxs.sg <- which(rowSums(x.by.sg == 0) == 3 & rowSums(x.by.sg) >= 0.75)
        heatmap.2(x.by.sg[row.idxs.sg, ], main = "Nodes that are exclusive to a subgroup and appear in >=75% of networks of that subgroup", 
            hclustfun = clustfun, RowSideColors = rsColors[row.idxs.sg], ColSideColors = colors.x.sg, 
            trace = "none", scale = "none", col = colorRampPalette(c("white", "blue", "red"))(n = 10), 
            margins = plotMargins, key = T, srtCol = 40, keysize = 0.9)
        legend("topright", legend = c(rownames(colors), "", "Steiner Node", "Terminal Node"), 
            col = c(colors$Color, "white", "hotpink", "gray"), lty = 1, lwd = 10, cex = 0.8)
        
        row.idxs.sg <- which(rowSums(x.by.sg == 0) == 3 & rowSums(x.by.sg) == 1)
        heatmap.2(x.by.sg[row.idxs.sg, ], main = "Nodes that are exclusive to a subgroup and appear in all networks of that subgroup", 
            hclustfun = clustfun, RowSideColors = rsColors[row.idxs.sg], ColSideColors = colors.x.sg, 
            trace = "none", scale = "none", col = colorRampPalette(c("white", "blue", "red"))(n = 10), 
            margins = plotMargins, key = T, srtCol = 40, keysize = 0.9)
        legend("topright", legend = c(rownames(colors), "", "Steiner Node", "Terminal Node"), 
            col = c(colors$Color, "white", "hotpink", "gray"), lty = 1, lwd = 10, cex = 0.8)
        
    }
    
    par(mar = c(7, 10, 2, 2))
    n <- 75
    if (nrow(x) < n) 
        n <- nrow(x)
    barplot(sort(rowSums(x > 0)/ncol(x), decr = F)[(nrow(x) - n):nrow(x)], horiz = T, las = 2, 
        cex.names = 0.75, main = paste0("Top ", n, " nodes across networks"), xlab = "[Fraction of networks node appears in]", 
        xlim = c(0, 1))
    xt <- x[which(isTerm), ]
    n <- 75
    if (nrow(xt) < n) 
        n <- nrow(xt)
    barplot(sort(rowSums(xt > 0)/ncol(xt), decr = F)[(nrow(xt) - n):nrow(xt)], horiz = T, las = 2, 
        cex.names = 0.75, main = paste0("Top ", n, " terminal nodes across networks"), xlab = "[Fraction of networks node appears in]", 
        xlim = c(0, 1))
    xs <- x[which(!isTerm), ]
    n <- 75
    if (nrow(xs) < n) 
        n <- nrow(xs)
    barplot(sort(rowSums(xs > 0)/ncol(xs), decr = F)[(nrow(xs) - n):nrow(xs)], horiz = T, las = 2, 
        cex.names = 0.75, main = paste0("Top ", n, " Steiner nodes across networks"), xlab = "[Fraction of networks node appears in]", 
        xlim = c(0, 1))
    dev.off()
    print(paste("Created", outPath, sep = " "))
} else {
    printUsage()
}
