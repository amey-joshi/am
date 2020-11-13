library(lpSolve)

advertisement <- c(1.3e6, 6e5, 5e5)
constraints <-
  matrix(
    data = c(
      9e4, 3e4, 4e4, # Planning cost.
      3e5, 1.5e5, 1e5, # Advertising cost.
      -1.2e6, -0.2e6, 0, # Young people.
      -0.5e6, -0.2e6, -0.2e6, # Middle-aged people.
      -0, -4e4, -1.2e5, # Coupons.
      1, 0, 0 # Available slots.s
    ),
    nrow = 6,
    ncol = 3,
    byrow = TRUE
  )

const.rhs <- c(1e6, 4e6, -5e6, -5e6, -1.49e6, 5)

stopifnot(length(const.rhs) == nrow(constraints))

lp.results <-
  lp(direction = "min",
     objective.in = advertisement,
     const.mat = constraints,
     const.dir = rep("<=", nrow(constraints)),
     const.rhs = const.rhs)
if (lp.results$status == 0) {
  print(paste('Objective value =', round(lp.results$objval, 0)))
  optimal.x <- lp.results$solution
  print(paste('Solution: x1 =', optimal.x[1], ' x[2] =', optimal.x[2], ' x[3] =', optimal.x[3]))
}
