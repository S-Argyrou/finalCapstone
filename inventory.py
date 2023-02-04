
# Import modules
from operator import attrgetter
import csv
from tabulate import tabulate

#========The beginning of the class==========

class Shoe:    
    '''Create a representation of shoe '''

    def __init__(self, country:str, code:str, product:str, cost:float, quantity:int):        
        '''
        Initialise attributes
           
        '''
        # Run check on passed arguments
        assert cost >= 0, f"Cost {cost} is not greater or equal to zero!"
        assert quantity >= 0, f"Quantity {quantity} is not greater or equal to zero!"

        # Define instance variables.
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
       
    def get_cost(self):        
        '''
        Return the cost of the shoe.

        Keyword arguments:
        None    
        '''
        return self.cost 

    def get_quantity(self):        
        '''
        Return the quantity of the shoes.
        
        Keyword arguments:
        None
        '''
        return self.quantity
    
    def update_quantity(self, num):        
        '''
        Update the quantity of the shoes by receving an integer as input.

        Keyword arguments:
        num (integer): number of items that need to be ordered
        
        Returns:
        all the attributes including the updated quantity.        
        '''
        self.quantity = self.quantity + num
        return self.country,self.code,self.product,self.cost,self.quantity
    
    def __str__(self):        
        '''
        Return a string representation of the class.

        Keyword arguments:
        None
        '''
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"

#=============Shoe list===========
    
# Define a variable to store a list of objects of shoes.
shoe_list = []

#==========Functions outside the class==============

def read_shoes_data():    
    '''
    Open the file inventory.txt, read the data from this file, then create a shoes object
    that is appended into the shoes list.
    
    Keyword arguments:
    None
    
    Returns:
    None
    '''
    # try to execute this part of the code.
    try:
        
        # Open the file in read mode.
        with open('inventory.txt', newline='') as f:

            # Define a variable to store the content of the file.
            reader = csv.reader(f)

            # Use next function to skip the first line (i.e the header)
            header = next(reader)

            # Loop through every line in the content
            for line in reader:
               
                # Assign each data at a specific index position to a variable.
                # Cast last two data into numbers.
                country = line[0]
                code = line[1]
                product = line[2]
                cost = float(line[3])
                quantity = int(line[4])
                
                # Instantiate a shoe object
                shoe = Shoe(country, code, product, cost, quantity)

                # Append the shoe object to the shoe_list
                shoe_list.append(shoe)

    # Define some possible exceptions 
    except FileNotFoundError:
        print("""
Oops! It seems the file you are looking for does not exist.
Before you move on, make sure you create it or enter the correct name.

If you don't have an inventory, type 'a' to create one and start adding
your shoes.
""")
    # If no exception is raised, print a success message.
    else:
        print("""
Data has been processed.
To check them, please type either 'vi' or 'cv'.
""")
            
     
def capture_shoes(ctry, cd, prod, cs, quty):
    '''
    Capture data about a shoe, use them to create a shoe object
    and append it inside the shoe list.

    Keyword arguments:
    ctry (string): country were the shoe has been made
    cd (string): code to identify the product
    prod (string): name of the product
    cs (float): coast 
    quty (integer): quantity
        
    Returns:
    None
    '''
    # Instantiate a shoe object from user input.
    shoe = Shoe(ctry, cd, prod, cs, quty)

    # Append shoe object inside the shoe list.
    shoe_list.append(shoe)

    # Open the file in append mode.
    with open('inventory.txt', 'a') as f:

        # Add at the end of the document the new shoe in its string representation. 
        f.write(f"{shoe.__str__()}\n")
    

def view_all():
    '''
    Iterate over the shoes list and print the details of the shoes returned from the __str__
    function in a neatly formatted way.

    Keyword arguments:
    None

    Returns:
    None
    '''
    # Create empty list to store the data.
    table = []

    # Loop through every shoe object in the shoe_list.
    for shoe in shoe_list:

        # Add the string representation of the shoe in the list.
        table.append(shoe.__str__().split(','))

    # Store the header into a list
    head = ['Country', 'Code', 'Product', 'Cost', 'Quantity']

    # Print the inventory neatly formatted.
    print(tabulate(table, headers=head, tablefmt = "fancy_grid"))
    print()
        

def re_stock(): 
    '''
    Find the shoe object with the lowest quantity, ask the user if they
    want to update this quantity and update the inventory.

    Keyword arguments:
    None

    Returns:
    None
    '''
    # Use min function to find the shoe object with the minimum quantity.
    # The additional parameter is specified in the key.
    lowest_quant = min(shoe_list, key=attrgetter('quantity'))
    
    # Cast the object in its string representation into a list
    l_qnty_as_list = [lowest_quant.__str__().split(',')]

    # Print relevant message.
    print(f"""This item was the one with lowest quantity:\n
{tabulate(l_qnty_as_list)}""")

    # Ask for user input.
    # Use lower method to eliminate case sensitivity.
    choice= input("\nWould you like to order some more of this product? Y/N: ").lower()

    # Check if user input is 'y'.
    if choice == 'y':

        # Try to execute this block of code.
        try:

            # If it is ask an integer input.
            new_quantity = int(input('Type how much more you need: '))

            # Define a variable to assign the index position of the shoe we want to update the quantity.            
            index_pos_low_qnt = shoe_list.index(lowest_quant) 
          
            # Update shoe quantity.
            lowest_quant.update_quantity(new_quantity)                     
            
            # Assign the updated object at the correct index position of the shoe_list.
            shoe_list[index_pos_low_qnt] = lowest_quant
           

            # Open the file in write and read mode.
            f = open('inventory.txt', 'w+')

            # Write the heading as first line.
            f.write('Country,Code,Product,Cost,Quantity\n')

            # Copy each object in shoe_list in the file.
            for shoe in shoe_list:
                f.write(f"{shoe}\n")

            # Print success message to inform the user.
            print('\nInventory updated\n')

        # Define some possible exceptions.
        except ValueError:

            # If exception raise, print error message and call the function again.
            print("\nOOps|You did not enter a whole number! Let's try again!\n")
            re_stock()

        # If no exception is raised closethe file.
        else:           
            f.close()

    # Check if user choice is 'n' and terminate the program.   
    elif choice == 'n':
        exit()

    # Display error message if invalid input and 'restart' the function.
    else:
        print('\nInvalid opition! Try again\n')
        re_stock()      
       
    
