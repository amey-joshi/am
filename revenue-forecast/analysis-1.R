seg <- read.csv('segment-1.csv')
seg$month <- substr(seg$Date, 1, 2)

analyze_model <- function(formula.str, show.plot = TRUE) {
  x <- seg$ARPU[1:200]
  y <- seg$Segment.1.MRR[1:200]
  m <- lm(as.formula(formula.str))
  
  newdata <- data.frame(x = seg$ARPU[201:nrow(seg)])
  mrr.predicted  <- predict(m, newdata = newdata)
  mrr.actual  <- seg$Segment.1.MRR[201:nrow(seg)]
  
  if (show.plot) {
    plot(
      mrr.actual,
      mrr.predicted,
      cex = 0.1,
      xlab = 'actual',
      ylab = 'predicted',
      main = formula.str
    )
    abline(0, 1, col = 'blue')
  }
  
  m
}
# Linear model.
m <- analyze_model('y ~ x')
summary(m)
plot(m)


# Linear model with cosine term.
m <- analyze_model('y ~ x + cos(x)')
summary(m)
plot(m)

# Quadratic model with cosine term.
m <- analyze_model('y ~ x + I(x^2) + cos(x)')
summary(m)
plot(m)

# From the three models fitted above, it is clear that the second model is the
# best.

# Can one find monthly MRR by aggregating the prediction?
m <- analyze_model('y ~ x + cos(x)', show.plot = FALSE)
newdata <- data.frame(x = seg$ARPU[201:nrow(seg)])
mrr.predicted  <- predict(m, newdata = newdata)

prediction <-
  data.frame(month = seg$month[201:nrow(seg)], mrr.predicted = mrr.predicted)
agg.prediction <-
  aggregate(mrr.predicted ~ month, data = prediction, sum)
agg.actual <-
  aggregate(Segment.1.MRR ~ month, data = seg[201:nrow(seg), ], sum)

agg.comparison <- merge(agg.actual, agg.prediction)
colnames(agg.comparison)[2] <- 'mrr.actual'
agg.comparison$pct_error <-
  (agg.comparison$mrr.predicted - agg.comparison$mrr.actual) / agg.comparison$mrr.actual

agg.comparison
# NO. The percentage error is quite high.

# Build a separate model for monthly aggregates.
seg.agg <-
  aggregate(cbind(Segment.1.MRR, ARPU) ~ month, data = seg, sum)
x <- seg.agg$ARPU[1:9]
y <- seg.agg$Segment.1.MRR[1:9]
m <- lm(y ~ x + cos(x), data = seg.agg)

newdata <- data.frame(x = seg.agg$ARPU[10:12])
y.pred <- predict(m, newdata = newdata)
comparison <-
  data.frame(x = newdata$x,
             actual = seg.agg$Segment.1.MRR[10:12],
             predicted = y.pred)
comparison$pct_error <-
  (comparison$predicted - comparison$actual) / comparison$actual
