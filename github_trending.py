import requests
import datetime
from collections import defaultdict


def date_number_of_days_ago(days_number):
    return datetime.date.today() - datetime.timedelta(days=days_number)


def get_trending_repositories(top_size, days_number):
    url = "https://api.github.com/search/repositories"
    date = "{}{}".format("created:>=", days_number)
    parameters = {'q': date, 'sort': 'stars', 'order': 'desc'}
    response_from_github = requests.get(url, params=parameters).json()
    top_repos = response_from_github["items"][:top_size]
    return top_repos


def get_top_repos_with_issues(top_repos):
    issues_dict = defaultdict(list)
    for rep in top_repos:
        issues_url = (rep["issues_url"].rstrip("{/number}"))
        parameters = {"state": "open"}
        response_from_gihub = requests.get(
            issues_url,
            params=parameters)\
            .json()
        issues_dict[(
            rep["html_url"],
            rep["stargazers_count"]
        )].append(len(response_from_gihub))
    return issues_dict


def print_top_repos(top_repos_with_open_issues):
    for top_rep, issues in top_repos_with_open_issues.items():
        print(
            "Ссылка: {}, звезды: {}, открытые вопросы: {}".format(
                top_rep[0],
                top_rep[1],
                issues[0])
        )


if __name__ == "__main__":
    days_number = 7
    number_of_top_repos = 20
    days = date_number_of_days_ago(days_number)
    top_repos = get_trending_repositories(number_of_top_repos, days)
    top_repos_with_open_issues = get_top_repos_with_issues(top_repos)
    print_top_repos(top_repos_with_open_issues)
