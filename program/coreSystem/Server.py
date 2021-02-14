import os,sys

import PyBear.Library.WebSuite as WebSuiteBear

def GetHandler(Client):
    #Client.PrintRequest()
    Client.ReturnPageGet()

WebSuiteBear.StartHttpServer(ApplicationFileLocation='F:\Github\FileBear\Application\ControlPanel\WebShell', LibraryFileLocation='F:\Github\JsBear', GetHandler=GetHandler, PostHandler=None, ParameterAnalyst=None,)