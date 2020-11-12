library(tseries)
data <- read.csv('wait_prob_1.csv')

E.series <- E.series[!is.na(data$E)]
plot(
  seq(1, length(E.series)),
  E.series,
  cex = 0.1,
  main = 'Traffic by time',
  xlab = 'Time',
  ylab = 'Traffic'
)
# The plot indicates that the time series might be stationary. Let's check it
# with a formal test.
result.0 <- adf.test(E.series)
# The p-value is < 0.05 and we can accept the alternative hypothesis that the
# series is indeed stationary.

result.1 <- acf(E.series, lag = 150)
p <- which(result.1$acf < 0.5)[1]

result.2 <- pacf(E.series)
# The partial auto-correlation function plot shows that the function decays only
# after lag = 14. It also drops after lag = 10. I am inclined to select lag = 10
# because the rise at lag = 13 seems to be by chance.
q <- which(result.2$acf < 0.05)[1]

# We did not choose differences of the series. The original series itself was
# stationary. Therefore,
d <- 0

# Let's try to fit ARIMA model.
train.limit <- 1500 # We use first 1500 points for prediction
result.3 <-
  arima(E.series[1:train.limit], order = c(p, d, q), method = 'CSS')

result.4 <-
  predict(result.3, n.ahead = length(E.series) - train.limit)
E.pred <- result.4$pred
E.actual <- E.series[(train.limit + 1):length(E.series)]

plot(
  seq(1, length(E.pred)),
  E.pred,
  cex = 0.1,
  xlab = 'Time',
  ylab = 'Predicted E',
  main = 'Traffic prediction'
)
points(seq(1, length(E.pred)), E.actual, cex = 0.1, col = 'blue')
# The plot shows that the model is quite bad.
