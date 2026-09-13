# Optimization Techniques Assignment

This repository contains the Python implementations for Assignment 1 on Operations Research / Optimization Techniques. The problems are formulated around practical optimization scenarios and solved using the Big-M Simplex Method and the Transportation Method with Vogel's Approximation Method (VAM) and MODI.

## Repository Contents

- `big_m_solver.py` — Big-M Simplex implementation for a cloud-computing resource allocation problem.
- `transportation_vam_modi.py` — Transportation problem implementation using VAM for the initial feasible solution and MODI for optimality analysis.

## 1. Big-M Simplex Method

### Problem Topic: Cloud Computing Resource Allocation

The first problem models a cloud-computing resource allocation decision. The goal is to determine how many GPU and CPU instances should be provisioned while satisfying several resource requirements.

The decision variables are:

- `gpu` (`x1`) — number of GPU instances.
- `cpu` (`x2`) — number of CPU instances.
- `s_speed` and `s_ram` — slack variables for resource constraints.
- `a_speed` and `a_target` — artificial variables introduced for constraints that require them.

The objective is to minimize the resource cost:

`Z = 5x1 + 3x2`

The constraints represented in the program are:

- `2x1 + 4x2 - s_speed + a_speed = 12`
- `3x1 + 2x2 + s_ram = 18`
- `x1 + x2 + a_target = 5`

### Code Logic

1. NumPy is used to store the objective coefficients, constraint matrix, and right-hand-side values.
2. A large value `M = 100000` is assigned to the artificial variables in the objective function.
3. The initial basis is set to the artificial/slack variables.
4. The Z-C row is calculated from the current basis.
5. The entering variable is selected using the most negative value in the Z-C row.
6. The leaving variable is selected using the minimum positive ratio test.
7. A pivot operation makes the entering variable a basic variable and eliminates it from the other constraint rows.
8. The Z-C row is recalculated after every pivot.
9. The process stops when there are no sufficiently negative Z-C values or when the iteration limit is reached.
10. The final values of GPU and CPU instances are extracted from the basis and the total cost is calculated.

### Important Functions

- `runBigmSolver()` controls the complete simplex procedure.
- `recalcZrow()` recalculates the Z-C row and objective value using the current basis.
- `displayGrid()` prints the current simplex tableau.

## 2. Transportation Problem

### Problem Topic: E-Commerce Fulfillment Logistics

The second problem models an e-commerce fulfillment network in which three warehouses supply four metro distribution hubs. Each warehouse has a fixed supply, each hub has a fixed demand, and every warehouse-to-hub route has a transportation cost.

The cost matrix is:

```text
[[ 2,  3, 11,  7],
 [ 1,  0,  6,  1],
 [ 5,  8, 15,  9]]
```

Warehouse supplies:

```text
[6, 1, 10]
```

Hub demands:

```text
[7, 5, 3, 2]
```

### Part A — Vogel's Approximation Method (VAM)

VAM is used to generate an initial feasible transportation solution.

The program:

1. Copies the original supply, demand, and cost data so the original values remain unchanged.
2. Calculates a penalty for every active row by finding the difference between its two lowest available transportation costs.
3. Calculates the corresponding penalties for every active column.
4. Selects the row or column with the largest penalty.
5. Within that row or column, selects the lowest-cost available route.
6. Allocates the maximum possible quantity, `min(supply, demand)`, to that route.
7. Updates the remaining supply and demand.
8. Repeats until all supply and demand have been allocated.
9. Calculates the total VAM transportation cost from the resulting allocation matrix.

### Part B — MODI Method

The program then performs MODI-based optimality analysis.

It first checks the number of occupied cells against the required number of basic cells:

`m + n - 1`

For a 3 × 4 transportation problem, the required number is 6.

If the solution is degenerate, the code inserts a very small value (`1e-6`) into an unallocated cell to provide the required number of basic cells.

Next, the program calculates the row and column potentials:

`u_i + v_j = c_ij`

for allocated cells.

For every unallocated cell, it calculates the opportunity cost:

`Delta_ij = c_ij - (u_i + v_j)`

If every opportunity cost is non-negative, the current solution is treated as optimal. If a negative opportunity cost exists, the program identifies the most negative Delta and uses the predefined final redistribution matrix in the code to obtain the final shipment plan.

### Important Functions / Sections

- `runTransportationSolver()` contains the complete transportation workflow.
- VAM penalty calculation determines the initial allocation.
- The MODI section calculates `u` and `v` potentials.
- The opportunity-cost matrix identifies whether an improving cell exists.
- The final section calculates the total transportation cost.

## How to Run

Install NumPy if it is not already installed:

```bash
pip install numpy
```

Run the Big-M program:

```bash
python big_m_solver.py
```

Run the Transportation program:

```bash
python transportation_vam_modi.py
```

## Summary

| Program | Optimization Topic | Method | Main Goal |
|---|---|---|---|
| `big_m_solver.py` | Cloud computing resource allocation | Big-M Simplex | Minimize GPU/CPU resource cost while satisfying constraints |
| `transportation_vam_modi.py` | E-commerce fulfillment logistics | VAM + MODI | Minimize transportation cost from warehouses to metro hubs |

These implementations demonstrate how classical Operations Research techniques can be applied to practical technology and logistics problems.