data <- read.csv('wait_prob_1.csv')
calls <- data$ncalls
d <- ts(calls, frequency = 160)
plot(d)
# The series does not appear to have seasonality.
# 
library(tseries)
adf.test(calls)
# The small p value suggests that the time series does not have a unit root.
# That is, it does not have a trend.

acf(calls)
pacf(calls)
# The ACF first falls below 0.05 at lag = 28. The PACF first falls below 0.05
# at lag = 5. Given the long lag, it might help to check if the first difference
# of the series has a better behavior.
acf(diff(calls))
pacf(diff(calls))
# The acf plot suggests that p = 1. The fact that we considered first difference
# suggests that d = 1. The pacf plot isn't that encouraging.
sample <- calls[1:20]
fit.0 <- arima(diff(sample), c(1, 1, 0))
summary(fit.0)
pred.0 <- predict(fit.0, n.ahead = 10)

