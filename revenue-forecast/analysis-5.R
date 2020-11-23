# Segment 2: time series analysis of 'Total paid customers'.
seg <- read.csv('segment-2.csv')
seg$month <- substr(seg$Date, 1, 2)

tpc <- seg$Total.paid.customers
mrr <- seg$Segment.2.MRR
adf.test(tpc)
# The series is not stationary.
adf.test(diff(tpc))
# The first differences are stationary.
acf(diff(tpc), main = '1st difference of TPC', lag.max = 100)
#
pacf(diff(tpc), lag.max = 100)
m1 <-
  arima(
    tpc,
    order = c(12, 0, 0),
    method = "ML",
    optim.control = list(maxit = 1000)
  )
future.tpc <- predict(m1, n.ahead = 90)
all.tpc <- c(tpc, future.tpc$pred)
plot(
  tpc,
  xlim = c(0, length(all.tpc)),
  ylim = c(0, max(all.tpc)),
  col = 'blue',
  cex = 0.1,
  xlab = 'time',
  ylab = 'TPC',
  main = 'Current and future TPC'
)
points(seq(from = 366, to = length(all.tpc)),
       future.tpc$pred,
       col = 'red',
       cex = 0.1)

adf.test(mrr)
acf(mrr, lag.max = 120, main = 'MRR') # ACF persists for a very long time, 116 lags
pacf(mrr, main = 'MRR') # Does not look like MA process.
m2 <- arima(mrr, order = c(100, 0, 0), method = "ML", optim.control = list(maxit=1000))
