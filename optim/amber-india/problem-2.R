library(nloptr)

# https://stackoverflow.com/questions/31431575/minimization-with-r-nloptr-package-multiple-equality-constraints

eval_f <- function(x) {
  # nloptr always minimizes the objective function. We want to maximize the
  # profit. Therefore, we seek to minimize negative of profit.
  objective <- 0.1 * x[1] * x[1] - 1.13 * x[1] + 0.4 +
    0.002 * x[2] * x[2] - 0.124 * x[2] - 0.14 +
    0.00321 * x[3] * x[3] - 0.706 * x[3] + 0.09
  gradient <-
    c(0.2 * x[2] - 1.13, 0.004 * x[2] - 0.124, 0.00641 * x[3] - 0.706)
  
  return(list('objective' = objective, 'gradient' = gradient))
}

eval_g_ineq <- function(x) {
  # These are the constraints from the previous part.
  constraints <- rbind(
    9e4 * x[1] + 3e4 * x[2] + 4e4 * x[3] - 1e6,
    3e5 * x[1] + 1.5e5 * x[2] + 1e5 * x[3] - 4e6,
    -1.2e6 * x[1] - 0.2e6 * x[2] + 5e6,
    -0.5e6 * x[1] - 0.2e6 * x[2] - 0.2e6 * x[3] + 5e6,
    -4e4 * x[2] - 1.2e5 * x[3] + 1.49e6,
    x[1] - 5
  )
  # Gradient of the constraints.
  gradient <- rbind(
    c(9e4, 3e4, 4e4),
    c(3e5, 1.5e5, 1e5),
    c(-1.2e6,-0.2e6, 0),
    c(-0.5e6,-0.2e6,-0.2e6),
    c(0,-4e6,-1.2e5),
    c(1, 0, 0)
  )
  return(list("constraints" = constraints, "jacobian" = gradient))
}

# Initial values, we start from the solution to the previous problem.
x0 <- c(4, 0, 14)

# lower and upper bounds of control
lb <- c(0, 0, 0)
ub <- c(Inf, Inf, Inf)
local_opts <- list("algorithm" = "NLOPT_LD_MMA",
                   "xtol_rel" = 1.0e-8)
opts <- list(
  "algorithm" = "NLOPT_LD_AUGLAG",
  "xtol_rel" = 1.0e-8,
  "maxeval" = 10000,
  "local_opts" = local_opts
)

res <- nloptr(
  x0 = x0,
  eval_f = eval_f,
  lb = lb,
  ub = ub,
  eval_g_ineq = eval_g_ineq,
  opts = opts
)

obj.val <- -res$objective * 1e6 # The lhs of quadratic equations is in MM USD.
print(paste('Objective-value:', round(obj.val, 2)))
optimal.x <- res$solution

cost <- c(9e4 + 3e5, 3e4 + 1.5e5, 4e4 + 1e5)
total.cost <- sum(cost * optimal.x)
net.profit <- obj.val - total.cost

print(paste('Net profit:', round(net.profit,0)))
print(paste('Solution: x1 =', round(optimal.x[1], 2),
            ' x[2] =', round(optimal.x[2], 2), 
            ' x[3] =', round(optimal.x[3], 2)))
