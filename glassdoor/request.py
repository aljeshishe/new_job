import json
import logging
import re

import attr
import jsonpath_ng
import scrapy

from glassdoor import constants, utils, middlewares
from glassdoor.state import State

log = logging.getLogger(__name__)

URL = "https://www.glassdoor.com/graph"
MAX_PAGE = 999

class RequestBase(scrapy.Request):
    def __str__(self):
        d = attr.asdict(self)
        d.pop("state")
        d_str = " ".join(f"{k}={v}" for k, v in d.items() if v is not None)
        return f"{self.__class__.__name__}({d_str})"

    __repr__ = __str__


@attr.define(eq=False)
class GetCsrfRequest(RequestBase):
    state: State
    def __attrs_post_init__(self):
        url = "https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=4&page=1&filterType=RATING_OVERALL"
        super().__init__(url=url, callback=self.parse, errback=middlewares.errback)

    def parse(self, response: scrapy.http.Response):
        result = re.search('"gdToken":"(.+?)"', response.text)
        if result is None:
            log.error(f"Cant find token")
            return
        csrf_token = result.group(1)
        log.info(f"Got {csrf_token=}")
        self.state.set_csrf_token(csrf_token)
        yield GetCountRequest(state=self.state, rating_min=3, rating_max=5)


@attr.define(eq=False)
class GetCountRequest(RequestBase):
    state: State
    rating_min: float
    rating_max: float

    def __attrs_post_init__(self):
        data = json.loads(constants.SEACH_DATA)
        data[0]["variables"]["employerSearchRangeFilters"][0]["maxInclusive"] = self.rating_max
        data[0]["variables"]["employerSearchRangeFilters"][0]["minInclusive"] = self.rating_min

        super().__init__(url=URL, method="POST", headers=self.state.headers, body=json.dumps(data),
                         callback=self.parse, errback=middlewares.errback)

    def parse(self, response: scrapy.http.Response):
        pages = jsonpath_ng.parse("$[0].data.employerSearchV2.numOfPagesAvailable").find(response.json())[0].value
        log.info(f"Going to crawls {pages=}")
        if pages > MAX_PAGE:
            log.info(f"Cant crawl > {MAX_PAGE} pages, splitting")
            for rating_min, rating_max in utils.gen_ranges(self.rating_min, self.rating_max, steps=20):
                yield GetCountRequest(state=self.state, rating_min=rating_min, rating_max=rating_max)
            return

        for page in range(1, pages + 1):
            yield SearchRequest(state=self.state, page=page)

# prepend pandas column with string

@attr.define(eq=False)
class SearchRequest(RequestBase):
    state: State
    page: int
    def __attrs_post_init__(self):
        data = json.loads(constants.SEACH_DATA)
        data[0]["variables"]["pageRequested"] = self.page
        super().__init__(url=URL, method="POST", headers=self.state.headers, body=json.dumps(data),
                         callback=self.parse, errback=middlewares.errback)

    def parse(self, response: scrapy.http.Response):
        results = jsonpath_ng.parse("$[0].data.employerSearchV2.employerResults[*].employer.id").find(response.json())
        if not results:
            print("Requiest returned no results")
            return
        ids = [result.value for result in results]
        yield GetInfosRequest(state=self.state, ids=ids)


@attr.define(eq=False)
class GetInfosRequest(RequestBase):
    state: State
    ids: list[int]

    def __attrs_post_init__(self):
        log.info(f"requesting {self.ids=}")
        data = [{
            "operationName": "ExplorerEmployerResultsGraphQuery",
            "variables": {
                "domain": "glassdoor.com",
                "id": id,
            },
            "query": "query ExplorerEmployerResultsGraphQuery($domain: String, $employerProfileId: Int, $gdId: String, $id: Int!, $ip: String, $locale: String, $locationId: Int, $locationType: String, $shortName: String, $userId: Int) {\n  EmployerJobs: employerJobsInfo(\n    context: {domain: $domain, gdId: $gdId, ip: $ip, locale: $locale, userId: $userId}\n    employer: {id: $id, name: $shortName}\n  ) {\n    eiJobsUrl\n    jobsCount\n    __typename\n  }\n  EmployerLocations: employerOfficeLocation(\n    context: {domain: $domain, gdId: $gdId, ip: $ip, locale: $locale, userId: $userId}\n    employer: {id: $id, name: $shortName}\n    locationId: $locationId\n    locationType: $locationType\n  ) {\n    eiOfficesLocationUrl\n    officeAddresses {\n      addressLine1\n      addressLine2\n      administrativeAreaName1\n      cityName\n      id\n      officeLocationId\n      __typename\n    }\n    __typename\n  }\n  EmployerReviews: employerReviews(\n    context: {domain: $domain, gdId: $gdId, ip: $ip, locale: $locale, userId: $userId}\n    employer: {id: $id}\n    dynamicProfileId: $employerProfileId\n  ) {\n    ...EmployerReviewsFragment\n    __typename\n  }\n  EmployerSalary: salariesByEmployer(\n    context: {domain: $domain, gdId: $gdId, ip: $ip, locale: $locale, userId: $userId}\n    employer: {id: $id}\n  ) {\n    salaryCount\n    __typename\n  }\n}\n\nfragment EmployerReviewsFragment on EmployerReviews {\n  allReviewsCount\n  employer {\n    headquarters\n    id\n    links {\n      overviewUrl\n      reviewsUrl\n      salariesUrl\n      __typename\n    }\n    overview {\n      description\n      __typename\n    }\n    primaryIndustry {\n      industryId\n      __typename\n    }\n    shortName\n    sizeCategory\n    squareLogoUrl\n    __typename\n  }\n  ratings {\n    overallRating\n    careerOpportunitiesRating\n    compensationAndBenefitsRating\n    cultureAndValuesRating\n    diversityAndInclusionRating\n    seniorManagementRating\n    workLifeBalanceRating\n    __typename\n  }\n  __typename\n}\n"
        } for id in self.ids]

        super().__init__(url=URL, method="POST", headers=self.state.headers, body=json.dumps(data),
                         callback=self.parse, errback=middlewares.errback)

    def parse(self, response: scrapy.http.Response):
        exceptions = [lambda k, v: k.startswith("__"), lambda k, v: isinstance(v, list)]
        for item in response.json():
            data = item["data"]
            result = utils.normalize(data, exceptions=exceptions)

            areas = set([address["administrativeAreaName1"] for address in data["EmployerLocations"]["officeAddresses"]])
            result["EmployerLocations_officeAddresses_administrativeAreaName1_list"] = list(areas)

            city_names = set([address["cityName"] for address in data["EmployerLocations"]["officeAddresses"]])
            result["EmployerLocations_officeAddresses_cityName_list"] = list(city_names)

            yield result

