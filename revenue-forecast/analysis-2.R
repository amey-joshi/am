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
  seg$ARPU,
  log(seg$Segment.2.MRR),
  cex = 0.1,
  xlab = 'ARPU',
  ylab = 'log(MRR)',
  main = 'Segment 2'
)

plot(seq(1:nrow(seg)), seg$ARPU, cex = 0.1, xlab = 'time', ylab = 'ARPU', main = 'Segment 2')
plot(seq(1:nrow(seg)), seg$Segment.2.MRR, cex = 0.1, xlab = 'time', ylab = 'MRR', main = 'Segment 2')

analyze_model <- function(formula.str, show.plot = TRUE) {
  x <- seg$ARPU[1:200]
  y <- seg$Segment.2.MRR[1:200]
  m <- lm(as.formula(formula.str))
  
  newdata <- data.frame(x = seg$ARPU[201:nrow(seg)])
  mrr.predicted  <- predict(m, newdata = newdata)
  mrr.actual  <- seg$Segment.2.MRR[201:nrow(seg)]
  
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

# Quadratic model.
m <- analyze_model('y ~ x + I(x^2)')
summary(m)
plot(m)

# Quadratic model.
m <- analyze_model('y ~ x + I(x^2)')
summary(m)
plot(m)

# Quadratic + exponential.
m <- analyze_model('y ~ x + I(x^2) + exp(x)')
summary(m)
plot(m)

# Trignometric + exponential
m <- analyze_model('y ~ I(x^2) +  cos(x) + exp(x)')
summary(m)
plot(m)

# Trignometric + exponential
m <- analyze_model('y ~ I(x^2) + cos(x) + exp(x)')
summary(m)
plot(m)

