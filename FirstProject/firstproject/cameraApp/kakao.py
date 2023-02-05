from distutils.util import execute
import json
import requests
#카카오
class Kakao():

    def __init__(self,m1,m2):
        self.m1 = m1
        self.m2 = m2

    def send_message(self):

        admin_email = self.m2.email
        admin_id = self.m2.username
        
        filename = "kakao_json/kakao_code_{}.json".format(admin_id)
        #경로 수정
        with open(filename, "r") as fp:        
            tokens = json.load(fp)

        headers = {
            "Authorization": "Bearer " + tokens["access_token"]
        }

        email_url = 'https://kapi.kakao.com/v2/user/me'
        result2 = json.loads(requests.get(email_url, headers=headers).text)
        print("email포함",result2['kakao_account']['email'])
        print()

        if (admin_email == result2['kakao_account']['email']):
            #메세지 보내기
            send_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
            cheating_message = self.m1

            data = {
                "template_object": json.dumps({
                    "object_type": "text",
                    "text":cheating_message,
                    "link": {
                        "web_url": "" # test
                    }
                })
            }
            response = requests.post(send_url, headers=headers, data=data)
            print("Response Status Code: {0}".format(response.status_code))

