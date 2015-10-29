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
        if (text.split()[domainIndex] in domains) or (text.split()[domainIndex] == '{' and text.split()[specialDomainIndex] in domains):
            continue
        if text.split()[domainIndex] == '{': # may need to iterate here
#work on special case
            #print text.split()[specialDomainIndex]
            domains.append(text.split()[specialDomainIndex])
            continue
        if(text.split()[2] == '{'): #may need to iterate here
            continue #work on special case
            print text.split()[domainIndex], ',', text.split()[3].split(':')[0], ',', text.split()[3].split(':')[1]
            continue
        
        r = "%s, %s, %s\n" % (text.split()[domainIndex], text.split()[2].split(':')[0], text.split()[2].split(':')[1])
        o.write(r)
        print text.split()[domainIndex], ',', text.split()[2].split(':')[0], ',', text.split()[2].split(':')[1]
        domains.append(text.split()[domainIndex])
        i+=1
f.close()
o.close()
# output:
# domain, type, class
# input:
# allow <domain> <type>:<class>
