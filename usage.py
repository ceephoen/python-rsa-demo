# -*- coding: utf-8 -*-
"""
use the rsa to encrypt/decrypt data in tornado
"""
from tornado.web import RequestHandler
from .encryption import encrypt, decrypt


class CustomHandler(RequestHandler):
    """CustomHandler"""

    async def get(self, oid, *args, **kwargs):
        """get"""

        # 1 db
        col = config.get('col_name')
        try:
            order = await self.mongo.get_collection(col).find_one({'_id': ObjectId(oid)})
        except Exception as err:
            print(err)
            return self.write({'result': RET.DBERR, 'data': ''})

        # 2 data
        encrypt_list = list()
        str_order = json_util.dumps(order)  # dict->str

        str_order = re.sub(r'(\s|\n)', '', str_order)  # del \s \n  str

        str_list = re.findall(r'.{1,100}', str_order)  # split data to block list
        for i in str_list:
            a = encrypt(i)
            a = base64.b64encode(a)
            encrypt_list.append(a.decode('utf-8'))

        # 3 return resp
        return self.write({'result': RET.OK, 'data': encrypt_list})

    async def post(self, *args, **kwargs):
        """post"""
        data = self.get_json  # custom func to get json data
        decrypt_text_list = data.get('data')
        raw_str = ''

        for i in decrypt_text_list:
            b = base64.b64decode(i)
            c = decrypt(b)
            raw_str += c.decode('utf-8')

        return self.write({'result': RET.OK, 'data': {'raw_str': raw_str}})


"""
1-->
{
  "_id" : ObjectId("5b87ae520ef0413684f48e2c"),
  "lotteryBetinfo" : {
    "stakeNum" : 28,
    "betCode" : [{
        "codeZone2" : "02",
        "playType" : "duplex",
        "codeZone1" : "02,14,18,19,20,24,25,31",
        "codeType" : "a"
      }],
    "gameCode" : "053101",
    "gameName" : "3D",
    "multiple" : 3,
    "totalMoney" : 168
  },
  "location" : {
    "latitude" : 31.249161709999999,
    "longitude" : 121.48789949
  },
  "uid" : 2,
  "createTime" : 1535532887,
  "tags" : "a",
  "dealerId" : "a",
  "lotteryStation" : "a",
  "paymentId" : "ebee70a84900525c90fbd58475f735be",
  "paid" : 1,
  "paymentTime" : 1535532892
}

2-->
{
"data":[
"hfliQaSLNJCsYFE8ERyyk1Ww0lo7AUipSopGmqiTuIybHXNA0L9d5wnxjNiu1Lll4cuRYqIWnE85n8pbD7EWq3EGxWrpMkIJW8+xiQxqD5YBlJetw99sPSyQXiUV52Coa1fq8bSHQtevkD5zjY9juHmGIixTT3fAn11FOh5Mj4Q3RS8oSzkd3wzFSMo0whR6EugYzJ4FLfWcPEqYj0H+OoFnI/zHIQFERVJzJrdLDGOemWVIdW2GqGUgmaMQyoSjsm9o0P79o+cY5WYRX9ozjRep8Iz449Fyr+EOkmR52NWLiEvUzJZC7IZ1IZHSxmiVFsx4b46VREPuJ8V2yPYh7Q==",
"sJhczHJvlyPp+Y4Wo5ZIVF6iDrhHmM6+CUm6PwIOM2CSF1WSmef+rcMFST+yfcCwT6xJC9toAxDIseQe9DV+LIGFZBNLpFSJXFs9yWvv3On77n/jOZctifYhm4DMfgeNQI9NJ1jE23n5+tTKBbVuPBCYj0I/rAFECxF/75z4bOzwNqMSGdo98XACaYN9w9HW/iuo87jW6sEwDr2lP09Ahby+6XIQODYHLMg+jlZL0JImOsAeF7Bka51N3M3OwghAPH7mO3gatgtzsyuXb0Nk0h/3BumnZu6OT9fywzBMGnLM/TFK4oG1h0FjL+3iQrwj+Ayd4GTxqKiSjBNSIF+30A==",
"g4T+egZJF8V/AbFw9bPdvx+npGlSBnx8ecrXnF/sieMKAms5VKL2yAG0FoAblPqWN5ID4eMF7/bGLAIpEnG76Mt/fEonMhS4OYE+GbUwt8aB+WG2gFMyeSFvi15m9NPIRWQW5b/FqG+JJ4ubasmqPtqX+YyG+pzY5CARsQXldLdlLXXutRK/MmVw5gNeqhVXcXNYliRHVWLgXdOpJzzH8Mx/PxsHNV0nblCWnhc4aJL8C4dvzMzidKx7Yiah9kWq+wyd/9a2419WJ+BH2jJ//Ttx8UiX00h5xhb1en3vNiQzEa37xOf1THNeGS195IbcdBNwN/+HDTU9m6HfUCH+ug==",
"E7+7HVa2HUYDMNxijOiTt+hFNfA4TWdr4E/OETbUlE3W99YmwvEmE8DLRdWDjM9g0qej2q/0wKIqep+wQ7YLXT7IgU8DCR1pqqez/oMTFCoCL2ckUuK30w/bfbL1jQwqYH4ARRLzWiLyi/XPb1IUfFU2r2twVEULcaLJRBBXkGJ2HQf++TjVCJRE52yk5BNX6koqjQFyeNFv8C+rjJHi3t+5/7biY31xAD3mkX0+ZqtaxyELgsQu2SjvybGafjA9rm2xQlnI8NjcR9Ew7GwJGGPdQXoOOsWRgV/xVYJcB4vTUKga/RuK4y8c8rRYeKnYq08ihkki9ZU/XzTlorftPQ==",
"gmhMCECRUkA1EzzmPPMhLaJ1PYnZE/xi5KyhOk++HhV0X+iKgEBP/+iyiy7A8wpAUKHrY3xSdIWMP274jAGq8uG0+HcOLsnB+xtztyL19sMsxXZfY8r74CEFprWUmVWW9O1JkF1gkdBwN8h0MQJTHS/KXgUdkOeNSGeoAg2mcZzFj5uJwPQ0eiSPOVSsM+A6W3fh18s8FC6QqViiMFFXgZ/zTI3avCCms4lRmvMiySNh58LJHBqkTJAI/p3yGypxinOk4ClBEfEr64ZMIYvJ/ZuwdkE8gtC78szViBYw9sqQKvHjy4HsJxtZPyTa1Fzc4cNrElR7zomlk/eRzKOPkQ=="
]
}

"""