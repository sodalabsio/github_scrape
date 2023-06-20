import os, requests, time
from dotenv import load_dotenv

# 1. create a .env file 
# 2. define GITHUB_TOKEN=<your github token> inside .env


load_dotenv()

class Query:
    def __init__(self, location:str, date_range:str, cursor=None):
        self.location = location
        self.date_range = date_range
        self.cursor = cursor
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        self.headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
        self.variables = {"queryString": f"location:{self.location} created:{self.date_range}", "afterCursor": self.cursor}

    def get_response(self):
        query = """
                query ($queryString: String!, $afterCursor: String) {
                search(query: $queryString, type: USER, first: 100, after: $afterCursor) {
                    userCount
                    pageInfo {
                    endCursor
                    hasNextPage
                    }
                    edges {
                    node { ... on User {
                        login
                        name
                        location
                        company
                        followers {
                            totalCount
                        }
                        following {
                            totalCount
                        }
                        repositories(first: 1) {
                            totalCount
                        }
                        createdAt
                        updatedAt}
                    }
                    }
                }
                }
                """
        
        response = requests.post("https://api.github.com/graphql", json={"query": query, "variables": self.variables}, headers=self.headers)
        return response

    def get_response_json(self):
        response = self.get_response()
        return response.json()

    def get_wait_time(self):
        response = self.get_response()
        limit_remaining = int(response.headers["X-RateLimit-Remaining"])
        if limit_remaining <= 0:
            reset_time = int(response.headers["X-RateLimit-Reset"])
            wait_time = reset_time - int(time.time()) + 5
            return wait_time
        return 0