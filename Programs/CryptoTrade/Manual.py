from Core import CoreSystem

core = CoreSystem()
core.getOrderInfo()
print(core.data['Order'])
core.cancelAll()
#result = core.placeOrderMatchPrice(2,1)
#result = core.getOrderInfoById('Order6744283862287315331')
#result = core.cancelOrder('Order6744283862287315331')
#print(result)
