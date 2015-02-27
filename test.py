from lxml import etree

#with open('test2.html', 'rb') as fin, open('test2.out.html', 'wb') as fout:
    #shtml = fin.read()
    #find = "</td>\r\n<tr>\r\n</table>"
    #replace = "</td>\r\n</tr>\r\n</table>"
    #shtml.replace(find, replace)
    #fout.write(shtml.replace(find, replace))
    
with open('indiv.html', 'rb') as fin:
    shtml = fin.read()

#parser = etree.HTMLParser()
#startIndex = shtml.find('<body>') + 6
#stopIndex = shtml.find('</body>')
#shtml = shtml[startIndex: stopIndex].strip('\r\n')
tree = etree.HTML(shtml)
print(etree.tostring(tree))