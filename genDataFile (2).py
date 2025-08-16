import os
import inspect
import csv as csv
import re


# Define the input and output file paths
cwd = inspect.getfile(inspect.currentframe())
cwd=os.path.dirname(os.path.abspath(cwd))

print(cwd)

"""
The ACS PUMS data files for 2023 (latest available as of project time)
are available at 
https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/

The California file is at
https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/csv_pca.zip

The site sometimes blocks access when accessed multiple times.
So, down the file once to a location on your system,
extract and use the psam_p06.csv file for further processing.
Also, GitHub limits individual file sizes to 25MB.
The csv_pca.zip is 68MB and unzipped csv is 270MB
The final Git repo will therefore only contain the processed pca2.csv file at 11MB.
"""

input_file = cwd+'/data/psam_p06.csv'
output_file = cwd+'/data/pca2.csv'


# List of fields to be copied
fields_to_copy = ['SERIALNO' ,'SPORDER' ,'WAGP' ,'AGEP' ,'COW' ,'SCHL' ,'SEX' ,'WKHP' ,'ESR' ,'NAICSP' ,'RAC1P' ,'HISP' ,'INDP' ,'OCCP' ,'SCIENGP' ,'SCIENGRLP']
fields_to_write = ['SERIALNO' ,'SPORDER' ,'WAGP' ,'AGEP' ,'COW' ,'SCHL' ,'SEX' ,'WKHP' ,'ESR' ,'NAICSP' ,'RAC1P' ,'HISP' ,'INDP' ,'OCCP' ,'SCIENGP' ,'SCIENGRLP','RACE']

# Open the input CSV file for reading
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    csv_reader = csv.DictReader(infile)
    
    # Open the output CSV file for writing
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        # Create a CSV writer object
        csv_writer = csv.DictWriter(outfile, fieldnames=fields_to_write)
        
        # Write header row to the output file
        csv_writer.writeheader()
        print(f'processing...')        
        # Iterate over rows in the input file
        nRows=0
        nWritten=0
        for row in csv_reader:
            if(nRows%10000==0):
                print(".", end="", flush=True)
            # Create a new row with only the selected fields
            filtered_row = {field: row[field] for field in fields_to_copy}
            if(filtered_row['WAGP']!='' and filtered_row['AGEP'] !='' and filtered_row['SCHL'] !='' and filtered_row['SEX'] !=''
               and float(filtered_row['WAGP']) > 0       #filter for records where wages are > 0 (current earners)
               and int(filtered_row['AGEP']) >= 18   #age 18 or older
               and float(filtered_row['WAGP'])<684000  #exclude top-coded wages (cutoff)
            ):
                if(  int(filtered_row['SCHL']) <= 15):
                     filtered_row['SCHL'] = '15' #anyone without at least a HS diploma 
                elif(  int(filtered_row['SCHL']) <= 19):
                     filtered_row['SCHL'] = '19' #anyone with at least HS but less than Associate Degree
                
                filtered_row['SERIALNO'] = re.sub('GQ', '00', filtered_row['SERIALNO']) # convert to a number by replacing GQ with 00
                filtered_row['SERIALNO'] = re.sub('HU', '11', filtered_row['SERIALNO']) # convert to a number by replacing HU with 11

                #some values for NAICSP/SCIENGP/SCIENGRLP have alphanumeric
                # Use regex to replace non-numeric characters with '0'
                #replacing with zero doesn't seem to create any duplicates/collisions with other values
                filtered_row['NAICSP'] = re.sub(r'[^0-9]', '0', filtered_row['NAICSP'])
                filtered_row['SCIENGP'] = re.sub(r'[^0-9]', '3', filtered_row['SCIENGP'])
                filtered_row['SCIENGRLP'] = re.sub(r'[^0-9]', '3', filtered_row['SCIENGRLP'])

                #treat empty fields as zero
                filtered_row['NAICSP']    = filtered_row['NAICSP']    if filtered_row['NAICSP']!= '' else '1'
                filtered_row['SCIENGP']   = filtered_row['SCIENGP']   if filtered_row['SCIENGP']!= '' else '3'
                filtered_row['SCIENGRLP'] = filtered_row['SCIENGRLP'] if filtered_row['SCIENGRLP']!= '' else '3'

                #create a new 'RACE' field and set it to the same value as RAC1P
                #except when the 'HISP' value is something other than '01' and '23'
                #if HISP is set to anything other than blank or 01 or 23,
                #treat as 'Hispanic' with a custom Race code of '0' (zero)
                filtered_row['RACE'] = filtered_row['RAC1P'] if filtered_row['HISP'] in ['01','23'] else 0

                # Write the filtered row to the output file
                csv_writer.writerow(filtered_row)
                nWritten+=1
            nRows+=1

print(f'\ndone creating {output_file}, accepted {nWritten} lines out of {nRows}')

