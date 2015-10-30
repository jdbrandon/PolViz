#this is really quick and dirty right now, plan on abstracting and modularizing 
f = open("./all-the-policy.te")
o = open("./allow.csv", "w")
i=0
domainIndex = 1
specialDomainIndex = domainIndex + 1
domains = []
types = []
classes = []
for text in iter(f):
    if text[0] == '#':
        continue
    if 'allow' in text and 'neverallow' not in text:
        if (text.split()[domainIndex] in domains):
            continue
        if text.split()[domainIndex] == '{':
            #work on special case { <domain> -<option> } 
            domains.append(text.split()[specialDomainIndex])
            if(text.split(':')[1].split()[0] == '{'): #need to get more data in this case
                r = "%s, %s, %s\n" % (text.split()[specialDomainIndex], text.split(':')[0].split()[5], text.split(':')[1].split()[1])
            else:
                r = "%s, %s, %s\n" % (text.split()[specialDomainIndex], text.split(':')[0].split()[5], text.split(':')[1].split()[0])
            o.write(r)
            continue
        if(text.split()[2] == '{'): #may need to iterate here
            print text
            continue #work on special case
            print text.split()[domainIndex], ',', text.split()[3].split(':')[0], ',', text.split()[3].split(':')[1]
            continue
        
        r = "%s, %s, %s\n" % (text.split()[domainIndex], text.split()[2].split(':')[0], text.split()[2].split(':')[1])
        o.write(r)
#        print text.split()[domainIndex], ',', text.split()[2].split(':')[0], ',', text.split()[2].split(':')[1]
        domains.append(text.split()[domainIndex]) #make this a list of domain, type tuples
        i+=1
f.close()
o.close()
# output:
# domain, type, class
# input:
# allow <domain> <type>:<class>
