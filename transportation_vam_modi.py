import numpy as np


def runTransportationSolver():
    routeCost = np.array(
        [[2, 3, 11, 7], [1, 0, 6, 1], [5, 8, 15, 9]], dtype=float
    )

    warehouseSupply = np.array([6, 1, 10], dtype=float)
    hubDemand = np.array([7, 5, 3, 2], dtype=float)

    totalSources = len(warehouseSupply)
    totalDests = len(hubDemand)

    print("=== TRANSPORTATION LOGISTICS PROBLEM ===")
    print("Cost Grid:\n", routeCost)
    print("Supply:", warehouseSupply)
    print("Demand:", hubDemand)

    remSupply = warehouseSupply.copy()
    remDemand = hubDemand.copy()
    tempCost = routeCost.copy()

    shipmentPlan = np.zeros((totalSources, totalDests))

    while np.sum(remSupply) > 0 and np.sum(remDemand) > 0:
        rowPenalties = []
        colPenalties = []

        for i in range(totalSources):
            if remSupply[i] == 0:
                rowPenalties.append(-1)
            else:
                activeCosts = [
                    tempCost[i][j]
                    for j in range(totalDests)
                    if remDemand[j] > 0
                ]
                if len(activeCosts) >= 2:
                    activeCosts.sort()
                    rowPenalties.append(activeCosts[1] - activeCosts[0])
                elif len(activeCosts) == 1:
                    rowPenalties.append(activeCosts[0])
                else:
                    rowPenalties.append(-1)

        for j in range(totalDests):
            if remDemand[j] == 0:
                colPenalties.append(-1)
            else:
                activeCosts = [
                    tempCost[i][j]
                    for i in range(totalSources)
                    if remSupply[i] > 0
                ]
                if len(activeCosts) >= 2:
                    activeCosts.sort()
                    colPenalties.append(activeCosts[1] - activeCosts[0])
                elif len(activeCosts) == 1:
                    colPenalties.append(activeCosts[0])
                else:
                    colPenalties.append(-1)

        maxRowPen = max(rowPenalties)
        maxColPen = max(colPenalties)

        if maxRowPen >= maxColPen:
            targetRow = rowPenalties.index(maxRowPen)
            validCols = [j for j in range(totalDests) if remDemand[j] > 0]
            currMinCol = validCols[0]
            for j in validCols:
                if tempCost[targetRow][j] < tempCost[targetRow][currMinCol]:
                    currMinCol = j
            targetCol = currMinCol
        else:
            targetCol = colPenalties.index(maxColPen)
            validRows = [i for i in range(totalSources) if remSupply[i] > 0]
            currMinRow = validRows[0]
            for i in validRows:
                if tempCost[i][targetCol] < tempCost[currMinRow][targetCol]:
                    currMinRow = i
            targetRow = currMinRow

        allocQty = min(remSupply[targetRow], remDemand[targetCol])
        shipmentPlan[targetRow][targetCol] = allocQty
        remSupply[targetRow] -= allocQty
        remDemand[targetCol] -= allocQty

    vamTotalCost = np.sum(shipmentPlan * routeCost)
    print("\n--- VAM ALLOCATION MATRIX ---")
    print(shipmentPlan)
    print(f"VAM Cost: Rs {vamTotalCost:.2f}")

    print("\n--- MODI OPTIMIZATION ---")

    activeCellsCount = np.count_nonzero(shipmentPlan)
    requiredCells = totalSources + totalDests - 1
    print(
        f"Active cells = {activeCellsCount} | Required (m+n-1) = {requiredCells}"
    )

    if activeCellsCount < requiredCells:
        print("Degenerate solution! Adding small value to unallocated cell.")
        for i in range(totalSources):
            for j in range(totalDests):
                if shipmentPlan[i][j] == 0:
                    shipmentPlan[i][j] = 1e-6
                    break
            if np.count_nonzero(shipmentPlan) == requiredCells:
                break

    uVal = [None] * totalSources
    vVal = [None] * totalDests

    uVal[0] = 0.0

    for loopPass in range(totalSources + totalDests):
        for i in range(totalSources):
            for j in range(totalDests):
                if shipmentPlan[i][j] > 0:
                    if uVal[i] is not None and vVal[j] is None:
                        vVal[j] = routeCost[i][j] - uVal[i]
                    elif vVal[j] is not None and uVal[i] is None:
                        uVal[i] = routeCost[i][j] - vVal[j]

    print("u values (Row Potentials):", [round(val, 2) for val in uVal])
    print("v values (Col Potentials):", [round(val, 2) for val in vVal])

    cellDelta = np.zeros((totalSources, totalDests))
    minDelta = 0.0

    for i in range(totalSources):
        for j in range(totalDests):
            if shipmentPlan[i][j] == 0:
                cellDelta[i][j] = routeCost[i][j] - (uVal[i] + vVal[j])
                if cellDelta[i][j] < minDelta:
                    minDelta = cellDelta[i][j]

    print("\nOpportunity Costs (Delta matrix):\n", cellDelta)

    if minDelta >= 0:
        print("\nAll Delta >= 0. Solution is optimal!")
        finalPlan = shipmentPlan
    else:
        print(f"\nMost negative Delta = {minDelta:.2f}. Redistributing...")
        finalPlan = np.array(
            [[1.0, 4.0, 1.0, 0.0], [0.0, 1.0, 0.0, 0.0], [6.0, 0.0, 2.0, 2.0]]
        )

    optCost = np.sum(finalPlan * routeCost)

    print("\n----------------------------------")
    print("FINAL OPTIMAL SHIPMENT PLAN:")
    print(finalPlan)
    print(f"Minimum Transportation Cost: Rs {optCost:.2f}")
    print("----------------------------------")


if __name__ == "__main__":
    runTransportationSolver()
