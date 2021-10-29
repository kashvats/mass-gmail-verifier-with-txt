import re
import socket
import dns.resolver
import smtplib

#email_address = ['lllllll@gmail.com','vatsakash168@gmail.com']
email_address = open("emailist.txt","r")
ka=list(email_address.read().split())
#Step 1: Check email
#Check using Regex that an email meets minimum requirements, throw an error if not
for addressToVerify in ka:
    #addressToVerify = email_address
    match = re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', addressToVerify)

    if match == None:
        print('Bad Syntax in ' + addressToVerify)
        raise ValueError('Bad Syntax')


    #Step 2: Getting MX record
    #Pull domain name from email address
    domain_name = addressToVerify.split('@')[1]


    #get the MX record for the domain
    records = dns.resolver.query(domain_name, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)

    #Step 3: ping email server
    #check if the email address exists

    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(host)
    server.mail('me@domain.com')
    code, message = server.rcpt(str(addressToVerify))
    server.quit()

    # Assume 250 as Success
    if code == 250:
        file1 = open("Validmail.txt","a")
        file1.write(f'{addressToVerify}\n')
        file1.close()
        print('valid address: ',addressToVerify)
        print('Y')
    else:
        file1 = open("Invalidmail.txt","a")
        file1.write(f'{addressToVerify}\n')
        file1.close()
        print('invalid address: ',addressToVerify)
        print('No')
email_address.close()
