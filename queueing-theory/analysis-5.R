library(queueing)
library(MASS)

data <- read.csv('wait_prob_1.csv')
# Use only weekday's data.
data <- data[data$isoday_of_week < 6, colnames(data)]

# Examination of average time.
summ.avg.time <- summary(data$Avg.time)
q1 <- summ.avg.time[2]
q3 <- summ.avg.time[5]
iqr <- IQR(data$Avg.time)
upper.limit <- q3 + 1.5 * iqr
lower.limit <- max(q1 - 1.5 * iqr, 0)

clean.avg.time <- data$Avg.time[lower.limit < data$Avg.time & data$Avg.time < upper.limit]

X <- data$ncalls[data$ncalls > 0]
Y <- clean.avg.time[order(clean.avg.time)]
lambda <- mean(X)
mu <- 12/mean(Y)

# Try a queueing model.
model.1 <- NewInput.MM1(lambda = lambda, mu = mu)
CheckInput(model.1)
qm.1 <- QueueingModel(model.1)
print(summary(qm.1))

main.title <- 'Distribution of waiting times'
fw <- qm.1$FW
fwq <- qm.1$FWq

y.label <- 'F_w, F_{w_q}'
curve(fw, from = 0, to = 1, xlab = 't', ylab = y.label, main = main.title, col='black')
curve(fwq, from = 0, to = 1, col = 'blue')
legend('bottomright', legend = c('Fw', 'F_{w_q}'), cols = c('black', 'blue'))
