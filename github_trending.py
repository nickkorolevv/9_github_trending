import requests
import datetime


def get_date_number_of_days_ago(date):
    return datetime.date.today() - datetime.timedelta(days=date)


def get_trending_repositories(top_size, date):
    url = "https://api.github.com/search/repositories"
    formated_date = "{}{}".format("created:>=", date)
    parameters = {'q': formated_date, 'sort': 'stars', 'order': 'desc'}
    decoded_json = requests.get(url, params=parameters).json()
    top_repos = decoded_json["items"][:top_size]
    return top_repos


def get_top_repos_with_issues(top_repos):
    for rep in top_repos:
        issues_url = (rep["issues_url"].rstrip("{/number}"))
        parameters = {"state": "open"}
        decoded_json = requests.get(
            issues_url, params=parameters).json()
        yield decoded_json


def print_top_repos(top_repos_with_open_issues, top_repos):
    for iss_repo, star_repo in zip(top_repos_with_open_issues, top_repos):
        print(
            "Ссылка: {}, звезды: {}, открытые вопросы: {}".format(
                star_repo["html_url"],
                star_repo["stargazers_count"],
                len(iss_repo))
        )


if __name__ == "__main__":
    date = 7
    number_of_top_repos = 20
    last_date = get_date_number_of_days_ago(date)
    top_repos = get_trending_repositories(number_of_top_repos, last_date)
    top_repos_with_open_issues = get_top_repos_with_issues(top_repos)
    print_top_repos(top_repos_with_open_issues, top_repos)
