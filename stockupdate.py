import csv
import re
import json


    
class vlookup(object):

    def __init__(self):        
        self.input_file = raw_input('Enter the name file name: ')
        self.binpicking_number = raw_input('Enter the Bin Picking Number: ')
        # self.input_file = 'DickSportingGoods1.csv'
        # self.binpicking_number = 'DICKSPORTINGGOODS'
              
        master_file = open('masterfile.csv', 'r')
        master_dict = csv.DictReader(master_file) 

        self.product_id_dict = {}
        '''Dictionary of all products from the masterfile 
        with SKU as the key and Product ID as values'''
        for row in master_dict:
            if row['Bin Picking Number'].lower().strip() == self.binpicking_number.lower().strip():
                self.product_id_dict[row['Product Code/SKU']+row['Item Type'].strip()] = row['Product ID']

        self.header = True
        master_file.close()
        self.vlookup()
        

    def vlookup(self):
        csv_file = open(self.input_file, 'r')
        csv_dict = csv.DictReader(csv_file)

        output_file = open(self.input_file.replace(".csv","")+"_New.csv","wb")
        mywriter = csv.writer(output_file)
        
        for new_row in csv_dict:
            if (new_row['Product Code/SKU'] + new_row['Item Type'].strip()) in self.product_id_dict:                
                    new_row['Product ID'] = self.product_id_dict[new_row['Product Code/SKU']+new_row['Item Type'].strip()]
                    self.product_id_dict.pop(new_row['Product Code/SKU']+new_row['Item Type'].strip())
                
            else:
                 new_row['Product ID'] = ''      
            self.csv_writer(new_row, mywriter)

        csv_file.close()   
        output_file.close()
        self.out_of_stock()

    
    def csv_writer(self, new_row, mywriter):            
        header_row, row = [], []
        for key,values in new_row.iteritems():
            if self.header == True:                
                header_row += [key]                               
            
            row += [values]
        if header_row:
                self.header = False 
                mywriter.writerow(header_row)

        mywriter.writerow(row)

    def out_of_stock(self):         
        output_file = open(self.input_file.replace(".csv","")+"_OutOfStock.csv","wb")
        mywriter = csv.writer(output_file)
        header = ('Product SKU','Current Stock Level')
        mywriter.writerow(header)
        
        for key,value in self.product_id_dict.iteritems():
            SKU = key.replace('Product','').replace('SKU','')
            row = (SKU,0)            
            mywriter.writerow(row)

        output_file.close()

if __name__ == '__main__':   
    a = vlookup()
    
