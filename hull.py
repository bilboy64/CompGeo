import sys 
import random
# import matplotlib.pyplot as plt


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
    

# Implementing my version of Graham's Scan Algorithm in R2
def ConvexHull2GS(P = []):

    n = len(P)      # Defining n = |P|
    LUpper = []     
    LLower = []
    
    P.sort()        # Organize elements in lexicographic order (sort() method by default does that in python)
        
    # Creating LUpper
    LUpper.append(P[0])     # Insert first and second element in LUpper 
    LUpper.append(P[1])     
    
    for i in range(2,n):
        LUpper.append(P[i])
        while len(LUpper) > 2 and orientation2(LUpper[-3],LUpper[-2],LUpper[-1]) > 0:
            LUpper.pop(-2)               # Add elif det == 0

            
    # Creating LLower
    LLower.append(P[n-1])       # n is 1-based, so last two elements are P[n-2] and P[n-1]
    LLower.append(P[n-2])
    for i in range(n-3,1,-1):
        LLower.append(P[i])
        while len(LLower) > 2 and orientation2(LLower[-3],LLower[-2],LLower[-1]) > 0:
            LLower.pop(-2)               # Add elif det == 0            
    
                            
    LLower.remove(LLower[0])    # Remove first and last elements of LLower
    LLower.remove(LLower[len(LLower) - 1])
    
    # Creating list of convex hull vertices L
    L = LUpper + LLower
    return L
        
    
    
    
  
# Main function 
def main():
    maxElements = 80
    points = [(random.randint(-10,100),random.randint(-10,100)) for i in range(maxElements)]     # Creating <maxElements> random points of R2   
    noList = ["No","NO","no","nO"]
    yesList = ["Yes","yes","YES", "yES", "yeS", "YEs"]
    while(1):
        print("Please insert the algorithm's name:")
        name = input()
        if name == "Graham's Scan":
            print("Length of point list:")
            print(len(points))
            print(points)
            L = ConvexHull2GS(points)
            print("Convex Hull: ", L)
            print(len(L))
            # plt.plot(L,color = 'magenta', marker = 'o')
            # plt.xticks(range(0,len(L)+1,1))
            # plt.xlabel('x')
            # plt.ylabel('y')
            # plt.title("Convex Hull")
            
            # plt.show()
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
    
