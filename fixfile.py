from jira import JIRA
import pandas as pd
import csv

jira_options = {'server':'https://jira.surfstudio.ru/'}
jira = JIRA(options=jira_options, basic_auth=('login','password'))
filename = "csv1.csv"
res = []
str = ""
with open (filename,"r") as csv_file:
    lines = csv_file.readlines()
    final_list = [x.replace('\n', '') for x in lines]
    for task in final_list:
        str += task + ","
str = str[0:-1]
print (str)

jql = 'issue in ('+ str +')and status != "To Do"'
print(jql)
issues_list = jira.search_issues(jql)
for issue in issues_list:
    issue_key = issue.key
    find_issue = jira.issue(issue_key)
    sum = 0
    remaning = 0
    for log in find_issue.fields.worklog.worklogs:
        sum += log.timeSpentSeconds
        final_sum = sum/3600
        issue.update(fields={"timetracking":{"originalEstimate":"%s"% final_sum, "remainingEstimate":final_sum}})
        OrigEst = issue.fields.timetracking.remainingEstimateSeconds
        issue.update(fields={"timetracking": {"originalEstimate": "%s" % final_sum, "remainingEstimate": 0}})
        if OrigEst != sum:
            print(find_issue)
            print("error")
        else:
            print(find_issue)
            print("done")