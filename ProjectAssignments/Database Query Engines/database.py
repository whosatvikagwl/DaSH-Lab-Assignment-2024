class Table:
    def __init__(self, name, columns):
        """
        Initialize a table with a name and a list of column names.
        """
        self.name = name
        self.columns = columns
        self.data = []  # 2D matrix to store rows of data

    def insert(self, row):
        """
        Insert a row into the table.
        """
        if len(row) != len(self.columns):
            raise ValueError("Row length does not match number of columns")
        self.data.append(row)

    def select(self, column, condition):
        """
        Select rows from the table based on a condition.
        """
        # Assuming the condition is in the form column_name == value
        column_index = self.columns.index(column)
        selected_rows = []
        for row in self.data:
            if row[column_index] == condition:
                selected_rows.append(row)
        return selected_rows

    def delete(self, column, condition):
        """
        Delete rows from the table based on a condition.
        """
        # Using list comprehension to filter rows that do not meet the condition
        column_index = self.columns.index(column)
        self.data = [row for row in self.data if row[column_index] != condition]

    def max(self, column):
        """
        Calculate the maximum value of a column.
        """
        column_index = self.columns.index(column)
        return max(row[column_index] for row in self.data)

    def sum(self, column):
        """
        Calculate the sum of a column.
        """
        column_index = self.columns.index(column)
        return sum(row[column_index] for row in self.data)

    def cross_product(self, other_table):
        """
        Perform a cross product with another table.
        """
        result_columns = self.columns + other_table.columns
        result_data = []

        for row1 in self.data:
            for row2 in other_table.data:
                result_data.append(row1 + row2)
        
        result_table = Table(f"{self.name}_cross_{other_table.name}", result_columns)
        result_table.data = result_data
        return result_table


class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns):
        """
        CREATE a new table in the database.
        """
        if name in self.tables:
            raise ValueError("Table already exists")
        self.tables[name] = Table(name, columns)

    def alter_table(self, name, new_column):
        """
        ALTER table by adding a new column.
        """
        if name not in self.tables:
            raise ValueError("Table does not exist")
        self.tables[name].columns.append(new_column)
        for row in self.tables[name].data:
            row.append(None)  # Add None for the new column
        print(f"Column {new_column} added to table {name}.")

    def join(self, table1_name, table2_name, column_name):
        """
        Perform an inner join between two tables based on a common column.
        """
        if table1_name not in self.tables or table2_name not in self.tables:
            raise ValueError("One or both tables do not exist in the database.")
        
        table1 = self.tables[table1_name]
        table2 = self.tables[table2_name]

        if column_name not in table1.columns or column_name not in table2.columns:
            raise ValueError(f"Column '{column_name}' must exist in both tables.")

        # Get column indices for the join column
        index1 = table1.columns.index(column_name)
        index2 = table2.columns.index(column_name)

        # Prepare result table columns (all columns from both tables)
        result_columns = table1.columns + [col for col in table2.columns if col != column_name]
        result_data = []

        # Perform the inner join
        for row1 in table1.data:
            for row2 in table2.data:
                if row1[index1] == row2[index2]:  # Match on the join column
                    combined_row = row1 + [row2[i] for i in range(len(row2)) if i != index2]
                    result_data.append(combined_row)

        # Create and return the new table with joined data
        result_table_name = f"{table1_name}_join_{table2_name}"
        result_table = Table(result_table_name, result_columns)
        result_table.data = result_data

        print(f"Join completed: {table1_name} and {table2_name} on column '{column_name}'.")
        return result_table


# Sample test case to showcase the working of the code
db = Database()
db.create_table('Students', ['ID', 'Name', 'Age', 'Grade'])
db.tables['Students'].insert([1, 'Alice', 20, 'A'])
db.tables['Students'].insert([2, 'Bob', 21, 'B'])
db.tables['Students'].insert([3, 'Charlie', 22, 'A'])

db.create_table('Scores', ['ID', 'Score'])
db.tables['Scores'].insert([1, 95])
db.tables['Scores'].insert([2, 88])

# Perform SELECT operation
selected_students = db.tables['Students'].select('Grade', 'A')
print("Selected students with Grade A:", selected_students)

# Perform DELETE operation
db.tables['Students'].delete('Name', 'Bob')
print("Data after deleting Bob:", db.tables['Students'].data)

# Perform MAX operation
max_age = db.tables['Students'].max('Age')
print("Max Age of students:", max_age)

# Perform SUM operation
total_age = db.tables['Students'].sum('Age')
print("Total Age of students:", total_age)

# Create another table and perform CROSS PRODUCT operation
cross_product_result = db.tables['Students'].cross_product(db.tables['Scores'])
print("Cross product of Students and Scores:")
print(cross_product_result.data)

# Perform JOIN operation using join method
joined_table = db.join('Students', 'Scores', 'ID')
print("Joined Table Data using join method:", joined_table.data)

