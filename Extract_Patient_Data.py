#### TO-DO:
# Use number of actual questions and answers in the for loops
# The formatting is defined for "LibreOffice Calc" on the Rpi4***


from xlsxwriter import Workbook
import mysql.connector

### Connecting to MySQL database
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'ajnist',
    password = 'nist', 
    database = "NIST_v1")

### Defining cursor for entire Python file
sql_cursor = mydb.cursor()

### Creating Excel file and sheets
patient_data = Workbook("patient_data.xlsx")
mc_data = patient_data.add_worksheet()
slider_data = patient_data.add_worksheet()

### Constants Used in Program
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
COLUMNS = ["%s1" % _ for _ in LETTERS]

SQL_MC_FIELDS = ["mc_id", "question", "option1", "option2", "option3", "option4"]
SQL_SLIDER_FIELDS = ["slide_id", "question", "slide_start", "slide_increment", "slide_limit"]

MC_HEADERS = ["MC #", "Question", "Option 1", "Option 2", "Option 3", "Option 4", "Patient Ans.", "Date", "Time"]
SLIDE_HEADERS = ["Slider #", "Question", "Start", "Increment", "End", "Patient Ans.", "Date", "Time", ""]

### Formatting for Excel sheets
BOLD_FONT = patient_data.add_format({"bold": True})
DATE_FONT = patient_data.add_format({"num_format": "dd-mm-yy"})
TIME_FONT = patient_data.add_format({"num_format": "hh:mm:ss"})
QUESTION_NUM_WIDTH = float(541/77)
QUESTION_WIDTH = float(2941/77)
OTHER_WIDTH = float(113/11)


### Creating headers for both sheets
for column, header in zip(COLUMNS, MC_HEADERS):
    mc_data.write(column, header, BOLD_FONT)
    
for column, header in zip(COLUMNS, SLIDE_HEADERS):
    slider_data.write(column, header, BOLD_FONT)

### Setting formatting for all columns
mc_data.set_column("A:A", QUESTION_NUM_WIDTH)
mc_data.set_column("B:B", QUESTION_WIDTH)
mc_data.set_column("C:I", OTHER_WIDTH)
slider_data.set_column("A:A", QUESTION_NUM_WIDTH)
slider_data.set_column("B:B", QUESTION_WIDTH)
slider_data.set_column("C:I", OTHER_WIDTH)

### Getting MC questions data
query = "SELECT * FROM mult_choice"
sql_cursor.execute(query)
mc_question_data = sql_cursor.fetchall()

### Getting MC answers data
query2 = "SELECT answer,date_stamp,time_stamp FROM mult_choice_answers"
sql_cursor.execute(query2)
mc_answer_data = sql_cursor.fetchall()

### Storing MC question and answer data into Excel
### ****Need to fix the ranges (get actual number of questions/answers)
for row in range(1,10):
    for column in range(6):
        mc_data.write(row,column, mc_question_data[row-1][column])

for row in range(1,40):
    mc_data.write(row, 6, mc_answer_data[row-1][0])
    mc_data.write(row, 7, mc_answer_data[row-1][1],DATE_FONT)
    mc_data.write(row, 8, mc_answer_data[row-1][2],TIME_FONT)

### Getting Slider question data
query3 = "SELECT * FROM slide"
sql_cursor.execute(query3)
slide_question_data = sql_cursor.fetchall()

### Getting Slider answer data
query4 = "SELECT answer,date_stamp,time_stamp FROM slide_answers"
sql_cursor.execute(query4)
slide_answer_data = sql_cursor.fetchall()

### Storing Slider question and answer data in to Excel
### ****Need to fix the ranges (get actual number of questions/answers)
for row in range(1,8):
    for column in range(5):
        slider_data.write(row,column, slide_question_data[row-1][column])

for row in range(1,9):
    slider_data.write(row, 5, slide_answer_data[row-1][0])
    slider_data.write(row, 6, slide_answer_data[row-1][1], DATE_FONT)
    slider_data.write(row, 7, slide_answer_data[row-1][2], TIME_FONT)

### Close Excel file
patient_data.close()



############ OLD CODE ##########


#print(mc_answer_data)
#print(mc_answer_data[26][2])
#print(type(mc_answer_data[26][2]))

#mc_data.write("K11",mc_answer_data[26][2])

#print(datetime.timedelta(seconds = mc_answer_data[26][2]))

#a,b,c,d,e,f = SQL_MC_FIELDS

###### Trying to call a single query using JOIN
###### Currently, won't work because tables have different # of rows!!!!
#query3 = "SELECT mult_choice.*, mult_choice_answers.answer, mult_choice_answers.date_stamp, mult_choice_answers.time_stamp FROM mult_choice"

