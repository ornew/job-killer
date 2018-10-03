# JobKiller

Kubernetes Custom Controller

ジョブ絶対殺すマン

## Install

```
$ kubectl create secret generic \
    slack --from-literal=slack_webhook_url=https://hooks.slack.com/services/...
$ kubectl apply -f https://raw.githubusercontent.com/ornew/job-killer/master/job-killer.yaml
```

## How to use

Add `job-killer: kill-me` label to your job metadata.
See [test-job.yaml](test-job.yaml) example.
