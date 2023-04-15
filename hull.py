import sys 
import random
import matplotlib.rcsetup as rcsetup
import matplotlib.pyplot as plt


# NOTES: 
# 1. The following program calculates convex hull of a randomly generated set (list) of elements of R^2 (and R^3).
# Every algorithm is defined as a function for organization purposes. 

# 2. According to the algorithm the user desires, the program calculates and prints the convex hull's vertices as its
# output. After every convex hull computation, we allow the user to re-enter an algorithm name of his choosing, if he 
# wants to test the correctness of each output. 

# 3. Terminate the program by either typing in "No" when asked if you want to continue, or by simply hitting ctrl + C.


# Functions
        
# Defining orientation predicate function in R2
# Note: pi[0] = xi, pi[1] = yi, where i = 0,1,2
def orientation2(p0 = [0,0], p1 = [0,0], p2 = [0,0]):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])
    


# Defining function that calculates squared distance between two elements of R2
# Note: pi[0] = xi, pi[1] = yi, where i = 0,1
def SqDist(p0=[0,0],p1=[0,0]):
    return (p0[0] - p1[0]) * (p0[0] - p1[0]) + (p0[1] - p1[1]) * (p0[1] - p1[1])



# Defining function that compares two elements of R2 using the orientation predicate 
# Note: it covers collinear case 
def cmp(p0=[0,0],p1=[0,0],p2=[0,0]):
    det = orientation2(p0,p1,p2)
    if det == 0:        # Collinear case
        if SqDist(p0,p2) >= SqDist(p0,p1):
            return -1
        else:
            return 1
    elif det < 0:
        return -1
    else: 
        return 1
    
    
