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
truehist(clean.avg.time)

Y <- clean.avg.time[order(clean.avg.time)]
mean.Y <- mean(Y)
check_fit <- function(k) {
  lambda <- k / mean.Y
  simulated.Y <- rgamma(n = length(Y),
                        shape = k,
                        rate = lambda)
  order.Y.hat <- order(simulated.Y)
  main.title <- paste('k = ', k)
  x.max <- max(Y)
  y.max <- max(simulated.Y)
  plot(
    Y,
    simulated.Y[order.Y.hat],
    cex = 0.1,
    xlim = c(0, x.max),
    ylim = c(0, y.max),
    xlab = 'Y',
    ylab = 'Y.hat',
    main = main.title
  )
  abline(0, 1, col = 'blue')
}

check_fit(1)
check_fit(2)
check_fit(3)
check_fit(4)
check_fit(5)
check_fit(6)
check_fit(7)
check_fit(8)
check_fit(9)
check_fit(10)
check_fit(11)
check_fit(12)

# I choose k = 11 as the best fit because (1) The blue line is almost diagonal.
# This indicates that the range of data on the two axes is almost the same; (2)
# the data is almost along the blue line except at the extremities. (3) The
# upper extremity fits better than the lower extremity.
# 
# Thus average time obeys a gamma distribution with parameters shape = 12 and
# rate = 12/mean(data$Avg.time)