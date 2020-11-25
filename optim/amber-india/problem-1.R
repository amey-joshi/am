library(lpSolve)

# The objective is to maximize the exposure through three advertisement channels.
# If x[1], x[2], x[3] are number of ads in TV, magazines and newspapers then the
# exposure is 1.3e6 x[1] + 6e5 x[2] + 5e5 x[3].
advertisement <- c(1.3e6, 6e5, 5e5)

# The constraints are:
# [1] Planning cost should be at most 1 MM. Therefore, 
#     9e4x[1] + 3e4x[2] + 4e4x[3] <= 1e6.
# [2] Advertising cost should be at most 4 MM. Therefore, 
#     3e5x[1] + 1.5e5x[2] + 1e5x[3] <= 4e6.
# [3] At least 5MM young people should be reached. 
#     1.2e6x[1] + 0.2e6x[2] + 0x[3] >= 5e6 or
#     -1.2e6x[1] - 0.26x[2] - 0x[3] <= -5e6.
# [4] At least 5MM middle-aged people should be reached.
#     -0.5e6x[1] - 0.2e6x[2] - 0.2e6x[3] <= -5e6
# [5] Exhaust last year's coupons.
#     -0x[1] - 4e4x[2] - 1.2e5x[3] <= -1.49e6
# [6] There are only five slots on TV.
#      x[1] + 0.x[2] + 0.x[3] <= 5.
constraints <-
  matrix(
    data = c(
      9e4, 3e4, 4e4, # Planning cost.
      3e5, 1.5e5, 1e5, # Advertising cost.
      -1.2e6, -0.2e6, 0, # Young people.
      -0.5e6, -0.2e6, -0.2e6, # Middle-aged people.
      -0, -4e4, -1.2e5, # Coupons.
      1, 0, 0 # Available slots.
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
  print(paste('Solution: x1 =', round(optimal.x[1], 2),
              ' x[2] =', round(optimal.x[2], 2), 
              ' x[3] =', round(optimal.x[3], 2)))
}
