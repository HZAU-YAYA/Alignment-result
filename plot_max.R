#!/usr/bin/env Rscript
library("dplyr")
library("ggplot2")

options(bitmapType='cairo') #关闭服务器与界面的互动响应

run_file <- function(data){
  df <- read.delim(data, header=TRUE)
  df <- df %>% mutate(sort_col = as.numeric(sub("-.*", "", position)))
  df <- df[order(df$sort_col), ]
  df <- df[, -4]
  rownames(df) <- seq(nrow(df))
  return(df)
}

run_plot <- function(data1, data2, data3, prefix, d){
  df1 <- run_file(data1)
  df2 <- run_file(data2)
  df3 <- run_file(data3)
  df1$group <- "df1"
  df2$group <- "df2"
  df3$group <- "df3"
  df <- rbind(df1, df2, df3)
  # 找到第三列和第四列中的最大值
  max_value <- max(df[,2:3])
  # 从数据框中删除具有最大值的行
  #df <- df[!(df[,2]==max_value | df[,3]==max_value),]
  #最大值改为0
  df[df[,2]==max_value, 2]<-0
  df[df[,3]==max_value, 3]<-0
  max_value <- max(df[,2:3])
  df[df[,2]==max_value, 2]<-0
  df[df[,3]==max_value, 3]<-0
  df$position <- factor(df$position, levels = unique(df$position))
  p<-ggplot(df, aes(x = position)) + 
    geom_bar(aes(y = plus, fill = interaction(group, "plus")), stat = "identity", position = position_dodge()) + 
    geom_bar(aes(y = -minus, fill = interaction(group, "minus")), stat = "identity", position = position_dodge()) +
    labs(title = "Positive and Negative Alignment Distribution", x = "Position", y = "Alignment Count") + 
    # 使用scale_fill_manual()函数来指定每个组和每个填充的颜色
    scale_fill_manual(values = c("#F98D63", "#3cc08f", "#2E9FDF", "#FC4E07", "#00AFBB", "#E7B800"), name = "Group and Fill") + 
    theme_classic() + 
    theme(legend.position = "top")+
    theme(axis.text.x=element_text(angle = 90))
  
  if (d=='P'){
    ggsave(paste(prefix, ".map_bar.png", sep=""),p, width=650, height=130, units="mm")
    ggsave(paste(prefix, ".map_bar.pdf", sep=""),p, width=650, height=130, units="mm")
  }else if (d=='G'){
    ggsave(paste(prefix, ".map_bar.png", sep=""),p, width=1050, height=130, units="mm")
    ggsave(paste(prefix, ".map_bar.pdf", sep=""),p, width=1050, height=130, units="mm")
  }
}


add_help_args <- function(args){
  
  if(length(args) != 5) {
    cat("Version: v1.0.0\n")
    cat("Author:Boya Xu\n")
    cat("Email:invicoun@foxmail.com\n")
    cat("Function:画map_blast图片，且去掉最高的那个柱子.\n")
    cat("Example:plot_b.r abundance_species.tsv prefix\n")
    quit()
  }
}

args <- commandArgs(trailingOnly=TRUE)
add_help_args(args)


run_plot(args[1], args[2], args[3], args[4], args[5])