# Defining a function that calculates which side of line (ab) p belongs in 
# Note: It's almost like calculating the orientation predicate determinant,
# but we also return a value based on turn of a,b,p
def findSide(a=[0,0],b=[0,0],p=[0,0]):
    result = (p[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (p[0] - a[0])
    
    if result > 0:
        return 1
    elif result < 0:
        return -1
    else:
        return 0
    

# Defining a function that calculates distance of element p from line (ab)
def distLine(a=[0,0],b=[0,0],p=[0,0]):
    return abs((p[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (p[0] - a[0]))



     

# Implementation 
print("\n\t\t Convex Hull Algorithms \n\n")

    
    
    
# 1. Graham's Scan Algorithm (R2) 

def GrahamsScan2(P = []):

    n = len(P)      # Defining n = |P|
    LUpper = []     
    LLower = []
    
    P.sort()        # Organize elements in lexicographic order (sort() method by default does that in python)
        
    # Creating LUpper
    LUpper.append(P[0])     # Insert first and second element in LUpper 
    LUpper.append(P[1])     
    
    for i in range(2,n):
        LUpper.append(P[i])
        while len(LUpper) > 2 and orientation2(LUpper[-3],LUpper[-2],LUpper[-1]) >= 0:
            LUpper.pop(-2)               # Add elif det == 0

            
    # Creating LLower
    LLower.append(P[n-1])       # n is 1-based, so last two elements are P[n-2] and P[n-1]
    LLower.append(P[n-2])
    for i in range(n-3,1,-1):
        LLower.append(P[i])
        while len(LLower) > 2 and orientation2(LLower[-3],LLower[-2],LLower[-1]) >= 0:
            LLower.pop(-2)               # Add elif det == 0            
    
                            
    LLower.remove(LLower[0])    # Remove first and last elements of LLower
    LLower.remove(LLower[len(LLower) - 1])
    
    # Creating list of convex hull vertices L
    L = LUpper + LLower
    L.append(L[0])
    return L
        
    
    
    
    
# 2. Gift-wrapping (Jarvis March) Algorithm (R2)

def JarvisMarch(P = []):
    
    n = len(P)
    r0 = 0        # Finding leftmost point P[r0] (r0 is index)
    for i in range(1,n):
        if P[i][0] < P[r0][0]:
            r0 = i
        elif P[i][0] == P[r0][0]:
            if P[i][1] > P[r0][1]: 
                r0 = i
                
    pos = P.index(P[r0])
    L = []        # Initialize list of convex hull vertices with element r0
    
    p = pos
    q = 0
    while(1):
        L.append(P[p])
        q = (p + 1) % n
        for i in range(n):        # We iterate over every element of P except for r0, which is the leftmost point
            det = orientation2(P[p],P[i],P[q])         # Calculating turn of r0,i,q, if they are collinear then choose the farthest element
            if det < 0 or (det == 0 and SqDist(P[i],P[p]) > SqDist(P[q],P[p])):
                q = i
        p = q
        if p == pos:
            break
        
    L.append(L[0])  
    return L


        
# 3. Divide and Conquer Convex Hull algorithm in R2
def divideAndConquer(P=[]):
    
    n = len(P)
    # Sorting elements of P in lexicographic order
    P.sort()
    
    # Finding leftmost and rightmost points a and b
    a = P[0]
    b = P[n-1]
    
    # Finding set of points to the left and right side 
    # of line (ab)
    
    # Convention: In case of collinearity, apply infinitesimal 
    # displacement method as follows: There's a 50% chance that 
    # elements y-coordinate will shift upward by 0.2 and 50% 
    # chance that it will shift downward by 0.2. Thus, the former
    # element belongs in leftSet and latter in rightSet
    leftSet = set()
    rightSet = set()
    for i in range(1,n-1):
        turn = orientation2(a,b,P[i])
        
        if turn > 0:        # Counter-clockwise, so left side
            leftSet.add(P[i])
        elif turn < 0:      # Clockwise, so right side
            rightSet.add(P[i])
        else: 
            if random.randint(0,1) == 0:
                P[i][1] = P[i][1] + 0.2
                leftSet.add(P[i])
            else:
                P[i][1] = P[i][1] - 0.2
                rightSet.add(P[i])

    
    
    
# 4. Recursive QuickHull Algorithm in R2

# Here, we define Hull as a global list since 
# our algorithm is recursive and we don't want
# it to reset on every call
quickHullL = []

# Note: p1 is the start and p2 the end of line (p1p2) <line>.
# Also, <side> is an indication of the position of element P[i]
# in relation to line (p1p2)
def QuickHull(P=[], p1=[0,0], p2=[0,0], side = 0):
   
    n = len(P)
    index = -1
    maxDistance = 0
    
    # Searching for point of P with max distance from line (p1p2)
    # (also calculating its turn)
    for i in range(n): 
        dist = distLine(p1,p2,P[i])
        if dist > maxDistance and findSide(p1,p2,P[i]) == side:
            index = i
            maxDistance = dist
    
    # If no such point was found, add points p1 and p2 to hull
    if index == -1:
        quickHullL.append(p1)
        quickHullL.append(p2)
        return
    
    # Repeat algorithm for parts of convex hull separated by P[index]
    QuickHull(P, P[index], p1, -findSide(P[index], p1, p2))
    QuickHull(P, P[index], p2, -findSide(P[index], p2, p1))
    
    
# Defining function that prints vertices of convex hull calculated 
# by the QuickHull algorithm
def printHull(P=[]):
    
    n = len(P)
    
    # Finding points with min and max x coordinate
    xMin = 0
    xMax = 0
    for i in range(1,n):
        if P[i][0] < P[xMin][0]:
            xMin = i
        if P[i][0] > P[xMax][0]:
            xMax = i
            
    # Recursively calculate convex hull on both sides
    # of line (P[xMin][0]P[xMax][0])
    QuickHull(P,P[xMin], P[xMax], 1)
    QuickHull(P,P[xMin], P[xMax], -1) 
    
    # Printing elements of convex hull
    print(quickHullL)
        
            
  
# Main function 
def main():
    maxElements = 80
    
    if maxElements < 3:
        print("Convex Hull is not possible! Enter a valid number of elements.")
        return
    
    points = [(random.randint(-10,100),random.randint(-10,100)) for i in range(maxElements)]     # Creating <maxElements> random points of R2   
    noList = ["No","NO","no","nO"]
    yesList = ["Yes","yes","YES", "yES", "yeS", "YEs"]
    while(1):
        print("Please insert the algorithm's name:")
        name = input()
        if name == "Graham's Scan R2":
            print("Points:", points)
            print("Length of point list:" , len(points))
            
            L = GrahamsScan2(points)
            n = len(L)
            print("Convex Hull: ", L)
            print("Vertices:", n)
            
            x = [L[i][0] for i in range(n)]
            y = [L[i][1] for i in range(n)]
    
            plt.plot(x,y,color = 'magenta', marker = 'o')
            plt.xticks(range(0, maxElements + 1, 1))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title("Convex Hull Graham's Scan")
            plt.show()
            
        elif name == "Gift-Wrapping" or name == "Jarvis March":
            print("Points:", points)
            print("Length of point list:" , len(points))
            
            L = JarvisMarch(points)
            n = len(L)
            print("Convex Hull: ", L)
            print("Vertices:", n)
                        
            x = [L[i][0] for i in range(n)]
            y = [L[i][1] for i in range(n)]
            
            plt.plot(x,y,color = 'magenta', marker = 'o')
            plt.xticks(range(0, maxElements + 1, 1))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title("Convex Hull Jarvis March")
            plt.show()
            
        elif name == "Quick Hull":
            print("Points:", points)
            print("Length of point list:" , len(points))
            
            printHull(points)
            L = quickHullL
            n = len(quickHullL)
            print("Vertices:", n)
            
            x = [L[i][0] for i in range(n)]
            y = [L[i][1] for i in range(n)]
    
            plt.plot(x,y,color = 'magenta', marker = 'o')
            plt.xticks(range(0, maxElements + 1, 1))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title("`Convex Hull QuickHull`")
            plt.show()
        elif name == "Divide and Conquer":
            print("Points:", points)
            print("Length of point list:" , len(points))
            
            L = divideAndConquer(points)
            n = len(L)
            print("Vertices:", n)
            
            x = [L[i][0] for i in range(n)]
            y = [L[i][1] for i in range(n)]
    
            plt.plot(x,y,color = 'magenta', marker = 'o')
            plt.xticks(range(0, maxElements + 1, 1))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title("`Convex Hull DC`")
            plt.show()
        elif name in noList:
            print("Do you want to exit?")
            choice = input()
            if choice in yesList:
                print("Ok then, exiting...")
                break
            elif choice in noList:
                continue
        else:
            print("Try again")


if __name__ == "__main__":
    main()
    
