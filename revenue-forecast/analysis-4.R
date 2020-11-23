# Segment 1: time series analysis of ARPU.
library(tseries)
seg <- read.csv('segment-1.csv')
seg$month <- substr(seg$Date, 1, 2)

arpu <- seg$ARPU
plot(
  arpu,
  cex = 0.1,
  xlab = 'time',
  ylab = 'ARPU',
  main = 'Linear model'
)
time <- seq(1, length(arpu))
m1 <- lm(arpu ~ time)
abline(m1, col = 'blue')
# The linear model is not bad but one should try something better.

m2 <- lm(arpu ~ time + I(time ^ 2))
summary(m2)
arpu.pred <- predict(m2, newdata = data.frame(time = time))
plot(
  arpu,
  arpu.pred,
  cex = 0.1,
  xlab = 'Actual ARPU',
  ylab = 'Predicted ARPU',
  main = 'Performance of quadratic model'
)
abline(0, 1)
# The quadratic model fits best for daily data.

future.times <- seq(from = 366, to = 366 + 90)
future.arpu  <-
  predict(m2, newdata = data.frame(time = future.times))

all.arpu <- c(arpu, future.arpu)
plot(
  all.arpu,
  cex = 0.1,
  xlab = 'time',
  ylab = 'ARPU',
  main = 'Actual + Predicted ARPU'
)

# Analysis of monthly data.

seg.agg <- aggregate(ARPU ~ month, data = seg, sum)
m.arpu <- seg.agg$ARPU
plot(
  m.arpu,
  cex = 0.1,
  xlab = 'time',
  ylab = 'Monthly ARPU',
  main = 'Linear model for monthly data'
)
time <- seq(1, nrow(seg.agg))
m3 <- lm(m.arpu ~ time)
abline(m3, col = 'blue')
# Not a great fit.

adf.test(m.arpu)
# The time series is not stationary.
adf.test(diff(m.arpu))
# This too is not stationary.
# Therefore, no time series analysis can be done. We will go with the 20% increase
# rule.

# How does data aggregated from prediction of daily series look like?
jan.arpu <- sum(future.arpu[1:31])
feb.arpu <- sum(future.arpu[32:59])
mar.arpu <- sum(future.arpu[60:91])

# Monthly ARPU predicted this way does not show 20% increase. Therefore, the
# only way out is to calculate the daily rate of increase needed to give 20%
# growth in three months.
#
# There are 31 + 28 + 31 = 90 days in first quarter of 2019. If r is daily rate
# of growth then
r = (1.2) ^ (1 / 90) - 1

fut.lin.arpu <- arpu[365] * (1 + r) ^ (1:90)
plot(
  fut.lin.arpu,
  xlab = seq(1, 90),
  ylab = 'Future ARPU',
  main = 'ARPU at 20% rate',
  cex = 0.1
)

jan.arpu <- sum(fut.lin.arpu[1:31])
feb.arpu <- sum(fut.lin.arpu[32:59])
mar.arpu <- sum(fut.lin.arpu[60:90])