def search_shoe(cd):
    '''
    Search for a shoe from the list using the shoe code.

    Keyword arguments:
    cd (string): code to identify the product.

    Returns:
    the object if in inventory or an error message.
    '''
    # Create an empty list to store all the results.
    results =[]

    # Check for every shoe in the list if the input code is equal to the shoe code.    
    for shoe in shoe_list:        
        if shoe.code == cd:
            
            # If it is, return the shoe object in its string representation and cast it into a list.
            code_shoe = shoe.__str__().split(',')

            # Append ALL the results in the list.
            results.append(code_shoe)

    # Return results.
    return results  
        

def value_per_item():
    '''
    Calculate the total value for each item and print this information
    on the console for all the shoes.

    Keyword arguments:
    None

    Returns:
    None
    '''
    # Create empty list to store the data
    table = []

    # Loop through every shoe object in the shoe_list.
    for shoe in shoe_list:

        # Calculate the shoe value (= cost of the shoe time by the quantity)
        shoe.value = shoe.cost * shoe.quantity

        # Add a list made of shoe priduct and its value.
        table.append([shoe.product, shoe.value])

    # Store the header into a list
    head = ["Product name","Total value"]

    # Print the inventory neatly formatted.
    print(tabulate(table, headers=head, tablefmt='fancy_grid'))
    print()


def highest_qty():    
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.

    Keyword arguments:
    None

    Returns:
    None
    '''
    
    # Use max function to find the shoe object with the maximum quantity.
    # The additional parameter is specified in the key.
    highest_quant = max(shoe_list, key=attrgetter('quantity'))

    # Cast the object in its string representation into a list
    h_qnty_as_list = [highest_quant.__str__().split(',')]

    # Print a neatly formatted message.
    print(f"""
This item was the one with the highest quantity:
{tabulate(h_qnty_as_list)}

{highest_quant.product} is now ON SALE for only R{highest_quant.cost}!

When it's gone, it's gone...
""")

#==========Main Menu=============

# Define a variable to store an initial value for user_choice.
usr_choice = ''

# Call the function to have data ready to use.
read_shoes_data() 

# This loop will carry on executing until the user inputs quit.
while usr_choice != 'q':

    # Request user input.
    # Use lower method to convert input all lowercase.
    usr_choice = input("""Choose one of the following options:

add a new shoe - a
view inventory - vi
restock - r
search shoe - s
calc. value per item - cv
highest qnty - h
quit - q

Type here: """).lower()

    # Check what the input is and call the appropriate function.            
    if usr_choice == 'a':

        # Try to execute this block of code:
        try:

            # Request five user inputs.
            # Cast the last two into numbers.
            country = input('Type the country where the shoe has been made: ')
            code = input('Type the shoe code: ')
            product = input('Type the product name: ')
            cost = float(input('Type the cost: '))
            quantity = int(input('Type how many items of this product are in stock: '))

        # Define some possible exceptions.
        except ValueError:

            # If exception raise, print error message and call the function again.
            print("\nOOps|You were supposed to enter a number! Let's try again!\n")
            
        # If no exception is raised, pass the inputs as parametes and call the function to create a
        # new shoe object.
        else:            
            capture_shoes(country, code, product, cost, quantity)

            # Print a success message.
            print('\nItem added!\n')
            
    
    elif usr_choice == 'vi':        
        view_all()
        
    
    elif usr_choice == 'r':        
        re_stock()
        
        
    elif usr_choice == 's':        

        # Request user input and pass it as parameter in the function.        
        code = input("""\nIn order to perform this search you need to know the shoe code.
Please type it here: """)

        # Assign to a variable the data returned from search_shoe function.
        output = search_shoe(code)

        # Print the data in a neatly formatted way if a value has been returned.
        if output:            
            print(tabulate(output))
            print('\nSearch complete!\n')            
            

        # Otherwise print a message to inform the user.
        else:
            print("""
It seems that the item you are looking for is not in stock.
Alternatiely, check that your code is correct.
""")
            
        
    elif usr_choice == 'cv':        
        value_per_item()
        
        
    elif usr_choice == 'h':        
        highest_qty()
        
        
    elif usr_choice == 'q':

        # Terminate the program.
        exit()
        
    
    else:
        # Print relevant error message.
        print('Oops, invalid value!\n')
