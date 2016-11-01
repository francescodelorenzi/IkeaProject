def isfloat(value):
    
    value=value.replace(",",".")
    try:
        float(value)
        return True
    except:
        return False


if __name__ == '__main__':
    
    import sys
    if len(sys.argv) <= 2 :
        print "Usage: python ", sys.argv[0], "<IkeaSiteUrl> <codes.txt>"
        exit()
    site  = sys.argv[1]
    fcode = sys.argv[2]
    #    site = 'http://www.ikea.com/fr/fr/'
    #    fcode= "testID.txt"

    print "Prices Ikea ", site

    outname = site
    outname = outname.replace("http://www.ikea.com","Prices")
    outname = outname.replace("/","_")
    outname+=".txt"
    
    missname = fcode
    missname = missname.replace(".txt","")
    sitetag  = site.replace("http://www.ikea.com","")
    sitetag  = sitetag.replace("/","_")
    missname+=sitetag
    missname+="Missing.txt"
    
    print missname
    
    print "Prices written in ", outname
 
    from mechanize import Browser
    from bs4 import BeautifulSoup

    codes =[]
    # output file
    out  = open(outname,  'a',0)
    # file where codes that are not retrieved due to a networks hiccup are stored,
    # so it's possibe to rerun the script only on those.
    miss = open(missname, 'w',0)

    with open(fcode, "r") as f:
        for line in f:
            codes.append(line.replace('\n',""))

    # remove duplicates
    codes = set(codes) 
    
    browser = Browser()
    #browser.set_handle_redirect(False)
    
    '''
    Test URL
    '''
    from urllib2 import HTTPError
    try:
        resp = browser.open(site)
    except HTTPError, e:
        print "Got error code", e.code  
        print "Exit"
        exit()
 
    # Start scraping
    for c in codes:
        if c=="": # skip "empty" codes
            continue
            
        try:
            resp = browser.open(site)
            browser.select_form(nr=1)
    
            browser.form['query']= c #"202.054.49"
            browser.submit()
            response = browser.response().read()
 
            soup = BeautifulSoup(response,'lxml')
            tag = soup.find_all("div", class_="priceFamilyTextDollar")

            if tag:
                price = tag[0].get_text() 
                # print c, " ", price
                # The price contains both the value and the currency. 
                # I'll split it and, since the order of the value and the currency is not fixed, 
                # I'll try to identify the value.
                vc = price.split()#" ")
                value = None
                for v in vc:
                    value = v
                    value=value.replace(",",".")
                    value=value.replace("-","0")
                    if isfloat(value):
                        line =  c+" "+str(value)  
                        #print line
                        out.write(line+"\n")
                        out.flush()
                        break
                        #            line =  c, " ", value, "\n"
                        #            print line
            else:
                print "Warning: code", c, "not found"

        except HTTPError, e:
            print "Got error code", e.code  
            miss.write(c+"\n")
            miss.flush()
