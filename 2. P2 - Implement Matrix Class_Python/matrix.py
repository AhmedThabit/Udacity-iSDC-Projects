import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for i in range(width)] for j in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
       
        #calculating determinant for 1x1 and 2x2 matrix
        if self.h==1:
            det=self.g[0][0]
        
        #Using formula for determinant of a 2x2 matrix as (a*d-b*c) for [[a,b],[c,d]] matrix
        if self.h==2:
            det=self.g[0][0]*self.g[1][1]-self.g[0][1]*self.g[1][0]
            
        
        return det
    
        return None

        

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        
        #Initializing trace and then summing up values on the diagonal
        
        trace=0.0
        for i in range(self.h):
            trace=trace+self.g[i][i]
            
        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

      
        # using 2x2 matrix inverse formulation to define inverse
        
        det= self.determinant()
        
        #Avoiding division by zero
        if (det)==0:
                raise ValueError('Matrix determinant is zero, matrix has no inverse')
        
        inverse = []
        
        if self.h==1:
            inverse.append([1/self.g[0][0]])
        else:
            if self.h==2:
                inverse=[[((1/det)*self.g[1][1]), ((-1/det)*self.g[0][1])],[((-1/det)*self.g[1][0]),((1/det)*self.g[0][0])]]
                
        return Matrix(inverse)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        # Creating an empty transpose matrix and filling the elements from self as transposed
        matrix_transpose=[]
        
        for i in range(self.w):
            row=[]
            for j in range(self.h):
                row.append(self.g[j][i])
            matrix_transpose.append(row)
          
        return Matrix(matrix_transpose) 

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        #   
        # Performing addition for corresponding matrix elements
        #
        addition=[]
        for i in range(self.h):
            row=[]
            for j in range(self.w):
                row.append(self.g[i][j] + other[i][j])
            addition.append(row)
            
        return Matrix(addition)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        #   
        # Multiplying matrix elements by -1 and filling a new matrix(negative) as new output
        #
        negative=[]
        for i in range(self.h):
            row=[]
            for j in range(self.w):
                row.append(-1*self.g[i][j])
            negative.append(row)
            
        return Matrix(negative)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        #   
        # Performing element by element subtraction
        #
        subtraction=[]
        for i in range(self.h):
            row=[]
            for j in range(self.w):
                row.append(self.g[i][j] - other[i][j])
            subtraction.append(row)
            
        return Matrix(subtraction)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        #   
        # Creating a transpose matrix for "other" to perform row wise multiplication of elements, adding the results of each step to form one element of a row. Repeating this step to form column elements and then whole rows.
        #
        matrixC=other.T()
        
        # Verify 1:1 relation of own column count vs other's row count
        if self.w != other.h:   
            raise (ValueError, "Matrices can only be multiplied if the own row count matches the other's column count")
            
        product = []
        for i in range(self.h):
            row=[]
            for j in range(matrixC.h):
                Temp=0
                for a, b in zip(self.g[i], matrixC.g[j]):
                    Temp=Temp + a * b
                
                row.append(Temp)
                
            product.append(row)
            
        return Matrix(product)
       
            
                

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        #checking type and then multiplying 
        
        if isinstance(other, numbers.Number):
            result = []
            for i in self.g:
                row = []
                for j in i:
                    row.append(j*other)
                result.append(row)
                
            return Matrix(result)