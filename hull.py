import sys 
import random

# NOTES: 
# 1. The following program calculates convex hull of a randomly generated set (list) of elements of R^2 (and R^3).
# Every algorithm is defined as a function for organization purposes. 

# 2. According to the algorithm the user desires, the program calculates and prints the convex hull's vertices as its
# output. After every convex hull computation, we allow the user to re-enter an algorithm name of his choosing, if he 
# wants to test the correctness of each output. 

# 3. Terminate the program by either typing in "No" when asked if you want to continue, or by simply hitting ctrl + C.



# Implementation part 1
print("\n\t\t Convex Hull Algorithms \n\n")


# 1. Graham's Scan Algorithm 

def ConvexHull2GS(P = []):
    print(P)
    
    n = len(P)      # Defining n = |P|
    hull = []       # Defining hull as an empty list of vertices
    LUpper = []     
    LLower = []
    
    P.sort()        # Organize elements in lexicographic order (sort() method by default does that in python)
    print(P)
    
    # Creating LUpper
    LUpper.append(P[0])     # Insert first and second element in LUpper 
    LUpper.append(P[1])     
    
    for i in range(2,n):
        LUpper.append(P[i])
        det = orientation2(P[i-2],P[i-1],P[i])
        if len(LUpper) > 2:
            if det > 0:
                LUpper.remove(P[i-1])               # Add elif det == 0

            
    # Creating LLower
    
        
# Defining orientation predicate function in R2
# Note: pi[0] = xi, pi[1] = yi, where i = 0,1,2
def orientation2(p0 = [0,0], p1 = [0,0], p2 = [0,0]):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])
    
    

    
# Main function 
def main():
    maxElements = 80
    points = [(random.randint(0,100),random.randint(0,100)) for i in range(maxElements)]     # Creating <maxElements> random points of R2   
    noList = ["No","NO","no","nO"]
    yesList = ["Yes","yes","YES", "yES", "yeS", "YEs"]
    while(1):
        print("Please insert the algorithm's name:")
        name = input()
        if name == "Graham's Scan":
            ConvexHull2GS(points)
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
    
