window.onload = function(){
    
}

Trigger = 0
PlusTemp = 0
Counter = 0

FunctionList = []

//97 98 99  100 101 102  103 104 105
var FunctionEntry = function(){
    if(PlusTemp==394){ //9001
        alert('here')
        Trigger = 0
        PlusTemp = 0
        Counter = 0
    }
}

var FunctionRegister = function(FuncCode, Func){

}

window.onkeydown = function(e){
    console.log(e.which)
    if(Trigger>1){
        PlusTemp += e.which
        Counter += 1
        FunctionEntry()
        if(Counter==4){
            Trigger = 0
            PlusTemp = 0
            Counter = 0
        }
    }
    if(e.which == 17){
        Trigger+=1
    }
}