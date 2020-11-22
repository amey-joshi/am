seg <- read.csv('segment-2.csv')
seg$month <- substr(seg$Date, 1, 2)

plot(
  seg$ARPU,
  seg$Segment.2.MRR,
  cex = 0.1,
  xlab = 'ARPU',
  ylab = 'MRR',
  main = 'Segment 2'
)

# A linear model is not going to fit well.
#
plot(
  seg$Total.paid.customers,
  seg$Segment.2.MRR,
  cex = 0.1,
  xlab = 'Total paid customers',
  ylab = 'MRR',
  main = 'Segment 2'
)

# Likely to get a better model with total paid customers.

analyze_model <- function(formula.str, show.plot = TRUE) {
  x <- seg$Total.paid.customers[1:200]
  y <- seg$Segment.2.MRR[1:200]
  m <- lm(as.formula(formula.str))
  
  newdata <- data.frame(x = seg$Total.paid.customers[201:nrow(seg)])
  mrr.predicted  <- predict(m, newdata = newdata)
  mrr.actual  <- seg$Segment.2.MRR[201:nrow(seg)]
  
  if (show.plot) {
    plot(
      newdata$x,
      mrr.actual,
      cex = 0.1,
      xlab = 'Total paid customers',
      ylab = 'MRR',
      main = formula.str,
      type = 'l'
    )
    lines(newdata$x, mrr.predicted, col = 'blue')
    legend(
      'topleft',
      legend = c('actual', 'predicted'),
      col = c('black', 'blue'),
      lty = c(1, 1),
      bty = 'n'
    )
  }
  
  print(summary(m))
  plot(m, cex = 0.1, main = formula.str)
  
  m
}

analyze_loess <- function(formula.str, show.plot = TRUE) {
  x <- seg$Total.paid.customers[1:200]
  y <- seg$Segment.2.MRR[1:200]
  m <- loess(as.formula(formula.str), control=loess.control(surface="direct"))
  
  newdata <- data.frame(x = seg$Total.paid.customers[201:nrow(seg)])
  mrr.predicted  <- predict(m, newdata = newdata)
  mrr.actual  <- seg$Segment.2.MRR[201:nrow(seg)]
  
  if (show.plot) {
    plot(
      newdata$x,
      mrr.actual,
      cex = 0.1,
      xlab = 'Total paid customers',
      ylab = 'MRR',
      main = formula.str,
      type = 'l'
    )
    lines(newdata$x, mrr.predicted, col = 'blue')
    legend(
      'topleft',
      legend = c('actual', 'predicted'),
      col = c('black', 'blue'),
      lty = c(1, 1),
      bty = 'n'
    )
  }
  
  print(summary(m))
  
  m
}

m <- analyze_loess('y ~ x')
m <- analyze_model('y ~ sqrt(x)')
m <- analyze_model('y ~ sqrt(x) + x')
m <- analyze_model('y ~ sqrt(x) + I(x^2)')

# Build a separate model for monthly aggregates.
seg.agg <-
  aggregate(cbind(Total.paid.customers, Segment.2.MRR) ~ month, data = seg, sum)
x <- seg.agg$Total.paid.customers[1:9]
y <- seg.agg$Segment.2.MRR[1:9]
plot(x, y)
abline(lm(y ~ x), col='blue')
# A linear model seems to fit well.
m <- loess(y ~ x, control=loess.control(surface="direct"))
newdata <- data.frame(x = seg.agg$Total.paid.customers[10:12])
y.pred <- predict(m, newdata = newdata)
comparison <- data.frame(x = newdata$x, actual = seg.agg$Segment.2.MRR[10:12], predicted = y.pred)
comparison$pct_error <- (comparison$predicted - comparison$actual)/comparison$actual
