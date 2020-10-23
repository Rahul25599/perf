'''
Created on 21-Oct-2020

@author: lsail
'''
from com.shaft.PageInsights import PageInsights

def main():
    page =  PageInsights("https://www.amazon.com/","AIzaSyBbFCnfGdhN6rfxwdhxDZYWYj0JKR2dTIc")
    page.getPageInsights()
    
    ' Test
    
if __name__ == "__main__":
    main()
