library(MASS)
library(vcd)
data <- read.csv('wait_prob_1.csv')
# Use only weekday's data.
data <- data[data$isoday_of_week < 6, colnames(data)]
summ.ncalls <- summary(data$ncalls)
boxplot(data$ncalls)

# The outliers carry critical information. They are not a result of bad data recording.
q1 <- summ.ncalls[2]
q3 <- summ.ncalls[5]
iqr <- IQR(data$ncalls)
upper.limit <- q3 + 1.5 * iqr
lower.limit <- max(q1 - 1.5 * iqr, 0)

clean.ncalls <- data$ncalls[lower.limit < data$ncalls & data$ncalls < upper.limit]
truehist(clean.ncalls)

truehist(data$ncalls, xlab = '# calls per 5m')
lines(density(data$ncalls))
# We should not bother about the data with no calls. The summary does not indicate
# serious outliers, although the box plot shows a few. 

Y <- data$ncalls[data$ncalls > 0]
boxplot(Y)
truehist(Y)
lines(density(Y))

Y.hat <- rpois(n = length(clean.ncalls), lambda = mean(Y))

chisq.test(clean.ncalls, Y.hat, simulate.p.value = TRUE)
# p-value of 0.5187 suggests that we cannot reject the null hypothesis that the
# two populations are similar. So this test suggests that Y is indeed Poisson
# distributed.
M <- max(max(clean.ncalls), max(Y.hat))
plot(
  clean.ncalls[order(clean.ncalls)],
  Y.hat[order(Y.hat)],
  xlim = c(0, M),
  ylim = c(0, M),
  xlab = 'Actual',
  ylab = 'Simulated',
  main = 'Fit',
  cex = 0.1
)
abline(0, 1, col = 'blue')
# The fit is not bad. Let's assume that the incoming call data is indeed Poisson
# distributed.
