zz <-read.csv("data.txt", strip.white=TRUE, header=TRUE, sep="\t")
attach(zz)
t.test(col1, col2, var.equal=F)

