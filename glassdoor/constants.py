import email

headers_str = """Host: www.glassdoor.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/json
Content-Length: 120
Referer: https://www.glassdoor.com/
gd-csrf-token: cI7XzVIYLJC7Cfj0zpgzVg:2xEMjNzFCkilPu5Z0nkj3cal48OAqj_lGDhQbrC4iOKCr57uU7sih8Pv6F-QQLNxJaHPhytxqIQwYc_JvGypdA:iF0MKftd4aTOtGb1nNWGoKu66OYIUItbnKVTS0LzTeQ
apollographql-client-name: gd-header
apollographql-client-version: 1.0
Origin: https://www.glassdoor.com
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Connection: keep-alive
Cookie: AWSALB=4Zy1qsHdH8hBJ4o1KhvIkpRfVD94ayyvUxIii6W5u7rEpzrIemCIlsHg8d08Dt/DeayEYlQGsIhiy99HiSJKntCRhl3RULX6HVB7GHb0CTXQkXrXkUaXiLcPLLTm9aLxLSLreqanwJyYUwuV1+bxE+PdDcVkuwtb5+auirmdP6wl33JWhiRxuLLM5awr3A==; AWSALBCORS=4Zy1qsHdH8hBJ4o1KhvIkpRfVD94ayyvUxIii6W5u7rEpzrIemCIlsHg8d08Dt/DeayEYlQGsIhiy99HiSJKntCRhl3RULX6HVB7GHb0CTXQkXrXkUaXiLcPLLTm9aLxLSLreqanwJyYUwuV1+bxE+PdDcVkuwtb5+auirmdP6wl33JWhiRxuLLM5awr3A==; gdId=1cfe1cd4-126b-4921-bd8e-d2e387e4cbd0; trs=direct:direct:direct:2023-01-17+00%3A00%3A47.322:undefined:undefined; rl_session=RudderEncrypt%3AU2FsdGVkX1%2BVXTFyyqLVxu4gl5hPsQ1P5kWFIJZC4zfU4DadF%2BqpJmAKYLGA278zilWabVlqdcpSgX68m%2FeDQvI5G9MPaXQIMQM20G%2BCdX9jLldx7dhhQZrwMUmDTOMGa8AMLopd5XlLz4T0HhB21A%3D%3D; rl_user_id=RudderEncrypt%3AU2FsdGVkX1%2FRT3%2BHvIwj9gcnGjpfjugJWR3FoCnyYe4%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX1%2BxX0%2BKVN7MmMSA%2BLjts0SzZVXFpImizWDdhYKSP47I4dPBFi7ZCo38HGRsDyD4IuK6WWutTqNFw5GNXgJb%2BfqV%2FtDpVW5b8Z7xZIAX9bEqWFbPWnYvz9Py8yGcoRt%2BZmrCTuARKHtyEOJq1Zn55d%2BeKm26rgIF%2B6ylDVnUuXaZS8J%2F%2B%2FA%2FM06bSPsnAVF3mO4nWGgYDlVYow%3D%3D; rl_group_id=RudderEncrypt%3AU2FsdGVkX183I3VLpPWgpogo8olg1Nxk%2Fm2jk8Ub6M8%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2BcEhWCko1WTt8BQ1uFxNxuzXGwCs4LbdI%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX19HS3dPML6XP4AoqjS2s74BUGR4QvIDOFbgeOmMLV9MBqVM2gaUW%2FGXPjhKlX44%2B3%2B6gTM1hLC3iQ%3D%3D; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX1%2B9GYZzobTqVX6jTuURov9p%2BGPOBaZUiiQ%3D; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX18yPBl%2BYVg3y6opVaVKAl9qTfPaGqpmA4I%3D; G_ENABLED_IDPS=google; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jan+30+2023+18%3A11%3A29+GMT%2B0200+(Eastern+European+Standard+Time)&version=202211.1.0&isIABGlobal=false&hosts=&consentId=18784226-ed23-427b-8ce9-4efb2f6cc38d&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&AwaitingReconsent=false; _optionalConsent=true; _ga=GA1.2.1703850821.1673942453; amp_bfd0a9=MlUCb5MZh2W8qTVCva1VvD.MTc5MjQ3MTY=..1gnl09c53.1gnl09c57.3h.2.3j; _gcl_au=1.1.819048233.1673942454; _rdt_uuid=1673942454593.8c4e1d16-1e27-4b9b-bfec-cb259777f00b; __pdst=77c36bd407e74f7a84a25152ed78b9aa; _tt_enable_cookie=1; _ttp=PokPVYBJJfn6GALy5HLMuYMxl0N; _pin_unauth=dWlkPU5tUXpNR0ptT1RRdFptRm1ZeTAwWVdZeExUaGxaak10TnpCbE1EazBNMlUzT1RBMQ; ki_t=1673942459188%3B1675081026477%3B1675095058902%3B4%3B76; ki_r=; uc=44095BCBCAA84CA861247591574CD4C5954700B37D29EFE86B45FA6F2401DE7C81D91672619B8DCF260860C36E954F29532B666493B20C72D0A8EBE096A27A1F39F86ECED60CD805763A4109785E81278FAD613BF11D917206EB12A1C111C9D05D2D3D7F52485F95786B4DC9A1FB16C806D1F7CF775971B32C15EE33EABAEA9335884B883642014DCA457CA3C094577F; indeedCtk=1gnt6k6tpirkm801; ki_u=e7bd782a-59da-8a6d-2e91-bd8a; ki_s=218147%3A1.0.0.1.2%3B221866%3A13.0.0.0.2; g_state={"i_l":1,"i_p":1674428517910}; at=pF9jiKbYgMwKQSRshfZceZ07zQmklRP4KZIYajNLNLtxUuFDSzEhUryX57oG2FZJEiSYmfhFH7ZZSY-r0_HbOGFXRa11sy9-UQdV3l8eT6SqwaRQQZus5P7egji-kBpo4plQf_PAPvTNihB8KL8pP3Y4nKi9iOATws-n_baLNMQh1hMnIyHTeS9XFc4GL8ZjmPgAXpTdT7pjO39hLQ5kx3LO5KiqxAOXWFbGVzr1EZnmk7oeJav0oUzwG6YDKfoyC0PJQKhHxYoha_AVbVl829hvO2X0yu2sWUq0I7iqMEYlAFyKmX5Mim2keyPamSwBdRdLv-8_5oiH8wa68IiyCNrOnpbAa3dxecMF7ec5goAVAQ0CEi6KIFSJ05C2vnkCc9V3X-D9PcK_HPYj062Hy4e79EJewTYD-H2Mhe5I-Ykv7HXXe9BvoAhgcENVF-GjWNhqD3x44CYrClWRkrmgsELPoXd-tC-4HbEreJ3L1pGUZdkqROBpz_pLsS-vrPK7VRislk8KVXGIqQP-Ol7CTVVMk_u3lZMAgTwag1UfZkKGTglMuyPLbqTpvSYUE9FOJQdSXcFz1EBuzmAGHJTk9C-a1GEnuHNmvXWTL-iPaCS0WhvURqoNQrtOHzkGTQQPoLNBzRRdfhj4vYNPoSV35tnxfIV46PFOPEbq8W3mxeDLc0xiySjWXqzpwSM8jHR8YL_vN2NgXn8yc1yh1vqJE2oDHTJZ_I7p86tvWupnB2OCrE9H5aPJ6ez6LC3hUrjJg8zj_t7_VoWq8Bzr0SqjHfFk8bG0OD9duSPTiqg9G6wJAv3daYXObgBwe5jMKatbMNKbNHYZwsh1oUKP80yZw48Cn-GLRk1ibxbv2oR2tXw; _janalytics_id.34ac=c8c4d13d-98c4-4c74-880e-62649da78077.1674422932.4.1674943626.1674852422.14f15e4d-b5c4-4bb4-b39d-bc84a8dfc035; fpvc=11; G_AUTHUSER_H=0; LSKey-CoveoV2$coveo_visitorId=0eadd746-33eb-958a-1de3-c6a10b33e3b7; __cf_bm=IpqrqYlw58hbnJyJ7btcTy35yorTSKUD8JZcer5iPjI-1675236336-0-AVe3+41q9qI0Br68L7W4k38Mvjd2gsGFkAjHVFxldALeAdhcsC69znjrXGLgHix7o1aGwDMC3pagb2YRhKKsJoU=; asst=1675228696.0; GSESSIONID=undefined; gdsid=1675228700192:1675234719466:A5153905742B04A12B3DFC776C7DC7BE; JSESSIONID=5F329CD2D2B20DEDDDB852EA3789ABEB; cass=1; bs=joyQpCAivVR_wbp0H3seWA:TZCSFm5iP9JVyMyOFI3dQbeswBcKpN6tlbXdtcZQzpLHV9RyYn4JHVk13QFcFhgbFBBn0Io3lraY01Wza0v_O1z_pfOVd9m7bCfHD7-fm8U:KlKjsfCASCaHHXBkbkssrA3ATi9kU0EXIHggUU_Tec8
Pragma: no-cache
Cache-Control: no-cache"""
HEADERS = dict(email.message_from_string(headers_str))
HEADERS.pop("Content-Length")
HEADERS.pop("Accept-Encoding")

