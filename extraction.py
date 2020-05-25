import spacy
import re
import SSGLog
logger = SSGLog.setup_custom_logger('Neurobot')
logger.info("*****************START************************")



#pattern_dict= {}
#final_dict = {}

def name_finder(doc,pattern_dict):
    #nlp = spacy.load('en')  
    #nlp = en.load()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(doc)
    people = [str(ee) for ee in doc.ents if ee.label_ == 'PERSON']
    

    pattern_dict['name'] = people

def extract_PAN(text , pattern_dict):
    pan_no = re.findall(r'(\s[a-zA-Z]{5}[\d]{4}[a-zA-Z]{1}\s)', text)
    pattern_dict['pan number'] = pan_no
    #print("PAN Number :", re.findall(r'([a-zA-Z]{5}[\d]{4}[a-zA-Z]{1})', text))

def extact_account_num(text,pattern_dict):                   #001402000010199
    account_no = re.findall(r'\b\d{12}\b', text)
    pattern_dict['account number'] = account_no
    #print("Account Number : ", re.findall(r'([\d]{15}|[\d]{12})', text))

def extact_creditcardno(text,pattern_dict):                   #001402000010199
    cc_no = re.findall(r'\b\d{16}\b', text)
    pattern_dict['credit card number'] = cc_no

def extract_ifsc_code(text,pattern_dict):                    #IOBA0000195    ICICOOO6245
    ifsc_code = re.findall(r'([a-zA-Z]{7}[0-9]{4}|[a-zA-Z]{4}[\d]{7})', text)
    pattern_dict['IFSC code'] = ifsc_code
    #print("IFSC Code :", re.findall(r'([a-zA-Z]{7}[0-9]{4}|[a-zA-Z]{4}[\d]{7})', text))

def find_contact_no(value, pattern_dict):
    contact_num = re.findall(r'\s[9|8][0-9]{10}\s', value)
    pattern_dict['contact number'] = contact_num
    #print("Contact Number :", re.findall(r'\s[9|8][0-9]{9}\s', value))

def find_phone_fax(value, pattern_dict):                              #02667-666062   +91 22 43436969   +91 22 22852529  022-67080666
    phone_fax = re.findall(r'([\d]{5}\.[\d]{6}|[\d]{3}\.[\d]{9})', value)
    pattern_dict['phone/fax number'] = phone_fax
    #print("Phone/Fax Number :", re.findall(r'([\d]{5}\.[\d]{6}|[\d]{3}\.[\d]{9})', value))

def extract_currency(text, pattern_dict):
    currency = re.findall('\$|₹|USD|CAD|INR|Rs|rs|RS', text)
    pattern_dict['currency'] = currency

def extract_emails(text, pattern_dict):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    pattern_dict['emails'] = emails
    #print("Email Id :", re.findall(r'[\w\.-]+@[\w\.-]+', text))

def find_email_ID(string, pattern_dict):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    email_new = r.findall(string)
    pattern_dict['email Id'] = email_new
    #print("Email_ID:", r.findall(string))


def find_money(sentence):
    sentence1 = sentence.split()
    money_list = list(w for w in sentence.split() if re.search('(^₹[0-9]{1,5}|^\$[0-9]{1,5}|^Rs[0-9]{1,5}|[0-9]{1,5}Rs$)', w))
    #print("Money : ", money_list)
    money_sent = []
    for money in money_list:
        if money in sentence1:
            money_ind = sentence1.index(money)
            # print(money_ind)
            sent = sentence1[money_ind - 3:money_ind + 3]
            #print(sent)
            sentence1.remove(money)

def extract_total_amount(value, pattern_dict):
    print("value-->", value)
    amount_list1 = re.findall(r'(\s[\d]{3}[.][\d]{2}\s|\s[\d]{4}[.][\d]{2}\s|\s[\d]{5}[.][\d]{2}|\s[\d]{5}[.][\d]{2}\s|\s[\d]{6}[.][\d]{2}\s)', value)
    amount_list2 = re.findall(r'(\s[\d]{3}[.][\d]{2}\s|\s[\d]{1}[,][\d]{3}[.][\d]{2}\s|\s[\d]{2}[,][\d]{3}[.][\d]{2}|\s[\d]{2}[,][\d]{2}[,][\d]{3}[.][\d]{2})',value)
    amount_list3 = re.findall(r'([\d]{1,11}[/][-]|[\d]{1,11}\.[\d]{2}[/][-])', value)
    print("amount list3", amount_list3)
    amount_list2 = [s.replace(",", "")for s in amount_list2]
    amount_list = amount_list1+amount_list2+amount_list3
    logger.debug(" amount_list %s", amount_list)
    print("Amount List", amount_list)
    pattern_dict['amounts'] = amount_list

    #print("Amount List :", amount_list)
    # max_amount = [float(rs) for rs in amount_list]
    
    # try:
    #     max_amount = max(max_amount)
    #     pattern_dict['total amount'] = [max_amount]
    # except:
    #     pass


def transaction_id(value, pattern_dict):
    value = value.lower()
    invoice_po_list = ["transaction"]
    for ele in invoice_po_list:
        if ele in value:
            key_len = len(ele)
            index = value.index(ele)
            print("index",index)
            term_contnet = value[index+key_len:index+40]
            po_no = re.findall(r"\w*\d+\w*", term_contnet)
            #print("PO no", po_)
            logger.debug(" transaction %s", po_no)

            pattern_dict[ele] = po_no

def reference_no(value, pattern_dict):
    value = value.lower()
    invoice_po_list = ["reference"]
    for ele in invoice_po_list:
        if ele in value:
            key_len = len(ele)
            index = value.index(ele)
            print("index",index)
            term_contnet = value[index+key_len:index+40]
            po_no = re.findall(r"\w*\d+\w*", term_contnet)
            #print("PO no", po_)

            pattern_dict[ele] = po_no



def pre_processing(doc):
    #doc = str(doc).lower()
    contain = doc
    bad_chars = [';', ':', '!', "*", '/', '-']
    contain = ''.join(i for i in contain if not i in bad_chars)

    return str(contain)

def main_valid(doc):
    pattern_dict = {}
    #pattern_dict.clear()

    #f_doc = pre_processing(doc)

    str_content = doc.replace("\n", " ")
    #print(str_content)
    content = str_content
    extract_PAN(content, pattern_dict )
    extact_account_num(content,pattern_dict)
    extract_ifsc_code(content, pattern_dict)
    find_contact_no(content, pattern_dict)
    find_phone_fax(content, pattern_dict)
    extract_currency(content, pattern_dict)
    find_email_ID(content, pattern_dict)
    #find_money(content)
    extract_total_amount(content, pattern_dict)
    transaction_id(content, pattern_dict)
    name_finder(content, pattern_dict)
    extact_creditcardno(content, pattern_dict)
    #reference_no(content, pattern_dict)

    if len(pattern_dict) > 0:

        return pattern_dict
    
    #extract_name_entity(content)
    else:
        return {}

def pattern_finder(doc):
    #print("I am in textfile", doc)
    final_dict = {}

    try:
        #print("Doc", doc)
        a = main_valid(doc)
        #print(a)
        
        for k, v in a.items():
            

            if v:
                final_dict[k] = list(set(v))
            #print(final_dict)

        return final_dict

    except Exception as e:
        print("Text Error->", e)
        return "Error in extraction part"







    