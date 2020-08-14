import json

answer1 = {
  'ok': True,
  'result': [{
    'update_id': 746898708,
    'channel_post': {
      'message_id': 2108,
      'chat': {
        'id': -1001221570774,
        'title': 'GoogleAssistant2Windows-Channel',
        'username': 'luahsdf5647',
        'type': 'channel'},
      'date': 1597348948,
      'text': 'starte Teamviewer'
    }
  }]
}

answer2 = {
    'ok': True,
    'result': []
    }

def exclude_result (dictionary):

    #exclude value of result in dicionary
    result_array = dictionary['result']

    #as the returned result is a list, it is neccesssary to pick the first element from the value,
    #as this constains the needed keys
    result_dic = result_array[0]

    #return the messsage
    return result_dic


print (exclude_result(answer1))
