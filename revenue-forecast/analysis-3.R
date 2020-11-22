seg <- read.csv('segment-1.csv')
seg$month <- substr(seg$Date, 1, 2)

analyze_loess <- function(formula.str, show.plot = TRUE) {
  x <- seg$ARPU[1:200]
  y <- seg$Segment.1.MRR[1:200]
  m <- loess(as.formula(formula.str), control=loess.control(surface="direct"))
  
  newdata <- data.frame(x = seg$ARPU[201:nrow(seg)])
  mrr.predicted  <- predict(m, newdata = newdata)
  mrr.actual  <- seg$Segment.1.MRR[201:nrow(seg)]
  
  if (show.plot) {
    plot(
      newdata$x,
      mrr.actual,
      cex = 0.1,
      xlab = 'ARPU',
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