SEACH_DATA = r"""[
  {
    "operationName": "ExplorerEmployerSearchGraphQuery",
    "variables": {
      "employerSearchRangeFilters": [
        {
          "filterType": "RATING_OVERALL",
          "maxInclusive": 5,
          "minInclusive": 2
        }
      ],
      "industries": [],
      "jobTitle": "",
      "location": null,
      "pageRequested": 0,
      "preferredTldId": 1,
      "sGocIds": [
        1007
      ],
      "sectors": []
    },
    "query": "query ExplorerEmployerSearchGraphQuery($employerSearchRangeFilters: [EmployerSearchRangeFilter], $industries: [IndustryIdent], $jobTitle: String, $location: UgcSearchV2LocationIdent, $pageRequested: Int, $preferredTldId: Int, $sGocIds: [Int], $sectors: [SectorIdent]) {\n  employerSearchV2(\n    employerSearchRangeFilters: $employerSearchRangeFilters\n    industries: $industries\n    jobTitle: $jobTitle\n    location: $location\n    pageRequested: $pageRequested\n    preferredTldId: $preferredTldId\n    sGocIds: $sGocIds\n    sectors: $sectors\n  ) {\n    employerResults {\n      demographicRatings {\n        category\n        categoryRatings {\n          categoryValue\n          ratings {\n            overallRating\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      employer {\n        bestProfile {\n          id\n          __typename\n        }\n        id\n        shortName\n        ratings {\n          overallRating\n          careerOpportunitiesRating\n          compensationAndBenefitsRating\n          cultureAndValuesRating\n          diversityAndInclusionRating\n          seniorManagementRating\n          workLifeBalanceRating\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    numOfPagesAvailable\n    numOfRecordsAvailable\n    __typename\n  }\n}\n"
  }
]"""

"""
Job Functions
sGocIds:
    1007 - engineering
"""