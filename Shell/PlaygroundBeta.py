from PyBear.GlobalBear import *
from PyBear.Library.Chart import *
from PyBear.Library.ModuleManager import *
from PyBear.Library.Chronus import *

import xml.dom.minidom as XML

from PyBear.Library.Financial import *

print(BondPresent(1000000, 0.1, 10, 0.05))
exit()

xml = '''
<xml>
        <ToUserName><![CDATA[gh_d9d1c2fef435]]></ToUserName>
        <FromUserName><![CDATA[oO3Ng5nUVlsp]]></FromUserName>
        <CreateTime>1588686640</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[jj]]></Content>
        <MsgId>22744526967177976</MsgId>
</xml>
'''

root = XML.parseString(xml).documentElement
a = root.getElementsByTagName('Content')[0].childNodes[0].nodeValue
print(a)
