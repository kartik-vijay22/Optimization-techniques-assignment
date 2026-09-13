import numpy as np

mVal = 100000.0


def runBigmSolver():
    labels = ["gpu", "cpu", "s_speed", "s_ram", "a_speed", "a_target"]

    objCosts = np.array([-5.0, -3.0, 0.0, 0.0, -mVal, -mVal], dtype=float)

    aMatrix = np.array(
        [
            [2.0, 4.0, -1.0, 0.0, 1.0, 0.0],
            [3.0, 2.0, 0.0, 1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0, 0.0, 0.0, 1.0],
        ]
    )

    rhs = np.array([12.0, 18.0, 5.0])

    curBasis = [4, 3, 5]

    mat = np.zeros((4, 7))
    mat[:3, :6] = aMatrix
    mat[:3, 6] = rhs

    print("=== STARTING BIG-M SIMPLEX ===")
    recalcZrow(mat, curBasis, objCosts)
    displayGrid(mat, labels)

    step = 1
    while step < 15:
        zVals = mat[3, :6]

        stopFlag = True
        for val in zVals:
            if val < -1e-4:
                stopFlag = False
                break

        if stopFlag:
            print("\nOptimal soln")
            break

        inCol = int(np.argmin(zVals))

        ratios = []
        for i in range(3):
            colVal = mat[i, inCol]
            if colVal > 1e-5:
                ratios.append(mat[i, 6] / colVal)
            else:
                ratios.append(1e9)

        outRow = int(np.argmin(ratios))

        if ratios[outRow] >= 1e8:
            print("unbounded/invalid")
            return

        print(
            f"\nIter {step}: Enter '{labels[inCol]}' | Leave '{labels[curBasis[outRow]]}'"
        )

        curBasis[outRow] = inCol

        pivotVal = mat[outRow, inCol]
        mat[outRow] = mat[outRow] / pivotVal

        for i in range(3):
            if i != outRow:
                scale = mat[i, inCol]
                mat[i] = mat[i] - scale * mat[outRow]

        recalcZrow(mat, curBasis, objCosts)
        displayGrid(mat, labels)

        step += 1

    gpuCount = 0.0
    cpuCount = 0.0

    for idx, bVar in enumerate(curBasis):
        if bVar == 0:
            gpuCount = mat[idx, 6]
        elif bVar == 1:
            cpuCount = mat[idx, 6]

    totalCost = (5.0 * gpuCount) + (3.0 * cpuCount)

    print("\n----------------------------------")
    print("RESULTS:")
    print(f"  GPU Instances (x1): {gpuCount:.2f}")
    print(f"  CPU Instances (x2): {cpuCount:.2f}")
    print(f"  Total Cost (Z):     ${totalCost:.2f}")
    print("----------------------------------")


def recalcZrow(tMat, basisList, cVec):
    for j in range(6):
        colDot = 0.0
        for i in range(3):
            colDot += cVec[basisList[i]] * tMat[i, j]
        tMat[3, j] = colDot - cVec[j]

    totalZ = 0.0
    for i in range(3):
        totalZ += cVec[basisList[i]] * tMat[i, 6]
    tMat[3, 6] = totalZ


def displayGrid(tMat, headers):
    print(
        "-------------------------------------------------------------------------"
    )
    hdrLine = "  ".join([f"{h:>6}" for h in headers]) + "     RHS"
    print(hdrLine)
    print(
        "-------------------------------------------------------------------------"
    )
    for i in range(3):
        rowStr = "    ".join([f"{val:6.1f}" for val in tMat[i, :6]])
        print(f"{rowStr} | {tMat[i, 6]:6.1f}")
    print(
        "-------------------------------------------------------------------------"
    )
    zStr = "  ".join([f"{val:6.1f}" for val in tMat[3, :6]])
    print(f"Z-C: {zStr} | {tMat[3, 6]:6.1f}")
    print(
        "-------------------------------------------------------------------------"
    )


if __name__ == "__main__":
    runBigmSolver()
