import classify
import extraction
import json
import SSGLog
logger = SSGLog.setup_custom_logger('Neurobot')
logger.info("*****************START************************")



def email_classification(doc):

    for_model = doc

    final_result = {}

    try:

        classes = classify.classify(for_model)
        metadata = extraction.pattern_finder(doc)

        logger.debug(" Metadata %s", metadata)


        final_result['Class'] = classes
        final_result['Metadata'] = metadata


        data = json.dumps(final_result)
        logger.debug(" Data %s", data)
        with open ('result.json', 'w') as f:
            f.write(data)

        return final_result
        

    
    except Exception as e:
        print("Error", e)
        return "Something went wrong!"


if __name__ == "__main__":
    

    doc = """
    
    This is Subhrajyoti Mandal. My Account no is 123412341234. By mistact I have transfer wrong account. Toral Rs. 6000.00

    Regards,
    Subhra
    
    """

    print(email_classification(doc))