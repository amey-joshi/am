# There are 96 records per day. Ideally, one should not use more than those many
# points to predict.

library(tseries)
data <- read.csv('wait_prob_1.csv')

E.series <- data$E[!is.na(data$E)]
result.0 <- adf.test(E.series)
result.1 <- acf(E.series, lag = 150)
p <- which(result.1$acf < 0.05)[1]
result.2 <- pacf(E.series)
q <- which(result.2$acf < 0.05)[1]
d <- 1
train.limit <- 3 * p 
result.3 <-
  arima(E.series[1:train.limit], 
        order = c(p, d, q), method = 'CSS', optim.control = list(maxit=1000))
# There is no convergence problem now.

n.ahead <- 5
result.4 <- predict(result.3, n.ahead = n.ahead)
E.pred <- result.4$pred
E.actual <- E.series[(train.limit + 1):(train.limit + n.ahead)]
plot(E.actual, E.pred, cex = 0.2)
