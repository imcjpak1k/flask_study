from flask import request

def get_req_data(id, default=None):
	# print('get_param')
	if request.method == 'GET':
		return request.args.get(id, default)
	else:
		return request.form.get(id, default)

def toDatatablesObject(object=None, data=None, exception=None):
	"""
	JSON DATA를 datatable 그리드의 형태로 변환하여 반환(Object)
	EX1) 
	object 	=  {
  		"draw": 7,
		"recordsTotal": 57,
		"recordsFiltered": 57,
		"error"	: ""
	}
	data	= [
		{
			"A" : 1
		},
		{
			"A" : 2
		}
	]
	
	<결과값>
	{
  		"draw": 7,
		"recordsTotal": 57,
		"recordsFiltered": 57,
		"error"	: ""
		"data": [
			{
				"A" : 1
			},
			{
				"A" : 2
			}
		]
	}
	
	EX2) 
	object 	=  {
  		"draw": 7,
		"recordsTotal": 57,
		"recordsFiltered": 57,
		"error"	: ""
	}
	data	= [
		{
			"A" : 1
		},
		{
			"A" : 2
		}
	]
	exception=ValueError("오류가 있습니다.")
	
	<결과값>
	{
  		"draw": 7,
		"recordsTotal": 57,
		"recordsFiltered": 57,
		"error"	: "오류가 있습니다."
		"data": 
	}
	"""
	
	if type(object) == dict and 'draw' in object:
		if exception != None:
			object['error']				= "{}".format(exception)
		elif type(data) == list:
			object['data'] 				= data
			object['recordsTotal']		= len(data)
			object['recordsFiltered']	= len(data)
			object['error']				= None
		else :
			object['data'] 				= data.get('data')
			object['recordsTotal']		= data.get('total_count')
			object['recordsFiltered']	= data.get('total_count')
			object['error']				= None
		return object
	
	if type(data) == list:
		return {
			"draw": 1,
			"recordsTotal": len(data),
			"recordsFiltered": len(data),
			"error"	: None,
			"data": data
		}

	return object

# def toDatatablesArray(arrayJsonData=None):
# 	"""
# 	JSON DATA를 datatable 그리드의 형태로 변환하여 반환(Array)
# 	EX) 
# 	<변경전>
# 	[
# 		{
# 			"A" : 1
# 		},
# 		{
# 			"A" : 2
# 		}
# 	]

# 	<변경후>
# 	{
# 		"data": [
# 			{
# 				"A" : 1
# 			},
# 			{
# 				"A" : 2
# 			}
# 		]
# 	}
# 	"""
